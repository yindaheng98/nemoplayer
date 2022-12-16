#!/bin/sh -x

ORIGIPATH=$1 # 原始完整视频路径（读取）
SMALLPATH=$2 # 裁剪后视频路径（写入）
SCALE=$3     # 缩放倍率
START=$4     # 从哪开始剪
FRAME=$5     # 剪多少帧

mkdir -p $(dirname $SMALLPATH)

eval $(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of default=nw=1 $ORIGIPATH) # 获取原始视频尺寸
small_width=$(($width / $SCALE))                                                                           # 计算缩放后的尺寸
small_height=$(($height / $SCALE))                                                                         # 计算缩放后的尺寸
SIZEARG="${small_width}x${small_height}"

ENCODER="$(dirname $0)/../build/vpxenc"
FFMPEG="ffmpeg -v quiet -y"
RAWARG="-f rawvideo -pix_fmt yuv420p"
END=$(($START + $FRAME - 1))
$FFMPEG -i $ORIGIPATH -s $SIZEARG -vcodec rawvideo $RAWARG -vf select="between(n\,$START\,$END),setpts=PTS-STARTPTS" -vsync vfr pipe:1 | # 原始视频缩放后转rawvideo
    $ENCODER --ivf --passes=1 -w $small_width -h $small_height -o $SMALLPATH -                                                           # 输入给vpxenc编码为IVF文件
