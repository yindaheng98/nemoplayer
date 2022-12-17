import logging
from skimage.metrics import peak_signal_noise_ratio

from common_bicubic import parse_args, read_videos_bicubic

logging.basicConfig(level=logging.INFO)


frames_o, frames_b = read_videos_bicubic(parse_args())


def psnr(frames1, frames2):
    return [peak_signal_noise_ratio(frames1[i, ...], frames2[i, ...]) for i in range(frames2.shape[0])]


print(",".join([str(p) for p in psnr(frames_o, frames_b)]))
