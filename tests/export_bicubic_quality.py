import os
import logging
import argparse
import torch
import cv2
import numpy as np
import multiprocessing as mp
from piq import psnr, ssim

logging.basicConfig(level=logging.INFO)


def task(lq_root, gt_root, video):
    pid = os.getpid()
    psnr_sort, ssim_sort = [], []
    try:
        length = max([int(os.path.splitext(frame)[0]) for frame in os.listdir(os.path.join(lq_root, video))])
        psnr_sort, ssim_sort = [0] * length, [0] * length
        batch_size = 16
        for batch in range(len(os.listdir(os.path.join(lq_root, video)))//batch_size):
            
            gts, hrs, frame_idx = [], [], []
            print(f"Process{pid}", "Reading", video, [batch*batch_size,(batch+1)*batch_size])
            for frame in os.listdir(os.path.join(lq_root, video))[batch*batch_size:(batch+1)*batch_size]:
                lq_path = os.path.join(lq_root, video, frame)
                gt_path = os.path.join(gt_root, video, frame)
                try:
                    lq = cv2.cvtColor(cv2.imread(lq_path, cv2.IMREAD_UNCHANGED), cv2.COLOR_YUV2BGR_I420)
                    gt = cv2.cvtColor(cv2.imread(gt_path, cv2.IMREAD_UNCHANGED), cv2.COLOR_YUV2BGR_I420)
                    hr = cv2.resize(lq, dsize=(gt.shape[1], gt.shape[0]), interpolation=cv2.INTER_CUBIC)
                    gts.append(gt)
                    hrs.append(hr)
                    frame_idx.append(int(os.path.splitext(frame)[0]))
                except Exception as e:
                    print(f"Process{pid}", e)
            gts = torch.from_numpy(np.stack(gts))
            hrs = torch.from_numpy(np.stack(hrs))
            try:
                torch.cuda.empty_cache()
                gts = gts.to('cuda')
                hrs = hrs.to('cuda')
                print(f"Process{pid}", "Calculating PSNR", video, [batch*batch_size,(batch+1)*batch_size])
                psnr_usort = psnr(gts, hrs, data_range=255, reduction='none').cpu()
                print(f"Process{pid}", "Calculating SSIM", video, [batch*batch_size,(batch+1)*batch_size])
                ssim_usort = ssim(gts.permute(0,3,1,2), hrs.permute(0,3,1,2), data_range=255, reduction='none', kernel_size=7, downsample=False).cpu()
            except RuntimeError as e:
                print("Fallback to cpu because of", e)
                gts = gts.cpu()
                hrs = hrs.cpu()
                torch.cuda.empty_cache()
                print(f"Process{pid}", "Calculating PSNR", video, [batch*batch_size,(batch+1)*batch_size])
                psnr_usort = psnr(gts, hrs, data_range=255, reduction='none')
                print(f"Process{pid}", "Calculating SSIM", video, [batch*batch_size,(batch+1)*batch_size])
                ssim_usort = ssim(gts.permute(0,3,1,2), hrs.permute(0,3,1,2), data_range=255, reduction='none', kernel_size=7, downsample=False)
            
            psnr_usort, ssim_usort = list(psnr_usort.numpy()), list(ssim_usort.numpy())
            for i, p, s in zip(frame_idx, psnr_usort, ssim_usort):
                psnr_sort[i-1], ssim_sort[i-1] = p, s
        
    except Exception as e:
        print(f"Process{pid}", e)
    return psnr_sort, ssim_sort


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
    pool = mp.Pool(1)
    videos = os.listdir(args.lq)
    results = {video: pool.apply_async(task, (args.lq, args.gt, video)) for video in videos}

    psnr_path = os.path.join(args.datadir, "psnr.csv")
    ssim_path = os.path.join(args.datadir, "ssim.csv")
    with open(psnr_path, "a+", encoding='utf8') as psnr_f, open(ssim_path, "a+", encoding='utf8') as ssim_f:
        for video in videos:
            psnr_sort, ssim_sort = results[video].get()
            psnr_f.write(f"{video},{','.join(str(frame) for frame in psnr_sort)}\n")
            ssim_f.write(f"{video},{','.join(str(frame) for frame in ssim_sort)}\n")
