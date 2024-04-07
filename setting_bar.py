from tkinter import ttk
import tkinter as tk

class SettingBar(ttk.Frame): 
    def __init__(self,parent,relx = 0,relwidth = 0.2): 
        super().__init__(parent)
        self.place(relx=relx,relwidth = relwidth, relheight=1)
        self.create_widget()


    def create_widget(self): 
        label = ttk.Label(self, text="Settings")
        add_cam_button = ttk.Button(self, text = "Add Camera")
        show_info_button = ttk.Checkbutton(self, text = "Show camera info", comman = self.toggle_show_camera_information)
        label.pack(fill = "both")
        add_cam_button.pack(fill = "both")
        show_info_button.pack(fill = "both")

    
    def toggle_show_camera_information(): 
        pass 