# import the necessary packages
from imutils.video import VideoStream
import numpy as np
import argparse
import datetime
import imutils
import time
from time import sleep
import cv2
import RPi.GPIO as GPIO

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
    
def img_capture ():
    vs = cv2.VideoCapture(0)
    time.sleep(1)
    _, frame =vs.read()
    date = time.strftime("%Y-%b-%d_(%H%M%S)")
    frame = imutils.resize(frame, width=500)
    frame= frame[0:300,50:350]
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


def image_cap(full_frame):
    date = time.strftime("%Y-%b-%d_(%H%M%S)")

    full_frame = full_frame[360:660, 460:760]

    filename = '/home/pi/test_file/{0}>.png'.format(date)
    cv2.imwrite(filename, full_frame)


def image_cap_2(frame):
    date = time.strftime("%Y-%b-%d_(%H%M%S)")

    frame = frame[0:300, 50:350]

    filename = '/home/pi/test_file/{0}.png'.format(date)
    cv2.imwrite(filename, frame)


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

    # show the trigger zone in red rectangle

    cv2.rectangle(frame, (205, 160), (270, 190), (0, 0, 255), 2)
    # cv2.rectangle(frame, (X, Y), (Xend, Yend), (0, 0, RED), 2)

    # small red frame

    frameDelta_RED = cv2.absdiff(firstFrame[160:190, 205:270], gray[160:190, 205:270])
    thresh = cv2.threshold(frameDelta_RED, 25, 255, cv2.THRESH_BINARY)[1]

    ############################ sens of the motion ditection

    thresh_sum = np.sum(thresh)
    if thresh_sum > 300000:
        text = "Detected"
        image_cap(full_frame)
        time.sleep(0.3)
        Buzzzer_activation ()
        time.sleep(0.3)
        Benefit_zone ()
        
        # image_cap_2 (frame)

        

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
            continue
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        # image_cap(frame)
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame[160:190, 205:270], (x, y), (x + w, y + h), (0, 255, 0), 2)
        # ==================================================
    #text = "Detected"
    i += 1
    if (i > 80):
        firstFrame = gray
        i = 0
        thresh_sum=0


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
    print(thresh_sum)

    # if the `q` key is pressed, break from the lop
# if key == ord("q"):
# break

# cleanup the camera and close any open windows
# vs.stop() if args.get("video", None) is None else vs.release()
# cv2.4711w1destroyAllWindows()



