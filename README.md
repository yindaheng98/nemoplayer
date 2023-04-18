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
python tests/prepare_dataset.py 4 $VIDEOROOT
python tests/prepare_dataset.py 4 $VIDEOROOT lossless --lossless=1
```

```sh
VIDEOROOT=~/dataset/ugc-dataset/original_videos_h264
python tests/prepare_dataset.py 4 $VIDEOROOT
python tests/prepare_dataset.py 4 $VIDEOROOT lossless --lossless=1
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

## Build .so and .a

```sh
make player.so
make player.a
```

## Test quality

```sh
rm ./tasks_quality.sh
DRYRUN=1 ./tests/test_dataset.sh ~/dataset/ugc-dataset/vp9_compressed_videos tests/data/temp tests/data/temp 4 16 > ./tasks_quality.sh
python3 ./tests/runner.py --tasks ./tasks_quality.sh
```

## Test quality with ingetrated upscale program

```sh
DRYRUN=1 ./tests/test_dataset.sh ~/dataset/ugc-dataset/vp9_compressed_videos tests/data/temp tests/data/temp 4 16 > ./tasks_quality.sh
python3 ./tests/runner.py --tasks ./tasks_quality.sh --preprocess "export INTEGRATION='python ./tests/integrate_sr.py ~/dataset/ugc-dataset-image/vp9_compressed_videos'"
```

Then your INTEGRATION would be call linke this:

```sh
python /path/to/upscale/script.py /path/to/low/resolution/video.mp4 | some other operation
```

Your `/path/to/upscale/script.py` should read the `/path/to/low/resolution/video.mp4`, upscale the first frame, and pipe the high resolution frame to `stdout`.

For example:

```sh
source /home/seu/FrogSR/venv/bin/activate && python3 ./tests/runner.py --devices 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,31,32 --tasks ./tasks_quality.sh --preprocess "export INTEGRATION='source /home/seu/FrogSR/venv/bin/activate && PYTHONPATH=/home/seu/FrogSR python /home/seu/FrogSR/vrt_server_cli.py --ports 8001,8002,8003,8004,8005,8006,8007,8008 --path'"
```

## Gather data

```sh
./tests/test_clip_headers.sh 16 > psnr.csv
cat ./tests/data/*/psnr.csv >> psnr.csv
./tests/test_clip_headers.sh 16 > ssim.csv
cat ./tests/data/*/ssim.csv >> ssim.csv
./tests/test_clip_headers.sh 16 > psnr_b.csv
cat ./tests/data/*/psnr_b.csv >> psnr_b.csv
./tests/test_clip_headers.sh 16 > ssim_b.csv
cat ./tests/data/*/ssim_b.csv >> ssim_b.csv
./tests/test_clip_headers.sh 16 > size.csv
cat ./tests/data/*/size.csv >> size.csv
cat ./tests/data/*/size_full.csv > size_full.csv
```

## Draw quality

```sh
rm tests/figures/*.size.csv.png
rm tests/figures/*.size.csv.log_yscale.png
cat > ./draw.sh <<EOF
python3 ./tests/draw_compare.py psnr.csv psnr_b.csv 0 100
python3 ./tests/draw_compare.py ssim.csv ssim_b.csv 0 1
python3 ./tests/draw_size.py size.csv size_full.csv
EOF
python3 ./tests/runner.py --devices '1,2,3' --tasks ./draw.sh
rm ./draw.sh
python3 ./tests/draw_average.py psnr.csv psnr_b.csv 0 50
python3 ./tests/draw_average.py ssim.csv ssim_b.csv 0.5 1
```