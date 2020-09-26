

# python color_tracking.py --video balls.mp4
# python color_tracking.py

# import the necessary packages
from collections import deque
import socket
import numpy as np
import argparse
import imutils
import cv2
import time
import tellopy
import urllib  # for reading image from URL


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ("192.168.10.1", 8889)
sock.bind(('', 9000))


msg = "command"
msg = msg.encode()
print(msg)
sent = sock.sendto(msg, tello_address)


msg = "streamon"
msg = msg.encode()
print(msg)
sent = sock.sendto(msg, tello_address)

msg = "takeoff"
msg = msg.encode()
print(msg)
sent = sock.sendto(msg, tello_address)


time.sleep(3)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the colors in the HSV color space
lower = {'red': (166, 84, 141)}  # assign new item lower['blue'] = (93, 10, 0)
upper = {'red': (186, 255, 255)}

# define standard colors for circle around the object
colors = {'red': (0, 0, 255)}

# pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture("udp://@0.0.0.0:11111")

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])
# keep looping
while True:
    msg = ""
    msg = msg.encode()
    print(msg)
    sent = sock.sendto(msg, tello_address)

    # grab the current frame
    (grabbed, frame) = camera.read()
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break

    # IP webcam image stream
    # URL = 'http://10.254.254.102:8080/shot.jpg'
    # urllib.urlretrieve(URL, 'shot1.jpg')
    # frame = cv2.imread('shot1.jpg')

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600, height=450)

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # for each color in dictionary check object in frame
    for key, value in upper.items():
        # construct a mask for the color from dictionary`1, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        kernel = np.ones((9, 9), np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # Circle Center
            centerX = center[0]
            centerY = center[1]

            # only proceed if the radius meets a minimum size. Correct this value for your obect's size
            if radius > 1:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 2)
                cv2.putText(frame, key + "red ball", (int(x - radius), int(y - radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            colors[key], 2)

                if centerX > 300:
                    msg = "right 25"
                    msg = msg.encode()
                    print(msg)
                    sent = sock.sendto(msg, tello_address)

                else:
                    msg = "left 25"
                    msg = msg.encode()
                    print(msg)
                    sent = sock.sendto(msg, tello_address)

                cv2.line(frame, (300, 225), (centerX, centerY), color=(255, 0, 0))

    # show the frame to our screen
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        msg = "land"
        msg = msg.encode()
        print(msg)
        sent = sock.sendto(msg, tello_address)
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()