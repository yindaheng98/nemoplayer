#include "./video_reader.h"

// VpxVideoReaderStruct is defined in .c
// So must have a VpxVideoReaderStruct here or you can not make a .o.
// Fuck the ugly code!
// One should define a struct in .h rather than .c !!!!!!
struct VpxVideoReaderStruct {
  VpxVideoInfo info;
  FILE *file;
  uint8_t *buffer;
  size_t buffer_size;
  size_t frame_size;
};

VpxVideoReader *vpx_video_reader_open_stdin();

struct PlayerStruct {
  vpx_image_t sr_raw;
  vpx_codec_ctx_t codec;
};

typedef struct PlayerStruct Player;

vpx_codec_err_t init(Player *player, const VpxVideoInfo *info,
                     vpx_img_fmt_t img_fmt, int scale);