# Player

```sh
VIDEOROOT=/root/Programs/视频数据
SCALE=4
SKIP=10
FROM=00:01:35
FRAMES=600
./player-test.sh $VIDEOROOT/4K.webm $VIDEOROOT/540p-small.ivf $VIDEOROOT/4K-small-nemo-$SCALE-$SKIP.mp4 $SCALE $SKIP $FROM $FRAMES
```