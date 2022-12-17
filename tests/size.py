import logging
import argparse
import ffmpeg

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--video', type=str, required=True, help='Video to be count')
parser.add_argument('--frame', type=int, required=True, help='Number of frames')

args = parser.parse_args()
probe = ffmpeg.probe(args.video, show_frames=None)
print(",".join([str(frame['pkt_size']) for frame in probe['frames']]))
