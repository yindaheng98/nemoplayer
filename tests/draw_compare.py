import sys
import os
import pandas as pd
from matplotlib import pyplot as plt
from draw import savedir, draw

if __name__ == "__main__":

    path0 = sys.argv[1]
    print("Reading:", path0)
    data0 = pd.read_csv(path0)
    print(data0)
    path1 = sys.argv[2]
    print("Reading:", path1)
    data1 = pd.read_csv(path1)
    print(data1)

    for video in (set(data0["video"].drop_duplicates()) & set(data1["video"].drop_duplicates())):
        video_data0 = data0[data0["video"] == video]
        video_data1 = data1[data1["video"] == video]
        print(video_data0)
        print(video_data1)
        fig, ax = plt.subplots(figsize=(12, 6))
        draw(ax, video_data0, color="royalblue", linewidth=0.5)
        draw(ax, video_data1, color="lightcoral", linewidth=0.5)
        fig.savefig(os.path.join(savedir, f"{video}.{os.path.basename(path0)}.{os.path.basename(path1)}.png"))
        plt.close(fig)
