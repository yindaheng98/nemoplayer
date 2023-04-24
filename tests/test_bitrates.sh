#!/bin/bash

ORIGIDIR=$1 # 原始完整视频路径（读取）
DSTINDIR=$2 # 原始高清视频经低码率转码后视频文件夹路径（写入）
BITRATE=$3  # 码率

QRUN="$(dirname $0)/test_bitrate_quality.sh"
for video in $(ls $ORIGIDIR); do
    if [ -f $ORIGIDIR/$video ]; then
        echo $QRUN $ORIGIDIR/$video $DSTINDIR $BITRATE
    fi
done
