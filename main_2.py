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
Relay_1 =17
GPIO.setup(Relay_1,GPIO.OUT)
GPIO.output(Relay_1,True)           
           

###############################################

def Relay_1_ON ():
    GPIO.output(Relay_1,False)
    time.sleep(5)
    GPIO.output(Relay_1,True)
    
    


def image_cap (full_frame):

    date = time.strftime("%Y-%b-%d_(%H%M%S)")

    full_frame=full_frame[240:540,450:750]

    filename = '/home/pi/test_file/{0}>.png' .format(date)
    cv2.imwrite( filename , full_frame)
    
def image_cap_2 (frame):

    date = time.strftime("%Y-%b-%d_(%H%M%S)")

    frame=frame[0:300,50:350]

    filename = '/home/pi/test_file/{0}.png' .format(date)
    cv2.imwrite( filename , frame)




# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=3000, help="minimum area size")
args = vars(ap.parse_args())
# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
# otherwise, we are reading from a video file
else:
    vs = cv2.VideoCapture(args["video"])
# initialize the first frame in the video stream
firstFrame = None
i = 0




# loop over the frames of the video
while True:
    # grab the current frame and initialize the occupied/unoccupied
    # text
    frame = vs.read()
    full_frame=frame
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

#show the trigger zone in red rectangle
    
    #cv2.rectangle(frame, (200, 100), (300, 250), (0, 0, 255), 2)
    

#small red frame

    frameDelta_RED = cv2.absdiff(firstFrame[100:250,200:300], gray[100:250,200:300])
    thresh = cv2.threshold(frameDelta_RED, 25, 255, cv2.THRESH_BINARY)[1]
    
    ############################ sens of the motion ditection

    thresh_sum=np.sum(thresh)
    if thresh_sum > 1330000:
        image_cap(full_frame)
        #image_cap_2 (frame)
        
        #Relay_1_ON ()




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
        #image_cap(frame)
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame[100:250,200:300], (x, y), (x + w, y + h), (0, 255, 0), 2)
    # ==================================================
    #big frame

    #frameDelta = cv2.absdiff(firstFrame, gray)
    #thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    #thresh =cv2.dilate(thresh, None, iterations=2)
    #cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                #cv2.CHAIN_APPROX_SIMPLE)
    #cnts = imutils.grab_contours(cnts)
    #for c_1 in cnts:
            # if the contour is too small, ignore it
        #if cv2.contourArea(c_1) < args["min_area"]:
           # continue

        #(x, y, w, h) = cv2.boundingRect(c_1)
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        i += 1
        if (i > 75):
            firstFrame = gray.copy()
            i = 0

        text = "Detected"

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


    # if the `q` key is pressed, break from the lop
   # if key == ord("q"):
       # break

# cleanup the camera and close any open windows
#vs.stop() if args.get("video", None) is None else vs.release()
#cv2.destroyAllWindows()

