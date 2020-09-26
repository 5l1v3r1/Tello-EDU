import socket
import cv2

tello_video = cv2.VideoCapture("udp://@0.0.0.0:11111")

while True:
    try:
        ret, frame = tello_video.read()
        if ret:
            cv2.imshow("", frame)
            cv2.waitKey(1)
    except Exception as err:
        tello_video.release()
        cv2.destroyAllWindows()
        print(err)