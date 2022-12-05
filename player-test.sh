#!/bin/sh
VIDEOPATH=$1
DSTPATH=$2
eval `ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of default=nw=1 $VIDEOPATH`
ffmpeg -i $VIDEOPATH -v quiet -vcodec rawvideo -f rawvideo -pix_fmt yuv420p pipe:1 | \
./build/vpxenc --ivf --passes=1 -w $width -h $height -o - - | \
./player > $DSTPATH
