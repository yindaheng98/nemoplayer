import sys
import os
import cv2

IMAGEROOT = sys.argv[1]
video = sys.argv[2]
name = '.'.join(os.path.basename(video).split('.')[0:-3])
start, end = os.path.basename(video).split('.')[-2].split('+')
path = os.path.join(IMAGEROOT, name, '%03d' % (int(start) + 1) + '.png')
image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
sys.stdout.buffer.write(image.tobytes())
'''
height, width = image.shape[0:-1]
process = (
    ffmpeg
    .input(path)
    .output('pipe:', format='rawvideo', pix_fmt='yuv420p')
    .run_async(pipe_stdin=False, pipe_stdout=True, pipe_stderr=False)
)
frame = process.stdout.read(width * height * 3)
sys.stdout.buffer.write(frame)
'''