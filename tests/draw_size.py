import sys
import os
import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt

log_yscale = True  # Config here

savedir = os.path.join(os.path.dirname(sys.argv[0]), "figures")
os.makedirs(savedir, exist_ok=True)

path = sys.argv[1]
data = pd.read_csv(path)
print(data)

path_full = sys.argv[2]
data_full = {}
with open(path_full, "r", encoding="utf8") as f:
    for line in f.readlines():
        row = line.split(",")
        data_full[row[0]] = [int(d)for d in row[1:]]

for video in data["video"].drop_duplicates():
    video_data = data[data["video"] == video]
    print(video_data)
    fig, ax = plt.subplots(figsize=(18, 6), dpi=600)

    if video in data_full:
        full = data_full[video]
        print(full)
        ax.plot(list(range(len(full))), full, color="r", linewidth=0.5)

    frame = video_data.shape[1]-3
    cmap = mpl.cm.get_cmap('viridis', frame)
    norm = mpl.colors.BoundaryNorm(list(range(1, frame+1)), frame)

    kframe_x, kframe_y = [], []
    for i in range(len(video_data)):
        clip_data = video_data.iloc[i]
        start = clip_data['start']
        frame = len(clip_data) - 3
        clip_x = [start + j for j in range(1, frame+1)]
        clip_y = [clip_data[str(j)] for j in range(1, frame+1)]
        if log_yscale:
            ax.scatter(clip_x, clip_y, s=1, c=[cmap(i) for i in np.linspace(0, 1, frame)])
        else:
            ax.plot(clip_x, clip_y, color="royalblue", linewidth=0.5)
        kframe_x.append(start)
        kframe_y.append(clip_data[str(0)])

    if log_yscale:
        fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)

    kframe_sort = np.argsort(kframe_x)
    kframe_x, kframe_y = np.array(kframe_x)[kframe_sort], np.array(kframe_y)[kframe_sort]
    ax.plot(kframe_x, kframe_y, color="r", linewidth=1)

    if log_yscale:
        plt.yscale("log")
    plt.ylim(10, 100000 if log_yscale else 80000)
    fig.savefig(os.path.join(savedir, video+"."+os.path.basename(path)+(".log_yscale" if log_yscale else "")+".png"))
    plt.close(fig)
