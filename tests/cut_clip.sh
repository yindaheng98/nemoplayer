#!/bin/sh -x

ORIGPATH=$1 # 原始完整视频路径（读取）
CLIPPATH=$2 # 裁剪后视频路径（写入）
START=$3    # 从哪开始剪
FRAME=$4    # 剪多少帧

mkdir -p $(dirname $CLIPPATH)

END=$(($START + $FRAME))
ffmpeg -i $ORIGPATH -vf select="between(n\,$START\,$END),setpts=PTS-STARTPTS" -vsync vfr $CLIPPATH
