import logging
import torch
from piq import psnr, ssim

from common import parse_args, read_videos, data_append

logging.basicConfig(level=logging.INFO)

args = parse_args()
frames_o, frames_d = read_videos(args)
frames_o_cuda = torch.from_numpy(frames_o) #.to('cuda')
frames_d_cuda = torch.from_numpy(frames_d) #.to('cuda')

data_append(args=args, data=list(psnr(frames_o_cuda, frames_d_cuda, data_range=255, reduction='none').cpu().numpy()), name="psnr")

data_append(args=args, data=list(ssim(frames_o_cuda.permute(0,3,1,2), frames_d_cuda.permute(0,3,1,2), data_range=255, reduction='none', kernel_size=7, downsample=False).cpu().numpy()), name="ssim")
