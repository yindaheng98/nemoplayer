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
export DRYRUN=1
./tests/test_dataset.sh ~/datasets/ugc/youtube ~/datasets/ugc/tests ~/datasets/ugc/tests 4 16 > ./tasks.sh
python3 ./tests/runner.py --tasks ./tasks.sh
./tests/test_clip_headers.sh 16 > psnr.csv
cat psnr_*.csv >> psnr.csv
./tests/test_clip_headers.sh 16 > ssim.csv
cat ssim_*.csv >> ssim.csv
./tests/test_clip_headers.sh 16 > psnr_b.csv
cat psnr_b_*.csv >> psnr_b.csv
./tests/test_clip_headers.sh 16 > ssim_b.csv
cat ssim_b_*.csv >> ssim_b.csv
./tests/test_clip_headers.sh 16 > size.csv
cat size_*.csv >> size.csv
```

## Draw quality

```sh
python3 ./tests/draw.py psnr.csv
python3 ./tests/draw.py size.csv
```