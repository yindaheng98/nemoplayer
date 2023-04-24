import argparse
import logging
import os
import ffmpeg

from common import read_video_meta, read_video_sequence
from quality import quality

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
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
        name = os.path.splitext(os.path.basename(args.destin))[0]
        print(name, start, start + frame, psnr_)
        print(name, start, start + frame, ssim_)
    return psnrs, ssims

if __name__ == "__main__":
    args = parser.parse_args()
    name = os.path.splitext(os.path.basename(args.destin))[0]
    
    psnr_, ssim_ = quality_long(args, batch_size=16)
    with open(os.path.join(args.datadir, "psnr.csv"), "a+", encoding='utf8') as f:
        f.write(f"{name},{','.join(str(d) for d in psnr_)}\n")
    with open(os.path.join(args.datadir, "ssim.csv"), "a+", encoding='utf8') as f:
        f.write(f"{name},{','.join(str(d) for d in ssim_)}\n")
    
    probe = ffmpeg.probe(args.destin, show_frames=None)
    with open(os.path.join(args.datadir, "size.csv"), "a+", encoding='utf8') as f:
        f.write(f"{name},{','.join(str(frame['pkt_size']) for frame in probe['frames'])}\n")
    with open(os.path.join(args.datadir, "keyframe.csv"), "a+", encoding='utf8') as f:
        f.write(f"{name},{','.join(str(frame['key_frame']) for frame in probe['frames'])}\n")
