#!/bin/sh -x

make player-clean
make player

VIDEOPATH=$1 # 原始高清视频路径（读取）
SMALLPATH=$2 # 原始高清视频经缩放后视频路径（写入）
DSTPATH=$3   # 缩放后视频经nemo还原的视频路径（写入）
SCALE=$4     # 缩放倍率
SKIP=$5      # nemo还原时跳帧间隔

eval $(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of default=nw=1 $VIDEOPATH) # 获取原始视频尺寸
small_width=$(($width / $SCALE))                                                                           # 计算缩放后的尺寸
small_height=$(($height / $SCALE))                                                                         # 计算缩放后的尺寸

ffmpeg -i $VIDEOPATH -s ${small_width}x${small_height} -v quiet -vcodec rawvideo -f rawvideo -pix_fmt yuv420p pipe:1 | # 原始视频缩放后转rawvideo
    ./build/vpxenc --ivf --passes=1 -w $small_width -h $small_height -o $SMALLPATH -                                   # 输入给vpxenc编码为IVF文件

ffmpeg -i $VIDEOPATH -v quiet -vcodec rawvideo -f rawvideo -pix_fmt yuv420p -vf "select=not(mod(n\,$SKIP))" pipe:1 |                            # 原始视频转rawvideo作为高清低帧率输入
    ./player $SMALLPATH - - $SCALE $SKIP |                                                                                                      # player程序：从文件读低清高帧率视频；从stdin读高清低帧率视频；高清高帧率视频输出到stdout
    ffmpeg -framerate 30 -video_size ${width}x${height} -pixel_format yuv420p -f rawvideo -i pipe:0 -v quiet -c:v libx264 -preset slow -qp 0 -y $DSTPATH # 编码为MP4写入文件，方便看
