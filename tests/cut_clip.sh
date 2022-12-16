#!/bin/sh -x

ORIGPATH=$1 # 原始完整视频路径（读取）
SMALPATH=$2 # 裁剪后视频路径（写入）
SCALE=$3    # 缩放倍率
START=$4    # 从哪开始剪
FRAME=$5    # 剪多少帧
FFMPEG="ffmpeg -v quiet -y"
RAWARG="-f rawvideo -pix_fmt yuv420p"

mkdir -p $(dirname $SMALPATH)

eval $(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of default=nw=1 $ORIGPATH) # 获取原始视频尺寸
small_width=$(($width / $SCALE))                                                                          # 计算缩放后的尺寸
small_height=$(($height / $SCALE))                                                                        # 计算缩放后的尺寸
SIZEARG="${small_width}x${small_height}"

END=$(($START + $FRAME - 1))
$FFMPEG -i $ORIGPATH -s $SIZEARG -vcodec rawvideo $RAWARG -vf select="between(n\,$START\,$END),setpts=PTS-STARTPTS" -vsync vfr $SMALPATH # 原始视频缩放后转rawvideo
