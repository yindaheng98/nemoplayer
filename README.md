# Player

## Build

```sh
git submodule update --init --recursive
git submodule update --remote --recursive
./player-build.sh
make player
```

## Run

```sh
VIDEOROOT=/root/Programs/视频数据
SCALE=4
SKIP=10
FROM=00:01:35
FRAMES=600
./player-test.sh $VIDEOROOT/4K.webm $VIDEOROOT/540p-small.ivf $VIDEOROOT/4K-small-nemo-$SCALE-$SKIP.mp4 $SCALE $SKIP $FROM $FRAMES
```

## Build .so and .a

```sh
make player.so
make player.a
```

## Test quality

```sh
DRYRUN=1 ./tests/test_dataset.sh ~/datasets/ugc/youtube ~/datasets/ugc/tests ~/datasets/ugc/tests 4 16 > ./tasks_quality.sh
python3 ./tests/runner.py --tasks ./tasks_quality.sh
```

## Test quality with ingetrated upscale program

```sh
DRYRUN=1 ./tests/test_dataset.sh ~/datasets/ugc/youtube ~/datasets/ugc/tests ~/datasets/ugc/tests 4 16 > ./tasks_quality.sh
python3 ./tests/runner.py --tasks ./tasks_quality.sh --preprocess "export INTEGRATION='python /path/to/upscale/script.py'"
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

## Test size

```sh
DRYRUN=1 ./tests/test_dataset_size.sh ~/datasets/ugc/youtube ~/datasets/ugc/tests 4 > ./tasks_size.sh
python3 ./tests/runner.py --tasks ./tasks_size.sh
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
```