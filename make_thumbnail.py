import cv2
import numpy as np
import os
# 330x243

import sys


import argparse

parser = argparse.ArgumentParser(description='Make video thumbnail by pattern matching.')
parser.add_argument('video', metavar='PATH', type=str,
                    help='Video Path')
parser.add_argument('-force','-f', action='store_true', help='force rebuild')
args = parser.parse_args()

vpath = args.video
(fname, ext) = os.path.splitext(vpath)
spath = fname+'.smi'
tpath = fname+'.jpg'

if os.path.isfile('tmp.smi'):
    os.remove('tmp.smi')
if os.path.isfile('tmp.ass'):
    os.remove('tmp.ass')
if os.path.isfile('tmp.jpg'):
    os.remove('tmp.jpg')

if (not args.force) and os.path.isfile(tpath):
	exit()


import chardet
smi = open(spath, 'rb').read()
result = chardet.detect(smi)
smi_enc = result['encoding']
if 'UTF-8' in smi_enc:
    smi_enc = 'utf8'

print("video:", vpath)
print("smi:  ", spath)
print("enc:", smi_enc)
print("thumb:", tpath)

threshold = 0.9
delay = 3
dsize = (100,100)
tmpl = cv2.imread('tmpl.png', cv2.IMREAD_GRAYSCALE)
tmpl = cv2.resize(tmpl, dsize)
video = cv2.VideoCapture(vpath)
fps = video.get(cv2.CAP_PROP_FPS)
frame_delay = 3 * fps
success,image = video.read()
frame_num = 0
while success:
    #print('Read a new frame: ', frame_num/fps , success)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image, dsize)
    result = cv2.matchTemplate(image,tmpl, cv2.TM_CCORR_NORMED)
    loc = np.where(result >= threshold)
    if len(loc[0]) != 0:
        break     
    success,image = video.read()
    frame_num += 1
    if (frame_num / fps) > 10*60:
        exit()

t = (frame_num / fps) + delay
cmd1 = f'iconv -f {smi_enc} \'{spath}\' > tmp.smi'
cmd2 = f'ffmpeg -y -i tmp.smi tmp.ass'
cmd3 = f'ffmpeg -y -ss {t} -copyts -i \'{vpath}\'  -vf "subtitles=\'tmp.ass\':force_style=\'Fontsize=40,Alignment=6\'" -vframes 1 tmp.jpg'
cmd4 = f'ffmpeg -y -i tmp.jpg -vf scale=160:120 \'{tpath}\''
print(cmd1)
print(cmd2)
print(cmd3)
print(cmd4)
os.system(cmd1)
os.system(cmd2)
os.system(cmd3)
os.system(cmd4)

