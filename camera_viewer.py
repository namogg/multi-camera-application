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
        self.num_cams = 0
        for i in range(max_row): 
            self.rowconfigure(i, weight = 1)
        for i in range(max_columns): 
            self.columnconfigure(i, weight = 1)
        self.camera_frames = []

        for i, source in enumerate(sources):
            self.add_cam(source[2],source[1], source[0])

      
    
    def add_cam_window(self): 
        if self.allow_camera_add():
            InputCameraWindow(self)
            return True
        return False
        


    def allow_camera_add(self):
        """
        Kiểm tra điều kiện add camera. Nếu số lượng cam lớn hơn số lượng cam cho phép thì thông báo
        """
        if self.num_cams >= self.max_cams: 
            messagebox.showerror("Error","Camera slots is full")
            return False
        else:
            return True

    def add_cam(self,source,ip,camera_id):
        """
        Add các Camera Frame vào Frame chính để hiển thị các camera stream

        Arg: 
            - source(string): nguồn của camera stream
            - camera_id(string): id của camera 
            - ip(string): địa chỉ ip của camera
            - col(int), row(int): vị trí hàng và cột của camera trong main frame 
        """
        if self.allow_camera_add():
            row = self.num_cams // self.max_columns
            col = self.num_cams % self.max_columns
            cameraFrame = CameraFrame(self,camera_id = camera_id,ip = ip,video_source = source) 
            cameraFrame.grid(row = row, column = col)
            self.camera_frames.append(cameraFrame)
            self.num_cams += 1
            return True
        else:
            return False

    def stop_playing(self): 
        """
        Tạm dừng video trên main frame. 
        """
        for camera in self.camera_frames: 
            camera.update_run_status()

    def show_cameras_information(self):
        """"
        Hiển thị thông tin camera
        """
        for camera in self.camera_frames:
            camera.toggle_show_camera_information()




class CameraFrame(ttk.Frame):
    """ 
    Camera Frame để hiển thị stream. 
    """
    def __init__(self, parent, video_source=0, camera_id = "", ip = "", **kwargs):
        super().__init__(parent)
        
        self.parent = parent
        self.video_source = video_source
        self.show_information = True

        self.vid = VideoCapture(self.video_source,width = CAMERA_WIDTH, height = CAMERA_HEIGHT)
        if not self.vid.vid.isOpened(): 
            messagebox.showerror("Error","Source not found")
            raise ValueError("[MyVideoCapture] Unable to open video source", video_source)
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
        """
        Update frame ở canvas
        """
        ret, frame = self.vid.get_frame()

        if ret:
            self.image = frame
            self.photo = ImageTk.PhotoImage(image=self.image)
            self.canvas.create_image(0, 0, image=self.photo, anchor='nw')

        # Nếu self.running = True thì tiép tục update
        if self.running:
            self.after(self.delay, self.update_frame)

    def update_run_status(self): 
        """
        Cập nhập thuộc tính running
        """
        self.running = not self.running 
        if self.running: 
            self.update_frame()

    def toggle_show_camera_information(self): 
        """
        Bật tắt thông tin camera
        """
        if self.show_information:
            self.camera_id.pack()
            self.ip.pack()
        else:
            self.camera_id.pack_forget()
            self.ip.pack_forget()
        self.show_information = not self.show_information




    
class InputCameraWindow(tk.Toplevel): 
    """
    Window form nhập thông tin add camera: source, id, ip
    """
    def __init__(self,parent): 
        super().__init__()

        self.parent = parent
        self.title("Camera adding")
        self.geometry("300x150")
        
        # Cài đặt grid 
        self.columnconfigure((0,1), weight=1)
        self.rowconfigure((0,1,2), weight=1)

        # Entry 
        camera_id = tk.StringVar()
        self.input_camera_id = ttk.Entry(self, textvariable=camera_id)
        source = tk.StringVar()
        self.input_source = ttk.Entry(self, textvariable=source)
        ip = tk.StringVar()
        self.input_ip = ttk.Entry(self, textvariable=ip)
        
        #Label 
        self.camera_id_label = ttk.Label(self, text="Camera ID")
        self.source_label = ttk.Label(self, text="Source")
        self.ip_label = ttk.Label(self, text="IP")
        
        # Đặt các label và entry vào các grid
        self.camera_id_label.grid(row = 0, column =  0, sticky="e")
        self.input_camera_id.grid(row = 0, column = 1,sticky="w")
        
        self.source_label.grid(row = 1, column =  0, sticky="e")
        self.input_source.grid(row = 1, column = 1,sticky="w")

        self.ip_label.grid(row = 2, column =  0, sticky="e")
        self.input_ip.grid(row = 2, column = 1,sticky="w")

        # Submit button 
        self.submit_button = ttk.Button(self, text="Submit", command=self.submit_data)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10) 
        self.mainloop()
    
    def submit_data(self):
        camera_id = self.input_camera_id.get()
        source = self.input_source.get()
        ip = self.input_ip.get()
        status =  self.parent.add_cam(source = source, camera_id = camera_id, ip = ip)
        if status:
            messagebox.showinfo(f"Added camera", "Camera with {source} was added")
            self.destroy()

        
    
