import pexpect
import time
import os
from subprocess import Popen, PIPE

picture = 'data/new.jpg'
d_picture = 'predictions.png'

def shot():
    os.system('raspistill -o '+picture+' -ex sports -e jpg -h 480 -w 640 -t 1 -q 100 --exif none')

def stream():
    cmd = 'raspivid -t 0 -w 360 -h 240 -fps 5 -b 25000000 -o - | mplayer -fps 10 -demuxer h264es -x 360 -y 240 -'
    return Popen(cmd, stdout = PIPE, stdin = PIPE, stderr = PIPE, shell = True)

def init():
    cmd = './ninja/NNPACK-darknet/darknet-nnpack/darknet detector test ./ninja/NNPACK-darknet/darknet-nnpack/cfg/voc.data ./ninja/NNPACK-darknet/darknet-nnpack/cfg/tiny-yolo-voc.cfg ./ninja/NNPACK-darknet/darknet-nnpack/tiny-yolo-voc.weights'
    p = pexpect.spawnu(cmd)
    time.sleep(15)
    p.expect('Enter Image Path: ') 
    ret = p.before
    return p

def recognize(p):
    try:
        p.sendline(picture)
        p.expect('Enter Image Path: ') 
        ret = p.before
        res = ret.find('person')
    except:
        return False
    os.system('cp '+d_picture+' ./data/')
    os.system('rm '+d_picture)
    #os.system('convert -resize 640x480 data/'+d_picture+' data/'+d_picture)
    if(res == -1):
    	return False
    else:
    	return True
