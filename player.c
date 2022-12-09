/*
 *  Copyright (c) 2010 The WebM project authors. All Rights Reserved.
 *
 *  Use of this source code is governed by a BSD-style license
 *  that can be found in the LICENSE file in the root of the source
 *  tree. An additional intellectual property rights grant can be found
 *  in the file PATENTS.  All contributing project authors may
 *  be found in the AUTHORS file in the root of the source tree.
 */

// Simple Decoder
// ==============
//
// This is an example of a simple decoder loop. It takes an input file
// containing the compressed data (in IVF format), passes it through the
// decoder, and writes the decompressed frames to disk. Other decoder
// examples build upon this one.
//
// The details of the IVF format have been elided from this example for
// simplicity of presentation, as IVF files will not generally be used by
// your application. In general, an IVF file consists of a file header,
// followed by a variable number of frames. Each frame consists of a frame
// header followed by a variable length payload. The length of the payload
// is specified in the first four bytes of the frame header. The payload is
// the raw compressed data.
//
// Standard Includes
// -----------------
// For decoders, you only have to include `vpx_decoder.h` and then any
// header files for the specific codecs you use. In this case, we're using
// vp8.
//
// Initializing The Codec
// ----------------------
// The libvpx decoder is initialized by the call to vpx_codec_dec_init().
// Determining the codec interface to use is handled by VpxVideoReader and the
// functions prefixed with vpx_video_reader_. Discussion of those functions is
// beyond the scope of this example, but the main gist is to open the input file
// and parse just enough of it to determine if it's a VPx file and which VPx
// codec is contained within the file.
// Note the NULL pointer passed to vpx_codec_dec_init(). We do that in this
// example because we want the algorithm to determine the stream configuration
// (width/height) and allocate memory automatically.
//
// Decoding A Frame
// ----------------
// Once the frame has been read into memory, it is decoded using the
// `vpx_codec_decode` function. The call takes a pointer to the data
// (`frame`) and the length of the data (`frame_size`). No application data
// is associated with the frame in this example, so the `user_priv`
// parameter is NULL. The `deadline` parameter is left at zero for this
// example. This parameter is generally only used when doing adaptive post
// processing.
//
// Codecs may produce a variable number of output frames for every call to
// `vpx_codec_decode`. These frames are retrieved by the
// `vpx_codec_get_frame` iterator function. The iterator variable `iter` is
// initialized to NULL each time `vpx_codec_decode` is called.
// `vpx_codec_get_frame` is called in a loop, returning a pointer to a
// decoded image or NULL to indicate the end of list.
//
// Processing The Decoded Data
// ---------------------------
// In this example, we simply write the encoded data to disk. It is
// important to honor the image's `stride` values.
//
// Cleanup
// -------
// The `vpx_codec_destroy` call frees any memory allocated by the codec.
//
// Error Handling
// --------------
// This example does not special case any error return codes. If there was
// an error, a descriptive message is printed and the program exits. With
// few exceptions, vpx_codec functions return an enumerated error status,
// with the value `0` indicating success.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "vpx/vpx_decoder.h"
#include "vpx_ports/mem_ops.h"

#include "./ivfdec.h"
#include "./tools_common.h"
#include "./video_reader.h"
#include "./vpx_config.h"
#include "./common.h"

static const char *exec_name;

void usage_exit(void) {
  fprintf(stderr, "Usage: %s <infile> <outfile> <sr infile> <scale> <skip>\n",
          exec_name);
  exit(EXIT_FAILURE);
}

int main(int argc, char **argv) {
  int frame_cnt = 0;
  FILE *outfile = NULL;
  vpx_codec_ctx_t codec;
  VpxVideoReader *reader = NULL;
  const VpxInterface *decoder = NULL;
  const VpxVideoInfo *info = NULL;

  FILE *sr_infile = NULL;
  vpx_image_t raw;
  int scale;
  int skip;

  exec_name = argv[0];

  if (argc != 6) die("Invalid number of arguments.");

  reader = strcmp(argv[1], "-") ? vpx_video_reader_open(argv[1])
                                : vpx_video_reader_open_stdin(argv[1]);
  if (!reader) die("Failed to open stdin for reading.");

  if (!(outfile = strcmp(argv[2], "-") ? fopen(argv[2], "wb") : stdout))
    die("Failed to open stdout for writing.");

  info = vpx_video_reader_get_info(reader);

  scale = (int)strtol(argv[4], NULL, 0);
  if (!vpx_img_alloc(&raw, VPX_IMG_FMT_I420, info->frame_width * scale,
                     info->frame_height * scale, 1)) {
    die("Failed to allocate image.");
  }

  if (!(sr_infile = strcmp(argv[3], "-") ? fopen(argv[3], "rb") : stdin))
    die("Failed to open %s for reading.", argv[3]);

  decoder = get_vpx_decoder_by_fourcc(info->codec_fourcc);
  if (!decoder) die("Unknown input codec.");

  fprintf(stderr, "Using %s\n",
          vpx_codec_iface_name(decoder->codec_interface()));

  if (vpx_codec_dec_init(&codec, decoder->codec_interface(), NULL, 0))
    die_codec(&codec, "Failed to initialize decoder.");

  skip = (int)strtol(argv[5], NULL, 0);
  while (vpx_video_reader_read_frame(reader)) {
    vpx_codec_iter_t iter = NULL;
    vpx_image_t *img = NULL;
    size_t frame_size = 0;
    const unsigned char *frame =
        vpx_video_reader_get_frame(reader, &frame_size);
    if (vpx_img_read(&raw, sr_infile) && frame_cnt % skip == 0) {
      fprintf(stderr, "|->");
      if (vpx_codec_set_sr_frame(&codec, &raw, scale))
        die_codec(&codec, "Failed to set super-resolution frame");
    }
    if (vpx_codec_decode(&codec, frame, (unsigned int)frame_size, NULL, 0))
      die_codec(&codec, "Failed to decode frame.");

    while ((img = vpx_codec_get_frame(&codec, &iter)) != NULL) {
      vpx_img_write(img, outfile);
      fprintf(stderr, ".");
      ++frame_cnt;
    }
  }

  if (vpx_codec_destroy(&codec)) die_codec(&codec, "Failed to destroy codec");

  vpx_video_reader_close(reader);

  fclose(outfile);
  
  fprintf(stderr, "\n");

  return EXIT_SUCCESS;
}
