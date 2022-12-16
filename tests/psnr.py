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
assert width_o == width_d and height_o == height_d and args.frame == n_frames_d and args.start + args.frame <= n_frames_o


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


frames_o = read_video_sequence(args.origin, args.start, args.frame, width_o, height_o)
logging.info(f"Origin frames shape: {frames_o.shape}")


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


frames_d = read_video_sequence_all(args.destin, width_d, height_d)
logging.info(f"Destin frames shape: {frames_d.shape}")


def psnr(img1, img2):
    dif = (img1 - img2) ** 2
    mse = np.mean(dif.reshape(dif.shape[0], -1), axis=1)
    psnr = 20 * np.log10(255.0 / np.sqrt(mse))
    return psnr


print(",".join([str(p) for p in psnr(frames_o, frames_d).tolist()]))
