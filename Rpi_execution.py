#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import smbus
from recognize import *
GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.OUT) #buzzer
GPIO.setup(22,GPIO.OUT) #relay switch
GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP) #IR sensor signal
bus=smbus.SMBus(1)
address=0x04
cmd={'b':0,'w':1,'s':2,'d':3,'a':4,'x':-1}

class Status:
	def __init__(self):
		self.CAMERA=False
		self.child_process=init()
	def interruptHandler_IR(self):
		self.CAMERA=True
	def init_child_process(self):
		self.child_process=init()
S=Status()

def writeCMD(value):
	bus.write_byte(address,value)

def IR_callback(channel):
	S.interruptHandler_IR()
	GPIO.output(22,True)
	shot()
	GPIO.output(22,False)
	if recognize(S.child_process):
		GPIO.output(16,True)
		while True:
			GPIO.output(22,False)
			time.sleep(0.1)
			GPIO.output(22,True)
			time.sleep(0.1)
	else:
		GPIO.output(22,False)
		S.init_child_process()
		
	S.CAMERA=False

GPIO.add_event_detect(18,GPIO.RISING,callback=IR_callback)
if __name__=="__main__":
	f=open("seq.txt",'r')
	line=f.readline()
	currentline=line.split(",")
	GPIO.output(16,False)
	GPIO.output(22,False)
	while True:
		for key in currentline:
			while(S.CAMERA):
				a=1
			writeCMD(cmd[key])
			time.sleep(1.1)
		GPIO.output(16,False)
		GPIO.output(22,False)
	f.close()
