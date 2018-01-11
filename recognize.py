import pexpect
import time
import os
import datetime
from subprocess import Popen, PIPE

picture = 'data/new.jpg'
d_picture = 'predictions.png'

def shot():
    a = datetime.datetime.now()
    os.system('raspistill -o '+picture+' -ex sports -e jpg -h 480 -w 640 -t 1 -q 100 --exif none')
    b = datetime.datetime.now()
    print(b-a)

def stream():
    cmd = 'raspivid -t 0 -w 360 -h 240 -fps 5 -b 25000000 -o - | mplayer -fps 10 -demuxer h264es -x 360 -y 240 -'
    return Popen(cmd, stdout = PIPE, stdin = PIPE, stderr = PIPE, shell = True)

def init():
    #cmd = './ninja/NNPACK-darknet/darknet-nnpack/darknet detector test ./ninja/NNPACK-darknet/darknet-nnpack/cfg/voc.data ./ninja/NNPACK-darknet/darknet-nnpack/cfg/tiny-yolo-voc.cfg ./ninja/NNPACK-darknet/darknet-nnpack/tiny-yolo-voc.weights'
    cmd = './alter/ninja/NNPACK/darknet-nnpack/darknet detector test ./alter/ninja/NNPACK/darknet-nnpack/cfg/voc.data ./alter/ninja/NNPACK/darknet-nnpack/cfg/tiny-yolo-voc.cfg ./alter/ninja/NNPACK/darknet-nnpack/tiny-yolo-voc.weights'   
    p = pexpect.spawnu(cmd)
    p.delaybeforesend = None
    time.sleep(15)
    try:
        p.expect_exact('Image Path: ') 
        ret = p.before
    except:
        ret =''
    return p

def recognize(p):
    a = datetime.datetime.now()
    try:
        p.sendline(picture)
        time.sleep(1.5)
        p.expect_exact('all done')
        ret = p.before
        res = ret.find('person: ')
    except:
        return False
    b = datetime.datetime.now()
    if(res == -1):
        print(b-a)
        return False
    else:
        print(b-a)
        return True

def move():
    os.system('cp '+d_picture+' ./data/')
    time.sleep(3)
