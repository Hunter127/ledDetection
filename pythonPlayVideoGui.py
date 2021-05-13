# -*- coding: utf-8 -*-
"""
Class definition of YOLO_v3 style detection model on image and video
"""
import cv2
import subprocess as sp
from roiTestBack2 import get_color

rtmpUrl = "rtmp://192.168.1.149/push/"
camera_path = "rtmp://58.200.131.2:1935/livetv/cctv10"
# 0是笔记本内置摄像头
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("images/6.mp4")
# cap = cv2.VideoCapture(camera_path)


while cap.isOpened():
    ret, frame = cap.read()

    x2, y2, w2, h2 = (420, 304, 48, 35)
    img_roi2 = frame[int(y2):int(y2 + h2), int(x2):int(x2 + w2)]
    cv2.rectangle(img=frame, pt1=(x2, y2), pt2=(x2 + w2, y2 + h2), color=(0, 0, 255), thickness=1)
    color = get_color(img_roi2)
    cv2.putText(frame, '{0}'.format(color),
               (x2 + 50, y2),
               cv2.FONT_HERSHEY_SIMPLEX,
               1.2, (0, 0, 255), 4,
               cv2.LINE_AA)

    cv2.imshow('frame', frame)
    c = cv2.waitKey(1)
    if c == 27:
        break


cap.release()
cv2.destroyAllWindows()