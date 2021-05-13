# -*- coding: utf-8 -*-
"""
Class definition of YOLO_v3 style detection model on image and video
"""
import cv2
import OperationMysql as mySql

img = cv2.imread('images/test.jpg')
op_mysql = mySql.OperationMysql()

#print(img.shape)
#windowName：选择的区域被命名
for num in range(1,10):
    roi = cv2.selectROI(windowName='roi' , img=img, showCrosshair=True, fromCenter=False)
    #x, y, w, h = (96, 84, 63, 29)
    x, y, w, h = roi

    print(x, y, w, h)

    cv2.rectangle(img=img, pt1=(x, y), pt2=(x + w, y + h), color=(0, 0, 255), thickness=1)
    op_mysql = mySql.OperationMysql()
    res = op_mysql.insert_one('insert led_roi (x_length,y_length,w_length,h_length) values ({0},{1},{2},{3})'.format(x, y, w, h))

#cv2.rectangle(img, (left, top), (right, bottom), color=(0, 255, 0),lineType=2, thickness=8)
#print(img_roi.shape)
#截取ROI
#cv2.rectangle(img=img, pt1=(x, y), pt2=(x + w, y + h), color=(0, 0, 255), thickness=2)
#cv2.imshow('roi', img)
#cv2.imshow('imageHSV',img_roi)



cv2.waitKey(0)

cv2.destroyAllWindows()