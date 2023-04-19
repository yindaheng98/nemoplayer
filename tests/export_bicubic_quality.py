import os
import logging
import argparse
import cv2
from skimage.metrics import peak_signal_noise_ratio
from skimage.metrics import structural_similarity

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--lq', type=str, required=True, help='Path of the low quality videos')
parser.add_argument('--gt', type=str, required=True, help='Path of the ground truth videos')
parser.add_argument('--datadir', type=str, required=True, help='Dir for export data')


args = parser.parse_args()
logging.info({
    '--lq': args.lq,
    '--gt': args.gt,
    '--datadir': args.datadir,
})
os.makedirs(args.datadir, exist_ok=True)

for video in os.listdir(args.lq):
    length = max([int(os.path.splitext(frame)[0]) for frame in os.listdir(os.path.join(args.lq, video))])
    psnr, ssim = [0] * length, [0] * length
    for frame in os.listdir(os.path.join(args.lq, video)):
        lq_path = os.path.join(args.lq, video, frame)
        gt_path = os.path.join(args.gt, video, frame)
        lq = cv2.cvtColor(cv2.imread(lq_path, cv2.IMREAD_UNCHANGED), cv2.COLOR_YUV2BGR_I420)
        gt = cv2.cvtColor(cv2.imread(gt_path, cv2.IMREAD_UNCHANGED), cv2.COLOR_YUV2BGR_I420)
        hr = cv2.resize(lq, dsize=(gt.shape[1], gt.shape[0]), interpolation=cv2.INTER_CUBIC)
        print(gt_path)
        frame_i = int(os.path.splitext(frame)[0])
        psnr[frame_i - 1] = peak_signal_noise_ratio(hr, gt)
        ssim[frame_i - 1] = structural_similarity(hr, gt, channel_axis=-1)
