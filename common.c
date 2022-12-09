#include <stdio.h>
#include <stdlib.h>
#include <string.h>
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
}