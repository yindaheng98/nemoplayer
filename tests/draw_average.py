import sys
import os
import pandas as pd
from matplotlib import pyplot as plt
from draw import savedir

def draw(ax, video_data, **kwargs):
        frame = len(video_data.columns) - 3
        clip_data = video_data.loc[:, [str(i) for i in range(1, frame+1)]]
        clip_x = list(range(1, frame+1))
        clip_y = clip_data.mean()
        ax.plot(clip_x, clip_y, **kwargs)

if __name__ == "__main__":

    path0 = sys.argv[1]
    print("Reading:", path0)
    data0 = pd.read_csv(path0)
    print(data0)
    path1 = sys.argv[2]
    print("Reading:", path1)
    data1 = pd.read_csv(path1)
    print(data1)
    minimum = int(sys.argv[3])
    maximum = int(sys.argv[4])
    print("Range:", [minimum, maximum])

    video_data0 = data0
    video_data1 = data1
    print(video_data0)
    print(video_data1)
    fig, ax = plt.subplots(figsize=(12, 6))
    draw(ax, video_data0, color="royalblue", linewidth=0.5)
    draw(ax, video_data1, color="lightcoral", linewidth=0.5)
    plt.ylim(minimum, maximum)
    fig.savefig(os.path.join(savedir, f"{os.path.basename(path0)}.{os.path.basename(path1)}.png"))
    plt.close(fig)
