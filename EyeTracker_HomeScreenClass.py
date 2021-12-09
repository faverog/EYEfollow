'''
EYEfollow 1.0
Home Screen Class
Gian Favero and Steven Caro
December 2021
'''

import tkinter as tk
from tkinter.messagebox import *
from PIL import ImageTk, Image

import EyeTracker_BallClass as Ball

class Home_Screen(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.configure(bg="white")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(7, weight=1)

        self.VS_b = tk.Button(self, text = 'Vertical Saccade', bg = "white",
                              command=lambda: [controller.activate_button("Vertical_Saccade"), self.onOff("Vertical_Saccade")])
        self.HS_b = tk.Button(self, text = 'Horizontal Saccade', bg = "white",
                              command=lambda: [controller.activate_button("Horizontal_Saccade"), self.onOff("Horizontal_Saccade")])
        self.SC_b = tk.Button(self, text = 'Smooth Circle', bg = "white", 
                              command=lambda: [controller.activate_button("Smooth_Circle"), self.onOff("Smooth_Circle")])
        self.SV_b = tk.Button(self, text = 'Smooth Vertical', bg="white",
                              command=lambda: [controller.activate_button("Smooth_Vertical"), self.onOff("Smooth_Vertical")])
        self.SH_b = tk.Button(self, text = 'Smooth Horizontal', bg="white",
                              command=lambda: [controller.activate_button("Smooth_Horizontal"), self.onOff("Smooth_Horizontal")])
        self.start_b = tk.Button(self, text = 'START', bg = "#eee", state="disabled", height=5, width=20, command=lambda:controller.show_canvas())

        self.VS_b.grid(row=1, column=2, padx=10)
        self.HS_b.grid(row=1, column=3, padx=10)
        self.SC_b.grid(row=1, column=4, padx=10)
        self.SV_b.grid(row=1, column=5, padx=10)
        self.SH_b.grid(row=1, column=6, padx=10)
        self.start_b.grid(row=2, column=0, columnspan = 8, pady=75)
        
    def onOff(self, buttonName):        
        if self.controller.activeButtons[buttonName] is True:
            match buttonName:
                case "Vertical_Saccade":
                    self.VS_b.configure(bg="#adffab")
                case "Horizontal_Saccade":
                    self.HS_b.configure(bg="#adffab")
                case "Smooth_Circle":
                    self.SC_b.configure(bg="#adffab")
                case "Smooth_Vertical":
                    self.SV_b.configure(bg="#adffab")
                case "Smooth_Horizontal":
                    self.SH_b.configure(bg="#adffab")
        else:
            match buttonName:
                case "Vertical_Saccade":
                    self.VS_b.configure(bg="white")
                case "Horizontal_Saccade":
                    self.HS_b.configure(bg="white")
                case "Smooth_Circle":
                    self.SC_b.configure(bg="white")
                case "Smooth_Vertical":
                    self.SV_b.configure(bg="white")
                case "Smooth_Horizontal":
                    self.SH_b.configure(bg="white")

        self.start_b.configure(state="disabled", bg="#eee")

        for item in self.controller.activeButtons:
            if self.controller.activeButtons[item] is True:
                self.start_b.configure(state="normal", bg="#adffab")
                break