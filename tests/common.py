import argparse
import logging
import ffmpeg
import os
import numpy as np
import cv2

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--name', type=str, required=True, help='Name of the video')
parser.add_argument('--origin', type=str, required=True, help='Origin video path')
parser.add_argument('--destin', type=str, required=True, help='Proceeded video path')
parser.add_argument('--small', type=str, required=True, help='Small video path')
parser.add_argument('--start', type=int, required=True, help='Start frame index')
parser.add_argument('--frame', type=int, required=True, help='Number of frames')
parser.add_argument('--scale', type=int, required=True, help='Scale for bicubic')
parser.add_argument('--datadir', type=str, required=True, help='Dir for data')


def parse_args():
    args = parser.parse_args()
    logging.info({
        '--name': args.name,
        '--origin': args.origin,
        '--destin': args.destin,
        '--small': args.small,
        '--start': args.start,
        '--frame': args.frame,
        '--scale': args.scale,
        '--datadir': args.datadir,
    })
    return args


def read_video_meta(path: str):
    path = os.path.expanduser(path)
    capture = cv2.VideoCapture(path)
    n_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    capture.release()
    return width, height, n_frames


def read_video_sequence(path: str, start: int, frame: int, width: int, height: int, pix_fmt='bgr24'):
    path = os.path.expanduser(path)
    process = (ffmpeg
               .input(path, loglevel="error")
               .trim(start_frame=start, end_frame=start+frame)
               .setpts('PTS-STARTPTS')
               .output('pipe:', format='rawvideo', pix_fmt=pix_fmt)
               .run_async(pipe_stdout=True, pipe_stderr=False))
    out, err = process.communicate()
    if err:
        raise err
    return np.frombuffer(out, np.uint8).reshape([-1, height, width, 3])


def read_video_sequence_all(path: str, width: int, height: int, pix_fmt='bgr24'):
    path = os.path.expanduser(path)
    process = (ffmpeg
               .input(path, loglevel="error")
               .output('pipe:', format='rawvideo', pix_fmt=pix_fmt)
               .run_async(pipe_stdout=True, pipe_stderr=False))
    out, err = process.communicate()
    if err:
        raise err
    return np.frombuffer(out, np.uint8).reshape([-1, height, width, 3])


def read_videos(args):

    width_o, height_o, n_frames_o = read_video_meta(args.origin)
    logging.info(f"Origin: {width_o}x{height_o} {n_frames_o}")
    width_d, height_d, n_frames_d = read_video_meta(args.destin)
    logging.info(f"Destin: {width_d}x{height_d} {n_frames_d}")
    assert width_o == width_d and height_o == height_d and args.frame == n_frames_d and args.start + args.frame <= n_frames_o

    frames_o = read_video_sequence(args.origin, args.start, args.frame, width_o, height_o)
    logging.info(f"Origin frames shape: {frames_o.shape}")

    frames_d = read_video_sequence_all(args.destin, width_d, height_d)
    logging.info(f"Destin frames shape: {frames_d.shape}")

    frames_s = read_video_sequence_all(args.small, width_d // args.scale, height_d // args.scale)
    logging.info(f"Lowres frames shape: {frames_s.shape}")

    return frames_o, frames_d, frames_s


def data_append(args, name, data):
    assert len(data) == args.frame
    path = os.path.join(args.datadir, name + ".csv")
    with open(path, "a+", encoding='utf8') as f:
        f.write(f"{args.name},{args.start},{','.join(str(d) for d in data)}\n")
