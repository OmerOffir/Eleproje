# import the necessary packages
from imutils.video import VideoStream
import numpy as np
import argparse
import datetime
import imutils
import time
from time import sleep, strftime
import cv2
import RPi.GPIO as GPIO
#import matplotlib.pyplot as plt
import pyrebase
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("/home/pi/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

firebaseconfig = {
    "apiKey": "AIzaSyDzIN8bRheaHJwUvoEwYAVmaVLs8raKtPY",
    "authDomain": "eleproje.firebaseapp.com",
    "databaseURL": "https://eleproje-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "eleproje",
    "storageBucket": "eleproje.appspot.com",
    "messagingSenderId": "776757916626",
    "appId": "1:776757916626:web:b324b35cfe3b0fa929ce0b",
    "measurementId": "G-02FNTRRDST",
    "serviceaccount": "serviceaccount.json"
  }
    
  

firebase = pyrebase.initialize_app(firebaseconfig)
storage = firebase.storage()

###############################################
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
benefit_zone_trigger = 17
benefit_zone_trigger_2 = 18
BUZZER  = 23
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(benefit_zone_trigger, GPIO.OUT)
GPIO.setup(benefit_zone_trigger_2, GPIO.OUT)
GPIO.output(BUZZER, False)

#plt.ion()
x = []
y = []


###############################################
def write_temp(temp):
    with open("/home/pi/log_file.csv", "a") as log:
        log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(temp)))

###############################################

def Buzzzer_activation ():
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


def image_cap(full_frame):
    date = time.strftime("%Y-%b-%d_(%H%M%S)")
    full_frame = imutils.resize(full_frame, width=1920)
    filename = '/home/pi/test_file/{0}>.png'.format(date)
    cv2.imwrite(filename, full_frame)
    #storage.child(filename).put(full_frame)




# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=3000, help="minimum area size")
args = vars(ap.parse_args())
# if the video argument is None, then we are reading from webcam
vs = VideoStream(src=0).start()
time.sleep(1.0)

firstFrame = None

i = 0

# loop over the frames of the video
while True:
    # grab the current frame and initialize the occupied/unoccupied
    # text
    frame = vs.read()
    full_frame = frame
    frame = frame if args.get("video", None) is None else frame[1]
    text = "Not Detected"
    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if frame is None:
        break

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue

    # show the trigger zone in red and blue 

    cv2.rectangle(frame, (275, 180), (380, 250), (0, 0, 255), 2)
    # cv2.rectangle(frame, (X, Y), (Xend, Yend), (BLUE, GREEN, RED), 2)
    cv2.rectangle(frame, (30, 35), (380, 100), (255, 0, 0), 2)

    # small RED frame

    frameDelta_RED = cv2.absdiff(firstFrame[180:250, 275:380], gray[180:250, 275:380])
    #frameDelta_RED = cv2.absdiff(firstFrame[Y:Yend, X:Xend], gray[Y:Yend, X:Xend])
    thresh_RED = cv2.threshold(frameDelta_RED, 25, 255, cv2.THRESH_BINARY)[1]
    
    # small BLUE frame

    frameDelta_BLUE = cv2.absdiff(firstFrame[35:100, 30:380], gray[35:100, 30:380])
    #frameDelta_RED = cv2.absdiff(firstFrame[Y:Yend, X:Xend], gray[Y:Yend, X:Xend])
    thresh_BLUE = cv2.threshold(frameDelta_BLUE, 25, 255, cv2.THRESH_BINARY)[1]


    ############################ sens of the motion ditection
    thresh_sum_BLUE = np.sum(thresh_BLUE)
    thresh_sum_RED = np.sum(thresh_RED)
    
    
    #time.sleep(0.3)
    if thresh_sum_RED > 400000:
        text = "Detected"
        action = "Touched the button"
        #image_cap(full_frame)
        #time.sleep(0.3)
        Buzzzer_activation ()
        write_temp(action)
        #time.sleep(0.3)
        Benefit_zone ()
        
        
    if thresh_sum_BLUE > 900000:
        action = "Passed by"
        Buzzzer_activation ()
        write_temp(action)
        

        


    i += 1
    if (i > 2):
        firstFrame = gray
        i = 0
        thresh_sum_RED=0
        thresh_sum_BLUE=0


    # draw the text and timestamp on the frame
    cv2.putText(frame, "Elephant Motion: {}".format(text), (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    # show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    #     cv2.imshow("Thresh", thresh)
    #     cv2.imshow("Frame Delta", frameDelta)

    key = cv2.waitKey(1) & 0xFF
    
    #print(thresh_sum_BLUE)
    print(thresh_sum_RED)

    # if the `q` key is pressed, break from the lop
# if key == ord("q"):
# break

# cleanup the camera and close any open windows
# vs.stop() if args.get("video", None) is None else vs.release()
# cv2.4711w1destroyAllWindows()



