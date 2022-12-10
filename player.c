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

int main(int argc, char **argv) {
  Player player;
  int frame_cnt = 0;
  FILE *outfile = NULL;
  VpxVideoReader *reader = NULL;
  const VpxVideoInfo *info = NULL;

  FILE *sr_infile = NULL;
  int scale;
  int skip;

  exec_name = argv[0];

  if (argc != 6) die("Invalid number of arguments.");

  reader = strcmp(argv[1], "-") ? vpx_video_reader_open(argv[1])
                                : vpx_video_reader_open_stdin(argv[1]);
  if (!reader) die("Failed to open stdin for reading.");
  if (!(outfile = strcmp(argv[2], "-") ? fopen(argv[2], "wb") : stdout))
    die("Failed to open stdout for writing.");
  if (!(sr_infile = strcmp(argv[3], "-") ? fopen(argv[3], "rb") : stdin))
    die("Failed to open %s for reading.", argv[3]);
  scale = (int)strtol(argv[4], NULL, 0);
  skip = (int)strtol(argv[5], NULL, 0);

  info = vpx_video_reader_get_info(reader);

  if (init(&player, info, VPX_IMG_FMT_I420, scale))
    die("Failed to initialize decoder.");

  while (vpx_video_reader_read_frame(reader)) {
    size_t sr_frame_buf_data_sz = get_sr_frame_buf_data_sz(&player);
    unsigned char *sr_frame_buf = (unsigned char *)malloc(sr_frame_buf_data_sz);
    unsigned char *rs_frame_buf = (unsigned char *)malloc(sr_frame_buf_data_sz);
    size_t frame_size = 0;
    const unsigned char *frame =
        vpx_video_reader_get_frame(reader, &frame_size);
    if (frame_cnt % skip == 0) {
      if (fread(sr_frame_buf, 1, sr_frame_buf_data_sz, sr_infile) !=
          sr_frame_buf_data_sz)
        die("Failed to read super-resolution frame");
      fprintf(stderr, "|");
      if (set_sr_frame(&player, sr_frame_buf, scale))
        die("Failed to set super-resolution frame");
    }
    if (decode(&player, frame, (unsigned int)frame_size, NULL, 0))
      die("Failed to decode frame.");

    while (get_frame(&player, rs_frame_buf) == VPX_CODEC_OK) {
      fwrite(rs_frame_buf, 1, sr_frame_buf_data_sz, outfile);
      fprintf(stderr, ".");
      ++frame_cnt;
    }
  }

  if (destory(&player)) die("Failed to destroy codec");

  vpx_video_reader_close(reader);

  fclose(outfile);

  fprintf(stderr, "\n");

  return EXIT_SUCCESS;
}
