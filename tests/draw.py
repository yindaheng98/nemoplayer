import sys
import pandas as pd

path = sys.argv[1]
data = pd.read_csv(path)
print(data)
for video in data["video"].drop_duplicates():
    video_data = data[data["video"] == video]
    print(video_data)
    for i in range(len(video_data)):
        clip_data = video_data.iloc[i]
        start = clip_data['start']
        frame = len(clip_data) - 3
        clip_x = [start + j for j in range(1, frame+1)]
        clip_y = [clip_data[str(j)] for j in range(1, frame+1)]
        print(clip_x)
        print(clip_y)
