#!/usr/bin/python
import smbus
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.IN,pull_up_down=GPIO.PUD_UP)
bus=smbus.SMBus(1)
address=0x04
cmd={'b':0,'w':1,'s':2,'d':3,'a':4,'x':-1}
class ACKStatus:
    def __init__(self):
        self.ACK=False
    def interruptHandler(self):
        self.ACK=True
ACK=ACKStatus()
def writeCMD(value):
        bus.write_byte(address,value)

def my_callback(channel):
            ACK.interruptHandler()
GPIO.add_event_detect(26,GPIO.RISING,callback=my_callback)
if __name__=="__main__":
    f=open('seq.txt','w')
    key='b'
    while cmd[key]!=-1:
        key=raw_input('b:STOP,w:FORWARD,s:BACKWARD,d:RIGHT,a:LEFT,x:END')
        if key not in cmd:
            print "Please enter a valid key !"
            key='b'
            continue
        ACK.ACK=False
        writeCMD(cmd[key])
        time.sleep(1)
        if key=='x':
            f.write(key)
        else:
            f.write(key+',')
    f.close()
