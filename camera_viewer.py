import tkinter as tk
from video_capture import VideoCapture
from tkinter import ttk

import time 
import cv2
from PIL import Image, ImageTk

from config import *


class MainFrame(ttk.Frame):
    """
    Frame lớn chứa các camera frame. Frame lớn được chia thành các grid 
    """
    def __init__(self, parent,relx = 0.1, relwidth = 0.8, max_row = 2, max_columns = 3):
        super().__init__(parent)
        self.place(relx = relx,relwidth = relwidth , relheight = 1)

        for i in range(max_row): 
            self.rowconfigure(i, weight = 1)
        for i in range(max_columns): 
            self.columnconfigure(i, weight = 1)
        self.camera_frames = []

    def add_cam(self,source,camera_id,ip, row, col):
        """
        Add các Camera Frame vào Frame chính để hiển thị các camera stream

        Arg: 
            - source(string): nguồn của camera stream
            - camera_id(string): id của camera 
            - ip(string): địa chỉ ip của camera
            - col(int), row(int): vị trí hàng và cột của camera trong main frame 
        """

        cameraFrame = CameraFrame(self,camera_id = camera_id,ip = ip,video_source = source) 
        cameraFrame.grid(row = row, column = col)
        self.camera_frames.append(cameraFrame)


class CameraFrame(ttk.Frame):
    """ 
    Camera Frame để hiển thị stream. 
    """
    def __init__(self, parent, video_source=0, camera_id = "", ip = "", **kwargs):
        super().__init__(parent)
        
        self.window = parent
        self.video_source = video_source


        self.vid = VideoCapture(self.video_source,width = CAMERA_WIDTH, height = CAMERA_HEIGHT)
        self.canvas = tk.Canvas(self, width=CAMERA_WIDTH, height=CAMERA_HEIGHT)
        
        self.camera_id = ttk.Label(self,text = f"Camera: {camera_id}" )
        self.ip = ttk.Label(self,text = f"ip: {ip}")
        
        # Hiển thị thông tin camera
        self.canvas.pack(side = "top")
        self.camera_id.pack(side = "top")
        self.ip.pack(side = "top")


        if "delay" in kwargs: 
            self.delay = kwargs["delay"]
        else: 
            self.delay = 15
        self.running = True
        self.update_frame()
    
    def update_frame(self):
            """TODO: add docstring"""

            # widgets in tkinter already have method `update()` so I have to use different name -

            # Get a frame from the video source
            ret, frame = self.vid.get_frame()

            if ret:
                self.image = frame
                self.photo = ImageTk.PhotoImage(image=self.image)
                self.canvas.create_image(0, 0, image=self.photo, anchor='nw')

            self.after(self.delay, self.update_frame)


