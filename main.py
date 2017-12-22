from tkinter import *
from tkinter.ttk import *
import os
import smbus
import RPi.GPIO as GPIO
import time
from threading import Thread
from recognize import *
GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.OUT) # buzzer
GPIO.setup(22,GPIO.OUT) # relay switch
GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP) # IR sensor signal
GPIO.output(16,False)
GPIO.output(22,False)
bus=smbus.SMBus(1)
address=0x04
cmd={'b':0,'w':1,'s':2,'d':3,'a':4,'x':-1}
win=Tk()
win.title("Car GUI")
win.geometry("645x650")
Style().configure("CB.TButton",font=("Sans","12","bold"),foreground="blue")
Style().configure("EB.TButton",font=("Sans","12","bold"),foreground="red")
btn_forward=Button(win,text="^",width=2,style="CB.TButton")
btn_backward=Button(win,text="v",width=2,style="CB.TButton")
btn_right=Button(win,text=">",width=2,style="CB.TButton")
btn_left=Button(win,text="<",width=2,style="CB.TButton")
btn_end=Button(win,text="X",width=2,style="EB.TButton")

btn_forward.place(x=45,y=550)
btn_backward.place(x=45,y=600)
btn_left.place(x=20,y=575)
btn_right.place(x=70,y=575)
btn_end.place(x=45,y=575)

class route:
    def __init__(self):
        self.window=win
        self.button_forward=btn_forward
        self.button_backward=btn_backward
        self.button_right=btn_right
        self.button_left=btn_left
        self.button_end=btn_end

        self.cmdValue='b'
        self.delay=1.1
    def forward(self):
        self.disableButtons()
        self.cmdValue='w'
        bus.write_byte(address,cmd[self.cmdValue])
        self.file.write(self.cmdValue+',')
        time.sleep(self.delay)
        self.enableButtons()
    def backward(self):
        self.disableButtons()
        self.cmdValue='s'
        bus.write_byte(address,cmd[self.cmdValue])
        self.file.write(self.cmdValue+',')
        time.sleep(self.delay)
        self.enableButtons()
    def right(self):
        self.disableButtons()
        self.cmdValue='d'
        bus.write_byte(address,cmd[self.cmdValue])
        self.file.write(self.cmdValue+',')
        time.sleep(self.delay)
        self.enableButtons()
    def left(self):
        self.disableButtons()
        self.cmdValue='a'
        bus.write_byte(address,cmd[self.cmdValue])
        self.file.write(self.cmdValue+',')
        time.sleep(self.delay)
        self.enableButtons()
    def end(self):
        enable_GO()
        enable_STOP()
        self.disableButtons()
        self.cmdValue='x'
        bus.write_byte(address,cmd['b'])
        self.file.write(self.cmdValue)
        self.button_forward.config(command=None)
        self.button_backward.config(command=None)
        self.button_right.config(command=None)
        self.button_left.config(command=None)
        self.button_end.config(command=None)
        self.file.close()
    def disableButtons(self):
        self.button_forward.state(["disabled"])
        self.button_backward.state(["disabled"])
        self.button_right.state(["disabled"])
        self.button_left.state(["disabled"])
        self.button_end.state(["disabled"])

    def enableButtons(self):
        self.button_forward.state(["!disabled"])
        self.button_backward.state(["!disabled"])
        self.button_right.state(["!disabled"])
        self.button_left.state(["!disabled"])
        self.button_end.state(["!disabled"])
 
    def start(self):
        self.file=open("cmd.txt",'w')
        self.button_forward.config(command=self.forward)
        self.button_backward.config(command=self.backward)
        self.button_right.config(command=self.right)
        self.button_left.config(command=self.left)
        self.button_end.config(command=self.end)
        self.enableButtons()
Route=route()

def keepMoving():
    Status.deactivateKeepMoving()
    Status.KEEPMOVING=True
    Status.changeMessage("","black") 

class status:
    def __init__(self):
        self.win=win
        self.child_process=init()
        self.CAMERA=False
        self.VIDEO=False
        self.MOVE=0
        self.STOP=False
        self.KEEPMOVING=False
        self.image=PhotoImage(file="./data/cover.png")
        self.label=Label(image=self.image)
        self.message=Label(self.win,text="   READY",foreground="black",font=("Helvetica",36))
        self.btn_keepmoving=Button(self.win,text="Keep Moving",width=12,style="EB.TButton")
    def interruptHandler_IR(self):
        self.CAMERA=True
    def changeImage(self,path):
        self.image=PhotoImage(file=path)
        self.label.configure(image=self.image)
    def changeMessage(self,text,color):
        self.message.configure(text=text)
        self.message.configure(foreground=color)
    def activateKeepMoving(self):
        self.btn_keepmoving.configure(command=keepMoving)
        self.btn_keepmoving.place(x=360,y=600)
    def deactivateKeepMoving(self):
        self.btn_keepmoving.configure(command=None)
Status=status()

class executionThread(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        GPIO.add_event_detect(18,GPIO.RISING,callback=IR_callback)  
        f=open("cmd.txt",'r')
        line=f.readline()
        currentline=line.split(",")
        while True:
            for key in currentline:
                while(Status.CAMERA):
                    a=1 #do nothing
                if Status.STOP:
                    GPIO.remove_event_detect(18)
                    f.close()
                    return
                bus.write_byte(address,cmd[key])
                Status.MOVE+=1
                time.sleep(1.1)

class videoThread(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        Stream=stream()
        while True:
            if Stream.poll()==0:
                Status.VIDEO=False
                return

def IR_callback(channel):
    if Status.VIDEO:
        return
    if(Status.MOVE>1):
        Status.KEEPMOVING=False
        Status.interruptHandler_IR()
        GPIO.output(22,True)
        time.sleep(1)
        shot()
        GPIO.output(22,False)
        if recognize(Status.child_process):
            Status.changeImage("./data/predictions.png")
            Status.changeMessage("WARNING","red")
            Status.activateKeepMoving()
            while True:
                if(Status.STOP or Status.KEEPMOVING):
                    break
                GPIO.output(16,True)
                GPIO.output(22,True)
                time.sleep(0.1)
                GPIO.output(22,False)
                time.sleep(0.1)
        else:
            Status.changeImage("./data/predictions.png")
            Status.changeMessage("      OK","green")
        GPIO.output(16,False)
        GPIO.output(22,False)
        Status.MOVE=0
    Status.CAMERA=False

def setupRoute():
    Status.STOP=True
    disable_STOP()
    disable_GO()
    Route.start()

def startNavigation():
    Status.STOP=False
    Status.CAMERA=False
    Status.MOVE=0
    disable_SetupandGO()
    Route.disableButtons()
    Status.changeMessage("","black")
    OBJ=executionThread()
    OBJ.start()

def stopNavigation():
    Status.STOP=True
    enable_SetupandGO()
    Status.changeMessage("   READY","black")
    Status.deactivateKeepMoving()
    Route.enableButtons()
    GPIO.output(16,False)
    GPIO.output(22,False)

def monitor():
    if Status.CAMERA:
        return
    Status.VIDEO=True
    OBJ=videoThread()
    OBJ.start()

Style().configure("Bold.TButton", font = ('Sans','10','bold'),foreground='black')
btn_setupRoute=Button(win,text="Set Up Route",command=setupRoute,style="Bold.TButton")
btn_setupRoute.place(x=15,y=510)
   
btn_GO=Button(win,text="GO !",command=startNavigation,style="Bold.TButton")
btn_GO.place(x=130,y=560)
   
btn_stop=Button(win,text="STOP",command=stopNavigation,style="Bold.TButton")
btn_stop.place(x=130,y=600)

Style().configure("VB.TButton",font=('Sans','12','bold'),foreground="green",background="black")
btn_video=Button(win,text="Monitor",command=monitor,style="VB.TButton")
btn_video.place(x=120,y=510)

def disable_SetupandGO():
    btn_setupRoute.state(["disabled"])
    btn_GO.state(["disabled"])
def enable_SetupandGO():
    btn_setupRoute.state(["!disabled"])
    btn_GO.state(["!disabled"])
def disable_GO():
    btn_GO.state(["disabled"])
def enable_GO():
    btn_GO.state(["!disabled"])
def disable_STOP():
    btn_stop.state(["disabled"])
def enable_STOP():
    btn_stop.state(["!disabled"])

if __name__=="__main__":
    Status.label.place(x=0,y=0)
    Status.message.place(x=300,y=520)
    win.mainloop()
