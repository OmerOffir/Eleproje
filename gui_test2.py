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
GPIO.setup(benefit_zone_trigger,GPIO.OUT)
GPIO.output(benefit_zone_trigger,True)
#lights = 27
############################################# define state of the pins
buzzState = False
#lights_state = True
############################################## define GPIO as output
GPIO.setup(BUZZER, GPIO.OUT)
#GPIO.setup(benefit_zone_trigger, GPIO.OUT)
#GPIO.setup(lights, GPIO.OUT)




def Buzzer ():

    global buzzState
    
    if buzzState == False:
        GPIO.output(BUZZER, True)
        buzzState = True
        time.sleep(1)
    else:
        GPIO.output(BUZZER, False)
        buzzState = False
        time.sleep(1)
        

def img_capture ():
    
    vs = cv2.VideoCapture(0)
    _, frame =vs.read()
    date = time.strftime("%Y-%b-%d_(%H%M%S)")
    #frame= frame[0:250, 200:300]
    filename = '/home/pi/img_test/{0}.png'.format(date)
    cv2.imwrite(filename ,frame)
    picture = Picture (app ,filename)
    
    
    

def Benefit_zone ():
    GPIO.output(benefit_zone_trigger,False)
    time.sleep(5)
    GPIO.output(benefit_zone_trigger,True)
    time.sleep(1)
    
        
   


def lights ():
    global buzzState
    
    if buzzState == False:
        GPIO.output(BUZZER, True)
        buzzState = True
        time.sleep(1)
    else:
        GPIO.output(BUZZER, False)
        buzzState = False
        time.sleep(1)


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



    


app.display()


