import logging
import cv2
import numpy as np
from common import parser, read_video_meta, read_video_sequence, read_video_sequence_all

logging.basicConfig(level=logging.INFO)


parser.add_argument('--scale', type=int, required=True, help='Scale for bicubic')


def parse_args():
    args = parser.parse_args()
    logging.info({
        '--origin': args.origin,
        '--destin': args.destin,
        '--start': args.start,
        '--frame': args.frame,
        '--scale': args.scale,
    })
    return args


def read_videos_bicubic(args):

    width_o, height_o, n_frames_o = read_video_meta(args.origin)
    logging.info(f"Origin: {width_o}x{height_o} {n_frames_o}")
    width_d, height_d, n_frames_d = read_video_meta(args.destin)
    logging.info(f"Destin: {width_d}x{height_d} {n_frames_d}")
    assert width_o == width_d*args.scale and height_o == height_d * \
        args.scale and args.frame == n_frames_d and args.start + args.frame <= n_frames_o

    frames_o = read_video_sequence(args.origin, args.start, args.frame, width_o, height_o)
    logging.info(f"Origin frames shape: {frames_o.shape}")

    frames_d = read_video_sequence_all(args.destin, width_d, height_d)
    logging.info(f"Destin frames shape: {frames_d.shape}")

    frames_b = np.stack([
        cv2.resize(frames_d[i, ...], dsize=(0, 0), fx=args.scale, fy=args.scale, interpolation=cv2.INTER_CUBIC) for i in range(frames_d.shape[0])
    ])
    logging.info(f"Bicubi frames shape: {frames_b.shape}")

    return frames_o, frames_b
