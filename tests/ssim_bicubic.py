import logging
from skimage.metrics import structural_similarity

from common_bicubic import parse_args, read_videos_bicubic

logging.basicConfig(level=logging.INFO)


frames_o, frames_b = read_videos_bicubic(parse_args())


def ssim(frames1, frames2):
    return [structural_similarity(frames1[i, ...], frames2[i, ...], multichannel=True) for i in range(frames2.shape[0])]


print(",".join([str(p) for p in ssim(frames_o, frames_b)]))
