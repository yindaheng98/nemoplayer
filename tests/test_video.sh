#!/bin/sh -x

ORIGIPATH=$1
SMALLDIR=$2 # 原始高清视频经裁剪缩放后视频文件夹路径（写入）
DSTINDIR=$3 # 缩放后视频经nemo还原的视频文件夹路径（写入）
SCALE=$4    # 缩放倍率
FRAME=$5    # 帧序列长度

eval $(ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=nb_read_frames -of default=nw=1 $ORIGIPATH) # 获取原始视频帧数
MAXSTART=$(($nb_read_frames - $FRAME))
for ((START = 0; START < $MAXSTART; START++)); do
    SMALLPATH="$SMALLDIR/$(basename $ORIGIPATH)"
    DSTINPATH="$SMALLPATH"
    END=$(($START + $FRAME - 1))
    SUFFIX="$START-$END"
    echo $ORIGIPATH $SMALLPATH.$SUFFIX $DSTINPATH.$SUFFIX $SCALE $START $FRAME
done
