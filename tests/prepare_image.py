import sys
import ffmpeg
import numpy as np
import cv2

video = sys.argv[1]
path_fmt = sys.argv[2]
probe = ffmpeg.probe(video)
width = probe['streams'][0]['width']
height = probe['streams'][0]['height']

process = (
    ffmpeg
    .input(video)
    .output('pipe:', format='rawvideo', pix_fmt='yuv420p')
    .run_async(pipe_stdout=True)
)
i = 1
while True:
    in_bytes = process.stdout.read(width * height//2*3)
    if not in_bytes:
        break
    in_frame = (
        np
        .frombuffer(in_bytes, np.uint8)
        .reshape([height//2*3, width])
    )
    cv2.imwrite(path_fmt % i, in_frame)
    i += 1
