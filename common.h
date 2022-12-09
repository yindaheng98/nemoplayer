#include "./video_reader.h"

struct VpxVideoReaderStruct {
  VpxVideoInfo info;
  FILE *file;
  uint8_t *buffer;
  size_t buffer_size;
  size_t frame_size;
};

VpxVideoReader *vpx_video_reader_open_stdin();