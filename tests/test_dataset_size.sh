#!/bin/sh -x

ORIGIDIR=$1
SMALLDIR=$2 # 原始高清视频经裁剪缩放后视频文件夹路径（写入）
SCALE=$3 # 缩放倍率

TESTSIZE="$(dirname $0)/size_video.sh"
if [ $DRYRUN ]; then
    TESTSIZE="echo $TESTSIZE"
fi
for ORIGIPATH in "$ORIGIDIR"/*; do
    $TESTSIZE $ORIGIPATH "$SMALLDIR/$(basename $ORIGIPATH)" $SCALE
done
