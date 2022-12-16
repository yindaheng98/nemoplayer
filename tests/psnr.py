import argparse
import logging
import ffmpeg
import os
import numpy as np
import cv2

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--origin', type=str, required=True, help='Origin video path')
parser.add_argument('--destin', type=str, required=True, help='Proceeded video path')
parser.add_argument('--start', type=int, required=True, help='Start frame index')
parser.add_argument('--frame', type=int, required=True, help='Number of frames')
args = parser.parse_args()
logging.info({
    '--origin': args.origin,
    '--destin': args.destin,
    '--start': args.start,
    '--frame': args.frame,
})


def read_video_meta(path: str):
    path = os.path.expanduser(path)
    capture = cv2.VideoCapture(path)
    n_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    capture.release()
    return width, height, n_frames


width_o, height_o, n_frames_o = read_video_meta(args.origin)
logging.info(f"Origin: {width_o}x{height_o} {n_frames_o}")
width_d, height_d, n_frames_d = read_video_meta(args.destin)
logging.info(f"Destin: {width_d}x{height_d} {n_frames_d}")

print(f"{123},{456}")
