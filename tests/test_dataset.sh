#!/bin/sh -x

ORIGIDIR=$1
SMALLDIR=$2 # 原始高清视频经裁剪缩放后视频文件夹路径（写入）
DSTINDIR=$3 # 缩放后视频经nemo还原的视频文件夹路径（写入）
SCALE=$4    # 缩放倍率
FRAME=$5    # 帧序列长度

TESTVIDEO="$(dirname $0)/test_video.sh"
for ORIGIPATH in "$ORIGIDIR"/*; do
    $TESTVIDEO $ORIGIPATH $SMALLDIR $DSTINDIR $SCALE $FRAME
done
