import logging
import ffmpeg
from skimage.metrics import peak_signal_noise_ratio
from skimage.metrics import structural_similarity

from common import parse_args, read_videos, data_append

logging.basicConfig(level=logging.INFO)

args = parse_args()
frames_o, frames_d, frames_s = read_videos(args)


def psnr(frames1, frames2):
    return [peak_signal_noise_ratio(frames1[i, ...], frames2[i, ...]) for i in range(frames2.shape[0])]


data_append(args=args, data=psnr(frames_o, frames_d), name="psnr")


def ssim(frames1, frames2):
    return [structural_similarity(frames1[i, ...], frames2[i, ...], channel_axis=-1) for i in range(frames2.shape[0])]


data_append(args=args, data=ssim(frames_o, frames_d), name="ssim")
