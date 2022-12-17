import sys
import os
import pandas as pd
from matplotlib import pyplot as plt

savedir = os.path.join(os.path.dirname(sys.argv[0]), "figures")
os.makedirs(savedir, exist_ok=True)

path = sys.argv[1]
data = pd.read_csv(path)
print(data)
for video in data["video"].drop_duplicates():
    video_data = data[data["video"] == video]
    print(video_data)
    fig, ax = plt.subplots(figsize=(12, 6))
    for i in range(len(video_data)):
        clip_data = video_data.iloc[i]
        start = clip_data['start']
        frame = len(clip_data) - 3
        clip_x = [start + j for j in range(1, frame+1)]
        clip_y = [clip_data[str(j)] for j in range(1, frame+1)]
        ax.plot(clip_x, clip_y, color="royalblue", linewidth=0.5)
    fig.savefig(os.path.join(savedir, video+".png"))
    plt.close(fig)
