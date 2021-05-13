# -*- coding: utf-8 -*-
"""
双线程
手工定位roi区域
处理roi区域后将结果写入管道中+将识别异常结果写入mysql中（待实现）
通向nginx直播服务器
最终在页面获取rtmp直播画面+mysql中的识别异常结果

author: huiyuan.huang
project:指示灯识别项目
desc；缺陷是不能智能识别led灯的区域，后期加入yolo来实现智能定位。暂时通过手动方式来定位roi区域来进行检测
createTime:2021-05-08 17:10

视频流

"""
import queue
import threading
import cv2 as cv
import subprocess as sp
from roiTestBack2 import get_color
import OperationMysql as mySql
from time import sleep


class Live(object):
    def __init__(self):
        self.frame_queue = queue.Queue()
        self.command = ""
        # 自行设置
        self.rtmpUrl = "rtmp://192.168.1.149/push/"
        self.camera_path = "rtmp://58.200.131.2:1935/livetv/cctv10"
        self.list_roi = []
        # self.get_roi()

    def read_frame(self):
        print("开启推流")
        cap = cv.VideoCapture(self.camera_path)

        # Get video information
        fps = int(cap.get(cv.CAP_PROP_FPS))
        width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

        # ffmpeg command
        self.command = ['ffmpeg',
                        '-y',
                        '-f', 'rawvideo',
                        '-vcodec', 'rawvideo',
                        '-pix_fmt', 'bgr24',
                        '-s', "{}x{}".format(width, height),
                        '-r', str(fps),
                        '-i', '-',
                        '-c:v', 'libx264',
                        '-pix_fmt', 'yuv420p',
                        '-preset', 'ultrafast',
                        '-f', 'flv',
                        self.rtmpUrl]
        # read webcamera
        while (cap.isOpened()):
            ret, frame = cap.read()
            if not ret:
                print("Opening camera is failed")
                # 说实话这里的break应该替换为：
                # cap = cv.VideoCapture(self.camera_path)
                # 因为我这俩天遇到的项目里出现断流的毛病
                # 特别是拉取rtmp流的时候！！！！
                break

            # put frame into queue
            self.frame_queue.put(frame)

    def push_frame(self):
        # 防止多线程时 command 未被设置
        while True:
            if len(self.command) > 0:
                # 管道配置
                p = sp.Popen(self.command, stdin=sp.PIPE)
                break
        while True:
            if self.frame_queue.empty() != True:
                frame = self.frame_queue.get()
                # process frame
                # 你处理图片的代码
                for roi in self.list_roi:  # 第二个实例
                    x2, y2, w2, h2 = (roi['x_length'], roi['y_length'], roi['w_length'], roi['h_length'])
                    #print(x2, y2, w2, h2)
                    img_roi2 = frame[int(y2):int(y2 + h2), int(x2):int(x2 + w2)]
                    cv.rectangle(img=frame, pt1=(x2, y2), pt2=(x2 + w2, y2 + h2), color=(0, 0, 255), thickness=1)
                    color = get_color(img_roi2)
                    cv.putText(frame, '{0}'.format(color),
                               (x2 + 50, y2),
                               cv.FONT_HERSHEY_SIMPLEX,
                               1.2, (0, 0, 255), 4,
                               cv.LINE_AA)
                # write to pipe
                p.stdin.write(frame.tostring())

    def run(self):
        threads = [
            threading.Thread(target=Live.read_frame, args=(self,)),
            threading.Thread(target=Live.push_frame, args=(self,))
        ]
        [thread.setDaemon(True) for thread in threads]
        [thread.start() for thread in threads]


if __name__ == '__main__':

    live = Live()
    op_mysql = mySql.OperationMysql()
    res = op_mysql.search_all("SELECT *  from led_roi")
    live.list_roi = res
    live.run()
    while True:
        sleep(15)
        print(f'threading: runing...')