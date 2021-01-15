import cv2
import numpy as np
import os
# 330x243

import sys

vpath = sys.argv[1]
(fname, ext) = os.path.splitext(vpath)
spath = fname+'.smi'
tpath = fname+'.jpg'

if os.path.isfile(tpath):
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

t = (frame_num / fps) + delay
cmd1 = f'iconv -f {smi_enc} \'{spath}\' > tmp.smi'
cmd2 = f'ffmpeg -y -i tmp.smi tmp.ass'
cmd3 = f'ffmpeg -y -ss {t} -copyts -i \'{vpath}\' -vf "subtitles=\'tmp.ass\':force_style=\'Fontsize=35\'" -vframes 1 tmp.jpg'
cmd4 = f'ffmpeg -y -i tmp.jpg -vf scale=160:-1 \'{tpath}\''
print(cmd1)
print(cmd2)
print(cmd3)
print(cmd4)
os.system(cmd1)
os.system(cmd2)
os.system(cmd3)
os.system(cmd4)
os.remove('tmp.smi')
os.remove('tmp.ass')
os.remove('tmp.jpg')
