import logging
import numpy as np

from common import parse_args, read_video_meta, read_video_sequence, read_video_sequence_all

logging.basicConfig(level=logging.INFO)


args = parse_args()


width_o, height_o, n_frames_o = read_video_meta(args.origin)
logging.info(f"Origin: {width_o}x{height_o} {n_frames_o}")
width_d, height_d, n_frames_d = read_video_meta(args.destin)
logging.info(f"Destin: {width_d}x{height_d} {n_frames_d}")
assert width_o == width_d and height_o == height_d and args.frame == n_frames_d and args.start + args.frame <= n_frames_o


frames_o = read_video_sequence(args.origin, args.start, args.frame, width_o, height_o)
logging.info(f"Origin frames shape: {frames_o.shape}")


frames_d = read_video_sequence_all(args.destin, width_d, height_d)
logging.info(f"Destin frames shape: {frames_d.shape}")


def psnr(img1, img2):
    dif = (img1 - img2) ** 2
    mse = np.mean(dif.reshape(dif.shape[0], -1), axis=1)
    psnr = 20 * np.log10(255.0 / np.sqrt(mse))
    return psnr


print(",".join([str(p) for p in psnr(frames_o, frames_d).tolist()]))
