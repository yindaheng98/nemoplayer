#!/bin/bash

ORIGIPATH=$1 # 原始完整视频路径（读取）
DSTINDIR=$2 # 原始高清视频经低码率转码后视频文件夹路径（写入）
BITRATE=$3   # 码率
DSTINPATH="$DSTINDIR"/$(basename $ORIGIPATH).ivf
mkdir -p "$DSTINDIR"

FFMPEG="ffmpeg -y"
$FFMPEG -i $ORIGIPATH -vcodec libvpx-vp9 -b:v $BITRATE -an -sn $DSTINPATH

QRUN="$(dirname $0)/quality_long.py"
DATADIR=$(dirname $0)/data/$NAME/$TASKID/$BITRATE
mkdir -p $DATADIR
PYTHONPATH=$(dirname $0) CUDA_VISIBLE_DEVICES=$DEVICE python3 $QRUN --origin $ORIGIPATH --destin $DSTINPATH --datadir $DATADIR

rm $DSTINPATH