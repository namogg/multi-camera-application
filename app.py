import tkinter as tk
from video_capture import VideoCapture
import tkinter.ttk as ttk 
import customtkinter as ctk 
from camera_viewer import MainFrame
from tkinter.ttk import *
from setting_bar import SettingBar
from config import *


ctk.set_default_color_theme("dark-blue")
class MulticamerasApp(ctk.CTk):
    def __init__(self,title = "Multicameras App",width = 1280, height = 720,main_width = 0.9,sources = 0, max_row = 2, max_columns = 3 ,*args, **kwargs):
        super().__init__()
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.maxsize(width, width)
        
        self.width = width
        self.height = height
        self.create_theme()
        self.resizable(True, True)

        self.setting_bar = SettingBar(self,relx = 0,relwidth = (1-main_width))
        self.main = MainFrame(self,relx=(1-main_width), relwidth = main_width, max_columns= max_columns, max_row = max_row)
        
        for i, source in enumerate(sources):
            row = i // max_columns
            col = i % max_columns
            self.main.add_cam(source[2],source[1], source[0],row , col)
        self.num_cams = i
        #run application
        self.mainloop()

    def create_theme(self): 
        s = ttk.Style()
        s.theme_use('clam')


if __name__ == "__main__":
    sources = [   
        (
            "Camera 1",
            "0,0,0,0",
            "data/yt5s.io-London Walk from Oxford Street to Carnaby Street.mp4",
        ),
        (
            "Camera 2",
            "0,0,0,0",
            "data/yt5s.io-London Walk from Oxford Street to Carnaby Street.mp4",
        ),
        (
            "Camera 3",
            "0,0,0,0",
            "data/yt5s.io-London Walk from Oxford Street to Carnaby Street.mp4",
        ),
        (
            "Camera 4",
            "0,0,0,0",
            "data/yt5s.io-London Walk from Oxford Street to Carnaby Street.mp4",
        ),
        (
            "Camera 5",
            "0,0,0,0",
            "data/yt5s.io-London Walk from Oxford Street to Carnaby Street.mp4",
        ),
                (
            "Camera 6",
            "0,0,0,0",
            "data/yt5s.io-London Walk from Oxford Street to Carnaby Street.mp4",
        ),
    ]

    MulticamerasApp(sources = sources, width =APP_WIDTH, height = APP_HEIGHT)