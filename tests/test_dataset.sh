#!/bin/bash -x

ORIGIDIR=$1
SMALLDIR=$2 # 原始高清视频经裁剪缩放后视频文件夹路径（写入）
DSTINDIR=$3 # 缩放后视频经nemo还原的视频文件夹路径（写入）
SCALE=$4    # 缩放倍率
FRAME=$5    # 帧序列长度

TESTVIDEO="$(dirname $0)/test_video.sh"
TESTCLIP="$(dirname $0)/test_clip.sh"
if [ $DRYRUN ]; then
    TESTCLIP="echo $TESTCLIP"
fi
for ORIGIPATH in "$ORIGIDIR"/*; do
    eval $(ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of default=nw=1 $ORIGIPATH) # 获取原始视频帧数
    MAXSTART=$(($nb_read_packets - $FRAME))
    for ((START = 0; START < $MAXSTART; START++)); do
        SMALLPATH="$SMALLDIR/$(basename $ORIGIPATH)"
        DSTINPATH="$SMALLPATH"
        SUFFIX="$START+$FRAME"
        $TESTCLIP $ORIGIPATH $SMALLPATH.$SUFFIX $DSTINPATH.$SUFFIX $SCALE $START $FRAME
    done
done
