# Player

## Update

```sh
git pull
git submodule update --remote --recursive
```

## Build

Before you start please install necessary buildtools according to `libvpx/README`.

```sh
git submodule update --init --recursive
chmod +x R .
./player-build.sh
make player
```

## Download Dataset

```sh
mkdir -p ~/dataset
cd ~/dataset
gsutil ls gs://ugc-dataset/original_videos_h264/*1080P*
mkdir -p ~/dataset/ugc-dataset/original_videos_h264
gsutil cp gs://ugc-dataset/original_videos_h264/*1080P* ~/dataset/ugc-dataset/original_videos_h264
```

## Downsample Video

```sh
VIDEOROOT=~/dataset/ugc-dataset/vp9_compressed_videos
python tests/prepare_videos.py 4 $VIDEOROOT
python tests/prepare_videos.py 4 $VIDEOROOT lossless --lossless=1
```

```sh
VIDEOROOT=~/dataset/ugc-dataset/original_videos_h264
python tests/prepare_videos.py 4 $VIDEOROOT
python tests/prepare_videos.py 4 $VIDEOROOT lossless --lossless=1
```

## Split to images

```sh
VIDEOROOT=~/dataset/ugc-dataset/vp9_compressed_videos
IMAGEROOT=~/dataset/ugc-dataset-image/vp9_compressed_videos
python tests/prepare_images.py $VIDEOROOT $IMAGEROOT
python tests/prepare_images.py "$VIDEOROOT"_x4 "$IMAGEROOT"_x4
python tests/prepare_images.py "$VIDEOROOT"_x4lossless "$IMAGEROOT"_x4lossless
```

```sh
VIDEOROOT=~/dataset/ugc-dataset/original_videos_h264
IMAGEROOT=~/dataset/ugc-dataset-image/original_videos_h264
python tests/prepare_images.py $VIDEOROOT $IMAGEROOT
python tests/prepare_images.py "$VIDEOROOT"_x4 "$IMAGEROOT"_x4
python tests/prepare_images.py "$VIDEOROOT"_x4lossless "$IMAGEROOT"_x4lossless
```

## Test Player

```sh
VIDEOROOT=~/dataset/ugc-dataset/vp9_compressed_videos
VIDEONAME=Gaming_1080P-0ce6_orig
mkdir -p build/results
SCALE=4
SKIP=10
FROM=00:00:00
FRAMES=600
./player-test.sh $VIDEOROOT/$VIDEONAME.mp4 "$VIDEOROOT"_x4lossless/$VIDEONAME.ivf build/results/$VIDEONAME.mp4 $SCALE $SKIP $FROM $FRAMES
```

## Export size of frames

```sh
VIDEOROOT=~/dataset/ugc-dataset/vp9_compressed_videos

rm -rf tests/data/size_x4
PYTHONPATH=tests python3 tests/export_size.py --videos "$VIDEOROOT"_x4 --datadir tests/data/size_x4

rm -rf tests/data/size_x4lossless
PYTHONPATH=tests python3 tests/export_size.py --videos "$VIDEOROOT"_x4lossless --datadir tests/data/size_x4lossless
```

```sh
VIDEOROOT=~/dataset/ugc-dataset/original_videos_h264

rm -rf tests/data/size
PYTHONPATH=tests python3 tests/export_size.py --videos "$VIDEOROOT" --datadir tests/data/size

rm -rf tests/data/size_x4
PYTHONPATH=tests python3 tests/export_size.py --videos "$VIDEOROOT"_x4 --datadir tests/data/size_x4

rm -rf tests/data/size_x4lossless
PYTHONPATH=tests python3 tests/export_size.py --videos "$VIDEOROOT"_x4lossless --datadir tests/data/size_x4lossless
```

## Export bicubic quality

```sh
IMAGEROOT=~/dataset/ugc-dataset-image/original_videos_h264
python3 tests/export_bicubic_quality.py --lq "$IMAGEROOT"_x4lossless --gt "$IMAGEROOT" --datadir tests/data/bicubic_x4lossless
```

## Export quality and size of frames from different bitrates

```sh
VIDEOROOT=~/dataset/ugc-dataset/original_videos_h264
./tests/test_bitrates.sh $VIDEOROOT tests/data/temp 4M > ./tasks_bitrates_quality.sh
./tests/test_bitrates.sh $VIDEOROOT tests/data/temp 2M >> ./tasks_bitrates_quality.sh
./tests/test_bitrates.sh $VIDEOROOT tests/data/temp 1M >> ./tasks_bitrates_quality.sh
./tests/test_bitrates.sh $VIDEOROOT tests/data/temp 512k >> ./tasks_bitrates_quality.sh
./tests/test_bitrates.sh $VIDEOROOT tests/data/temp 256k >> ./tasks_bitrates_quality.sh
python3 ./tests/runner.py --tasks ./tasks_bitrates_quality.sh --shuffle --preprocess "export NAME=bitrates" --devices 0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7
```

```sh
for b in 4M 2M 1M 256k 512k; do
mkdir -p bitrates_$b
cat ./tests/data/bitrates/*/$b/keyframe.csv >> bitrates_$b/keyframe.csv
cat ./tests/data/bitrates/*/$b/size.csv >> bitrates_$b/size.csv
cat ./tests/data/bitrates/*/$b/psnr.csv >> bitrates_$b/psnr.csv
cat ./tests/data/bitrates/*/$b/ssim.csv >> bitrates_$b/ssim.csv
done
```

## Build .so and .a

```sh
make player.so
make player.a
```

## Test quality

```sh
VIDEOROOT=~/dataset/ugc-dataset/original_videos_h264
rm ./tasks_quality.sh
DRYRUN=1 ./tests/test_dataset.sh $VIDEOROOT tests/data/temp tests/data/temp 4 16 > ./tasks_quality.sh
python3 ./tests/runner.py --tasks ./tasks_quality.sh
```

## Generate quality test script

```sh
DRYRUN=1 ./tests/test_dataset.sh ~/dataset/ugc-dataset/vp9_compressed_videos tests/data/temp tests/data/temp 4 16 > ./tasks_quality.sh
```

```sh
DRYRUN=1 ./tests/test_dataset.sh ~/dataset/ugc-dataset/original_videos_h264 tests/data/temp tests/data/temp 4 16 > ./tasks_quality.sh
```

## Test quality with ingetrated upscale program

```sh
python3 ./tests/runner.py --tasks ./tasks_quality.sh --preprocess "export INTEGRATION='python ./tests/integrate_sr.py ~/dataset/ugc-dataset-image/vp9_compressed_videos'"
```

```sh
python3 ./tests/runner.py --tasks ./tasks_quality.sh --preprocess "export INTEGRATION='python ./tests/integrate_sr.py ~/dataset/ugc-dataset-image/original_videos_h264'"
```

Then your INTEGRATION would be call like this:

```sh
python /path/to/upscale/script.py /path/to/low/resolution/video.mp4 | some other operation
```

Your `/path/to/upscale/script.py` should read the `/path/to/low/resolution/video.mp4`, upscale the first frame, and pipe the high resolution frame to `stdout`.

For example:

```sh
python3 ./tests/runner.py --tasks ./tasks_quality.sh --shuffle --preprocess "export INTEGRATION='python ./tests/integrate_sr_rgb.py ~/FrogSR_train/tmp/vrt_test/7' && export NAME=decoder7" --devices 0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3
python3 ./tests/runner.py --tasks ./tasks_quality.sh --shuffle --preprocess "export INTEGRATION='python ./tests/integrate_sr_rgb.py ~/FrogSR_train/tmp/vrt_test/3' && export NAME=decoder3" --devices 4,5,6,7,4,5,6,7,4,5,6,7,4,5,6,7,4,5,6,7,4,5,6,7,4,5,6,7,4,5,6,7
```

## Gather data

```sh
echo "video,start,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15" > psnr7.csv
cat ./tests/data/decoder7/*/psnr.csv >> psnr7.csv

echo "video,start,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15" > ssim7.csv
cat ./tests/data/decoder7/*/ssim.csv >> ssim7.csv

echo "video,start,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15" > psnr3.csv
cat ./tests/data/decoder3/*/psnr.csv >> psnr3.csv

echo "video,start,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15" > ssim3.csv
cat ./tests/data/decoder3/*/ssim.csv >> ssim3.csv
```
