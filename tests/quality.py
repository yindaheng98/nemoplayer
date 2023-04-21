import logging
import torch
from piq import psnr, ssim

from common import parse_args, read_videos, data_append

logging.basicConfig(level=logging.INFO)

args = parse_args()
frames_o, frames_d = read_videos(args)
frames_o_cpu = torch.from_numpy(frames_o)
frames_d_cpu = torch.from_numpy(frames_d)

try:
    frames_o_cuda = frames_o_cpu.to('cuda')
    frames_d_cuda = frames_d_cpu.to('cuda')
    psnr_ = psnr(frames_o_cuda, frames_d_cuda, data_range=255, reduction='none').cpu()
    ssim_ = ssim(frames_o_cuda.permute(0,3,1,2), frames_d_cuda.permute(0,3,1,2), data_range=255, reduction='none', kernel_size=7, downsample=False).cpu()
except RuntimeError as e:
    print("Fallback to CPU because of", e)
    psnr_ = psnr(frames_o_cpu, frames_d_cpu, data_range=255, reduction='none')
    ssim_ = ssim(frames_o_cpu.permute(0,3,1,2), frames_d_cpu.permute(0,3,1,2), data_range=255, reduction='none', kernel_size=7, downsample=False).cpu()

data_append(args=args, data=list(psnr_.numpy()), name="psnr")
data_append(args=args, data=list(ssim_.numpy()), name="ssim")
