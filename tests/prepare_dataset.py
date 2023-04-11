import os
import sys

script = os.path.join(os.path.dirname(sys.argv[0]), "prepare_video.sh")

scale = int(sys.argv[1])
root_orig = sys.argv[2]
root_desc = os.path.join(root_orig, '')[0:-1] + "_x%d" % scale
for name in os.listdir(root_orig):
    path_orig = os.path.join(root_orig, name)
    path_desc = os.path.join(root_desc, name + '.ivf')
    cmd = [script, path_orig, path_desc, scale]
    print(cmd)