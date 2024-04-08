from tkinter import ttk
import tkinter as tk

class SettingBar(ttk.Frame): 
    def __init__(self,parent,relx = 0,relwidth = 0.2): 
        super().__init__(parent)
        self.place(relx=relx,relwidth = relwidth, relheight=1)
        self.create_widget(parent)


    def create_widget(self, parent): 
        label = ttk.Label(self, text="Settings")

        add_cam_button = ttk.Button(self, text = "Add Camera", command  = parent.main.add_cam_window)
        stop_button = ttk.Button(self, text = "Stop", command  = parent.main.stop_playing)
        show_info_button = ttk.Checkbutton(self, text = "Camera info" ,command = parent.main.show_cameras_information)
        
        label.pack(fill = "both",padx = 2)
        add_cam_button.pack(fill = "both",padx = 2)
        show_info_button.pack(fill = "both",padx = 2)
        stop_button.pack(fill = "both",padx = 2)

    