from guizero import App, Text,PushButton,Window ,Picture
import time
import imutils
import cv2
import RPi.GPIO as GPIO
from time import sleep
import numpy as np
#############################################
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()
############################################# define GPIO
BUZZER= 23
benefit_zone_trigger=17
benefit_zone_trigger_2=18
lights1= 27
GPIO.setup(benefit_zone_trigger,GPIO.OUT)
GPIO.setup(benefit_zone_trigger_2,GPIO.OUT)
#p = GPIO.PWM(benefit_zone_trigger ,50)
#p.start(7) #Initialization
GPIO.setup(lights1,GPIO.OUT)
GPIO.output(lights1,True)

############################################# define state of the pins
buzzState = False
############################################## define GPIO as output
GPIO.setup(BUZZER, GPIO.OUT)



def lights_img ():
    GPIO.output(lights1,False)
    
        
    vs = cv2.VideoCapture(0)
    time.sleep(1.5)
    _, frame =vs.read()
    date = time.strftime("%Y-%b-%d_(%H%M%S)")
    frame = imutils.resize(frame, width=1920)
    #frame= frame[360:660,460:760]
    filename = '/home/pi/test_file/{0}.png'.format(date)
    cv2.imwrite(filename ,frame)
    
    GPIO.output(lights1,True)
    

def Buzzer ():

    GPIO.output(BUZZER,False)
    time.sleep(0.5)
    GPIO.output(BUZZER,True)
    time.sleep(0.5)
    GPIO.output(BUZZER,False)
    time.sleep(0.5)
    GPIO.output(BUZZER,True)
    time.sleep(0.5)
    GPIO.output(BUZZER,False)
    time.sleep(0.5)
    GPIO.output(BUZZER,True)
    time.sleep(0.5)
    GPIO.output(BUZZER,False)
        

def img_capture ():
    vs = cv2.VideoCapture(0)
    time.sleep(1)
    _, frame =vs.read()
    date = time.strftime("%Y-%b-%d_(%H%M%S)")
    frame = imutils.resize(frame, width=500)
    #frame= frame[0:300,50:350]
    filename = '/home/pi/test_file/{0}.png'.format(date)
    cv2.imwrite(filename ,frame)
    
    

def Benefit_zone ():
    t = GPIO.PWM(benefit_zone_trigger_2 ,50)
    t.start(5.5) #Initialization
    time.sleep(0.5)
    t.ChangeDutyCycle(10.5)
    time.sleep(0.5)
    
    
    
    p = GPIO.PWM(benefit_zone_trigger ,50)
    p.start(7) #Initialization
    time.sleep(0.5)
    p.ChangeDutyCycle(3.5)
    time.sleep(0.5)
    p.ChangeDutyCycle(7)
    time.sleep(0.5)
    
    t.ChangeDutyCycle(5.5)
    time.sleep(0.5)
    
    
    
    
    


def lights ():
    Loop=[True,False,True,False]
    for B in Loop:
        GPIO.output(Buzzer,B)
        time.sleep(0.5)
    


    

    




app = App(title="Eleproje Control Panel ")
welcome_message = Text(app, text="Welcome to our Project Control Panel App", size=20, font="Times New Roman", color="lightblue")


# function to activate the buzzer
Buzzer_Button = PushButton(app, command=Buzzer, text="Buzzer",align="left",grid=[0,1] )
# function to capture an img.
img_Button = PushButton(app, command=img_capture, text="img capture", align="right")
# function to activate benefit zone
benefit_zone_Button = PushButton(app, command=Benefit_zone, text="Benefit zone",align="up")
# function to turn on the lights
lights_Button = PushButton(app, command=lights, text="Lights",align="bottom")
# function to capture image with lights.
img_lights_button= PushButton(app , command =lights_img , text="full_img" ,align="right")

app.display()

