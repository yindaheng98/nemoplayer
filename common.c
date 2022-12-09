#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "vpx/vpx_decoder.h"
#include "vpx_ports/mem_ops.h"

#include "./common.h"

static const char *const kIVFSignature = "DKIF";

VpxVideoReader *vpx_video_reader_open_stdin() {
  char header[32];
  VpxVideoReader *reader = NULL;
  FILE *const file = stdin;
  if (!file) return NULL;  // Can't open file

  if (fread(header, 1, 32, file) != 32) return NULL;  // Can't read file header

  if (memcmp(kIVFSignature, header, 4) != 0)
    return NULL;  // Wrong IVF signature

  if (mem_get_le16(header + 4) != 0) return NULL;  // Wrong IVF version

  reader = calloc(1, sizeof(*reader));
  if (!reader) return NULL;  // Can't allocate VpxVideoReader

  reader->file = file;
  reader->info.codec_fourcc = mem_get_le32(header + 8);
  reader->info.frame_width = mem_get_le16(header + 12);
  reader->info.frame_height = mem_get_le16(header + 14);
  reader->info.time_base.numerator = mem_get_le32(header + 16);
  reader->info.time_base.denominator = mem_get_le32(header + 20);

  return reader;
};

void error(const char *msg) { fprintf(stderr, msg); }

void error_codec(vpx_codec_ctx_t *ctx, const char *s) {
  const char *detail = vpx_codec_error_detail(ctx);

  printf("%s: %s\n", s, vpx_codec_error(ctx));
  if (detail) fprintf("    %s\n", detail);
};

void init(Player *player, const VpxVideoInfo *info, vpx_img_fmt_t img_fmt,
          int scale) {
  const VpxInterface *decoder = NULL;

  if (!vpx_img_alloc(&player->raw, img_fmt, info->frame_width * scale,
                     info->frame_height * scale, 1))
    error("Failed to allocate image.");

  decoder = get_vpx_decoder_by_fourcc(info->codec_fourcc);
  if (!decoder) error("Unknown input codec.");

  fprintf(stderr, "Using %s\n",
          vpx_codec_iface_name(decoder->codec_interface()));

  if (vpx_codec_dec_init(&player->codec, decoder->codec_interface(), NULL, 0))
    error_codec(&player->codec, "Failed to initialize decoder.");
};