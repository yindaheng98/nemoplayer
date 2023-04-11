import os
import logging
import argparse
import ffmpeg

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--videos', type=str, required=True, help='Path of the videos')
parser.add_argument('--datadir', type=str, required=True, help='Dir for export data')


args = parser.parse_args()
logging.info({
    '--videos': args.videos,
    '--datadir': args.datadir,
})
os.makedirs(args.datadir, exist_ok=True)

for file in os.listdir(args.videos):
    path = os.path.join(args.videos, file)
    name = os.path.splitext(file)[0]

    print(name)
    probe = ffmpeg.probe(path, show_frames=None)

    sz_path = os.path.join(args.datadir, "size.csv")
    with open(sz_path, "a+", encoding='utf8') as f:
        f.write(f"{name},{','.join(str(frame['pkt_size']) for frame in probe['frames'])}\n")
        
    kf_path = os.path.join(args.datadir, "keyframe.csv")
    with open(kf_path, "a+", encoding='utf8') as f:
        f.write(f"{name},{','.join(str(frame['key_frame']) for frame in probe['frames'])}\n")
