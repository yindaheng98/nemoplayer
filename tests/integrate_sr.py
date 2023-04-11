import sys
import os
import cv2

IMAGEROOT = sys.argv[1]
video = sys.argv[2]
name = os.path.basename(video).split('.')[0]
start, end = os.path.basename(video).split('.')[2].split('+')
path = os.path.join(IMAGEROOT, name, '%03d' % (int(start) + 1)+ '.png')
image = cv2.imread(path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV_YV12)
sys.stdout.buffer.write(image.tobytes())
