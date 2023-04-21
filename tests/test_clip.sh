#!/bin/bash -x

ORIGIPATH=$1     # 原始完整视频路径（读取）
SMALLPATH=$2.ivf # 原始高清视频经裁剪缩放后视频路径（写入）
DSTINPATH=$3.mp4 # 缩放后视频经nemo还原的视频路径（写入）
SCALE=$4         # 缩放倍率
START=$5         # 从哪开始剪
FRAME=$6         # 剪多少帧

mkdir -p $(dirname $SMALLPATH)

eval $(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of default=nw=1 $ORIGIPATH) # 获取原始视频尺寸
small_width=$(($width / $SCALE))                                                                           # 计算缩放后的尺寸
small_height=$(($height / $SCALE))                                                                         # 计算缩放后的尺寸
SIZEARG="${small_width}x${small_height}"

ENCODER="$(dirname $0)/../build/vpxenc"
FFMPEG="ffmpeg -v quiet -y"
RAWARG="-f rawvideo -pix_fmt yuv420p"
END=$(($START + $FRAME - 1))

function down_scale() {
    $FFMPEG -i $ORIGIPATH -s $SIZEARG -vcodec rawvideo $RAWARG -vf select="between(n\,$1\,$2),setpts=PTS-STARTPTS" -vsync vfr pipe:1 | # 原始视频缩放后转rawvideo
        $ENCODER --ivf --lossless=1 --passes=1 -w $small_width -h $small_height -o $3 -                                                # 输入给vpxenc无损编码为IVF文件
}
down_scale $START $END $SMALLPATH # 生成原始视频缩放后IVF文件

PLAYER="$(dirname $0)/../player"
HQVIDEO="$FFMPEG -i $ORIGIPATH -vcodec rawvideo $RAWARG -vf select='eq(n\,$START)' -vsync vfr pipe:1" # 原始视频所选起始帧转rawvideo作为高清低帧率输入
# SMALLPATH_INT=$SMALLPATH.for_integration.ivf
if [ "$INTEGRATION" ]; then
    # START_INT=$(($START - $FRAME + 1)) # 往前取FRAME帧用于计算
    # if [ $START_INT -lt 0 ]; then
    #     rm $SMALLPATH
    #     exit 0
    # fi
    # down_scale $START_INT $START $SMALLPATH_INT # 生成原始视频缩放后IVF文件
    # HQVIDEO="$INTEGRATION $SMALLPATH_INT"       # 用INTEGRATION指定如何生成高清低帧率输入
    HQVIDEO="$INTEGRATION $SMALLPATH" # 用INTEGRATION指定如何生成高清低帧率输入
fi
sh -c "$HQVIDEO" |                                                                                                   # 总之来一个高清低帧率输入
    $PLAYER $SMALLPATH - - $SCALE $FRAME |                                                                           # player程序：从文件读低清高帧率视频；从stdin读高清低帧率视频；高清高帧率视频输出到stdout
    ffmpeg -video_size "${width}x${height}" $RAWARG -i pipe:0 -v quiet -c:v libx264 -preset slow -qp 0 -y $DSTINPATH # 编码为MP4写入文件，方便看
# rm $SMALLPATH_INT

DATADIR=$(dirname $0)/data/$NAME/$TASKID
mkdir -p $DATADIR
QRUN="$(dirname $0)/quality.py"
PYTHONPATH=$(dirname $0) CUDA_VISIBLE_DEVICES=$DEVICE python3 $QRUN --name $(basename $ORIGIPATH) --origin $ORIGIPATH --destin $DSTINPATH --small $SMALLPATH --start $START --frame $FRAME --scale $SCALE --datadir $DATADIR

rm $SMALLPATH
rm $DSTINPATH
