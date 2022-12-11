#!/bin/sh -x

ENCODER="$(dirname $0)/../build/vpxenc"
VIDEOPATH=$1 # 原始高清视频路径（读取）
SMALLPATH=$2 # 原始高清视频经缩放后视频路径（写入）
SCALE=$3     # 缩放倍率

eval $(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of default=nw=1 $VIDEOPATH) # 获取原始视频尺寸
small_width=$(($width / $SCALE))                                                                                        # 计算缩放后的尺寸
small_height=$(($height / $SCALE))                                                                                      # 计算缩放后的尺寸

ffmpeg -i $VIDEOPATH -s ${small_width}x${small_height} -v quiet -vcodec rawvideo -f rawvideo -pix_fmt yuv420p pipe:1 | # 原始视频缩放后转rawvideo
    $ENCODER --ivf --passes=1 -w $small_width -h $small_height -o $SMALLPATH -                                         # 输入给vpxenc编码为IVF文件
