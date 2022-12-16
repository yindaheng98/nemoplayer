import logging
import numpy as np

from common import parse_args, read_videos

logging.basicConfig(level=logging.INFO)


frames_o, frames_d = read_videos(parse_args())


def psnr(img1, img2):
    dif = (img1 - img2) ** 2
    mse = np.mean(dif.reshape(dif.shape[0], -1), axis=1)
    psnr = 20 * np.log10(255.0 / np.sqrt(mse))
    return psnr


print(",".join([str(p) for p in psnr(frames_o, frames_d).tolist()]))
