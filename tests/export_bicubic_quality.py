import os
import logging
import argparse
import cv2
import multiprocessing as mp
from skimage.metrics import peak_signal_noise_ratio
from skimage.metrics import structural_similarity

logging.basicConfig(level=logging.INFO)


def task(lq_root, gt_root, video):
    pid = os.getpid()
    length = max([int(os.path.splitext(frame)[0]) for frame in os.listdir(os.path.join(lq_root, video))])
    psnr, ssim = [0] * length, [0] * length
    for frame in os.listdir(os.path.join(lq_root, video)):
        lq_path = os.path.join(lq_root, video, frame)
        gt_path = os.path.join(gt_root, video, frame)
        try:
            lq = cv2.cvtColor(cv2.imread(lq_path, cv2.IMREAD_UNCHANGED), cv2.COLOR_YUV2BGR_I420)
            gt = cv2.cvtColor(cv2.imread(gt_path, cv2.IMREAD_UNCHANGED), cv2.COLOR_YUV2BGR_I420)
            hr = cv2.resize(lq, dsize=(gt.shape[1], gt.shape[0]), interpolation=cv2.INTER_CUBIC)
            print(f"Process{pid:02d}", gt_path)
            frame_i = int(os.path.splitext(frame)[0])
            psnr[frame_i - 1] = peak_signal_noise_ratio(hr, gt)
            ssim[frame_i - 1] = structural_similarity(hr, gt, channel_axis=-1)
        except Exception as e:
            print(e)
    return psnr, ssim


if __name__ == '__main__':

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

    mp.set_start_method('spawn')
    pool = mp.Pool(32)
    videos = os.listdir(args.lq)
    results = {video: pool.apply_async(task, (args.lq, args.gt, video)) for video in videos}

    psnr_path = os.path.join(args.datadir, "psnr.csv")
    ssim_path = os.path.join(args.datadir, "ssim.csv")
    with open(psnr_path, "a+", encoding='utf8') as psnr_f, open(ssim_path, "a+", encoding='utf8') as ssim_f:
        for video in videos:
            psnr, ssim = results[video].get()
            psnr_f.write(f"{video},{','.join(str(frame) for frame in psnr)}\n")
            ssim_f.write(f"{video},{','.join(str(frame) for frame in ssim)}\n")
