import sys
import os
import cv2

IMAGEROOT = sys.argv[1]
video = sys.argv[2]
name = '.'.join(os.path.basename(video).split('.')[0:-3])
start, end = os.path.basename(video).split('.')[-2].split('+')
path = os.path.join(IMAGEROOT, name, '%03d' % (int(start) + 1) + '.png')
image = cv2.cvtColor(cv2.imread(path, cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2YUV_I420)
sys.stdout.buffer.write(image.tobytes())
