import argparse
import logging
import torch
from piq import psnr, ssim

from common import read_videos, data_append, read_video_meta, read_video_sequence
from quality import quality

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--name', type=str, required=True, help='Name of the video')
parser.add_argument('--origin', type=str, required=True, help='Origin video path')
parser.add_argument('--destin', type=str, required=True, help='Proceeded video path')
parser.add_argument('--datadir', type=str, required=True, help='Dir for data')


def read_videos(args, start, frame):

    width_o, height_o, n_frames_o = read_video_meta(args.origin)
    logging.info(f"Origin: {width_o}x{height_o} {n_frames_o}")
    width_d, height_d, n_frames_d = read_video_meta(args.destin)
    logging.info(f"Destin: {width_d}x{height_d} {n_frames_d}")
    assert width_o == width_d and height_o == height_d and args.frame == n_frames_d and args.start + args.frame <= n_frames_o

    frames_o = read_video_sequence(args.origin, start, frame, width_o, height_o)
    logging.info(f"Origin frames shape: {frames_o.shape}")

    frames_d = read_video_sequence(args.destin, start, frame, width_d, height_d)
    logging.info(f"Destin frames shape: {frames_d.shape}")

    return frames_o, frames_d

def quality_long(args, batch_size):

    width_o, height_o, n_frames_o = read_video_meta(args.origin)
    logging.info(f"Origin: {width_o}x{height_o} {n_frames_o}")
    width_d, height_d, n_frames_d = read_video_meta(args.destin)
    logging.info(f"Destin: {width_d}x{height_d} {n_frames_d}")
    assert width_o == width_d and height_o == height_d and n_frames_o == n_frames_d
    
    n_frames = n_frames_o
    psnrs, ssims = [], []
    for start in range(0, n_frames, batch_size):
        frame = min(batch_size, n_frames - start)

        frames_o = read_video_sequence(args.origin, start, frame, width_o, height_o)
        logging.info(f"Origin frames shape: {frames_o.shape}")

        frames_d = read_video_sequence(args.destin, start, frame, width_d, height_d)
        logging.info(f"Destin frames shape: {frames_d.shape}")
        
        psnr_, ssim_ = quality(frames_o, frames_d)
        psnrs.extend(psnr_)
        ssims.extend(ssim_)
        print(psnr_)
        print(ssim_)
    print(psnrs)
    print(ssims)
    return psnrs, ssims
    

if __name__ == "__main__":
    args = parser.parse_args()
    psnr_, ssim_ = quality_long(args, batch_size=16)
