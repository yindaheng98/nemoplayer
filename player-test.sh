#!/bin/sh
VIDEOPATH=$1
ffmpeg -i $VIDEOPATH -v quiet -vcodec libvpx-vp9 -f ivf pipe:1 | ./player