import os
import logging
import argparse
import ffmpeg

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--name', type=str, required=True, help='Name of the video')
parser.add_argument('--small', type=str, required=True, help='Small video path')
parser.add_argument('--datadir', type=str, required=True, help='Dir for data')


args = parser.parse_args()
logging.info({
    '--name': args.name,
    '--small': args.small,
    '--datadir': args.datadir,
})

probe = ffmpeg.probe(args.small, show_frames=None)

sz_path = os.path.join(args.datadir, "size_full.csv")
with open(sz_path, "a+", encoding='utf8') as f:
    f.write(f"{args.name},{','.join(str(frame['pkt_size']) for frame in probe['frames'])}\n")
    
kf_path = os.path.join(args.datadir, "keyframe_full.csv")
with open(kf_path, "a+", encoding='utf8') as f:
    f.write(f"{args.name},{','.join(str(frame['key_frame']) for frame in probe['frames'])}\n")
