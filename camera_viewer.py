import tkinter as tk
from video_capture import VideoCapture
from tkinter import ttk
from tkinter import messagebox 

import time 
import cv2
from PIL import Image, ImageTk

from config import *


class MainFrame(ttk.Frame):
    """
    Frame lớn chứa các camera frame. Frame lớn được chia thành các grid 
    """
    def __init__(self, parent,relx = 0.1, relwidth = 0.8, max_row = 2, max_columns = 3, sources = []):
        super().__init__(parent)
        self.place(relx = relx,relwidth = relwidth , relheight = 1)
        self.max_row = max_row
        self.max_columns = max_columns
        self.max_cams = max_row * max_columns
        for i in range(max_row): 
            self.rowconfigure(i, weight = 1)
        for i in range(max_columns): 
            self.columnconfigure(i, weight = 1)
        self.camera_frames = []

        for i, source in enumerate(sources):
            self.add_cam(source[2],source[1], source[0],i)

        self.num_cams = i + 1
    
    def add_cam_window(self): 
        if self.num_cams >= self.max_cams: 

            messagebox.showerror("Error","Camera slots is full")
        else: 
            input_window = InputCameraWindow()




    def add_cam(self,source,camera_id,ip, num_cams):
        """
        Add các Camera Frame vào Frame chính để hiển thị các camera stream

        Arg: 
            - source(string): nguồn của camera stream
            - camera_id(string): id của camera 
            - ip(string): địa chỉ ip của camera
            - col(int), row(int): vị trí hàng và cột của camera trong main frame 
        """
        row = num_cams // self.max_columns
        col = num_cams % self.max_columns
        cameraFrame = CameraFrame(self,camera_id = camera_id,ip = ip,video_source = source) 
        cameraFrame.grid(row = row, column = col)
        self.camera_frames.append(cameraFrame)

    def stop_playing(self): 

        for camera in self.camera_frames: 
            camera.update_run_status()

    def show_cameras_information(self):
        for camera in self.camera_frames:
            camera.toggle_show_camera_information()




class CameraFrame(ttk.Frame):
    """ 
    Camera Frame để hiển thị stream. 
    """
    def __init__(self, parent, video_source=0, camera_id = "", ip = "", **kwargs):
        super().__init__(parent)
        
        self.window = parent
        self.video_source = video_source
        self.show_information = True

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

            if self.running:
                
                self.after(self.delay, self.update_frame)

    def update_run_status(self): 
        self.running = not self.running 
        if self.running: 
            self.update_frame()

    def toggle_show_camera_information(self): 
        if self.show_information:
            self.camera_id.pack()
            self.ip.pack()
        else:
            self.camera_id.pack_forget()
            self.ip.pack_forget()
        self.show_information = not self.show_information




    
class InputCameraWindow(tk.Toplevel): 
    def __init__(self): 
        super().__init__()
        self.titie("Camera adding")
        self.geometry("300x400")
        camera_id = tk.StringVar()
        self.input_camera_id = ttk.Entry(self, textvariable=camera_id)
        source = tk.StringVar()
        self.input_source = ttk.Entry(self, textvariable=source)
        ip = tk.StringVar()
        self.input_ip = ttk.Entry(self, textvariable=ip)

        self.input_camera_id.pack()
        self.input_source.pack()
        self.input_ip.pack()
        self.mainloop()
    
    
    
