import logging
from skimage.metrics import peak_signal_noise_ratio

from common import parse_args, read_videos

logging.basicConfig(level=logging.INFO)


frames_o, frames_d = read_videos(parse_args())


def psnr(frames1, frames2):
    return [peak_signal_noise_ratio(frames1[i, ...], frames2[i, ...]) for i in range(frames_d.shape[0])]


print(",".join([str(p) for p in psnr(frames_o, frames_d)]))
