'''
EYEfollow 1.0
Home Screen Class
Gian Favero and Steven Caro
December 2022
'''

import tkinter as tk
from PIL import Image, ImageTk
from tkinter.messagebox import *

class Home_Screen(tk.Frame):
    '''
    Class to represent the "Home Screen" of the application
    '''
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        
        self.controller = controller

        # Configure the screen/frame grid
        self.configure_grid()

        # Create the test option buttons
        self.VS_b = tk.Button(self, text = 'Vertical Saccade', bg = "white",
                              command=lambda: [self.onOff("Vertical_Saccade")])
        self.HS_b = tk.Button(self, text = 'Horizontal Saccade', bg = "white",
                              command=lambda: [self.onOff("Horizontal_Saccade")])
        self.SC_b = tk.Button(self, text = 'Smooth Circle', bg = "white", 
                              command=lambda: [self.onOff("Smooth_Circle")])
        self.SV_b = tk.Button(self, text = 'Smooth Vertical', bg="white",
                              command=lambda: [self.onOff("Smooth_Vertical")])
        self.SH_b = tk.Button(self, text = 'Smooth Horizontal', bg="white",
                              command=lambda: [self.onOff("Smooth_Horizontal")])
        self.start_b = tk.Button(self, text = 'START', bg = "#eee", state="disabled", height=5, width=20, 
                              command=lambda:self.controller.create_test_routine())

        # Place logo png
        logo_image = Image.open("Logo.png")
        logo_photo_image = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(self, image=logo_photo_image, bg="white")
        logo_label.image = logo_photo_image

        logo_label.grid(row=0, columnspan=20, pady=100)

        # Layout the test option buttons nicely in the frame
        self.VS_b.grid(row=1, column=2, padx=10)
        self.HS_b.grid(row=1, column=3, padx=10)
        self.SC_b.grid(row=1, column=4, padx=10)
        self.SV_b.grid(row=1, column=5, padx=10)
        self.SH_b.grid(row=1, column=6, padx=10)
        self.start_b.grid(row=3, column=0, columnspan = 8, pady=75)

    def configure_grid(self):
        '''
        Configure the grid and background colour of the Home Screen
        '''
        self.configure(bg="white")
        #self.grid_rowconfigure(0, weight=1)
        #self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(7, weight=1)
        
    def onOff(self, button_name, reset=0):
        '''
        Event handler for the press of a test option button
        Desired behaviour: Change button colour, "activate" button in controlling class
        '''
        self.controller.activate_button(button_name)            

        if self.controller.activeButtons[button_name] is True:
            if button_name =="Vertical_Saccade":
                self.VS_b.configure(bg="#adffab")
            elif button_name == "Horizontal_Saccade":
                self.HS_b.configure(bg="#adffab")
            elif button_name == "Smooth_Circle":
                self.SC_b.configure(bg="#adffab")
            elif button_name == "Smooth_Vertical":
                self.SV_b.configure(bg="#adffab")
            elif button_name == "Smooth_Horizontal":
                self.SH_b.configure(bg="#adffab")
        else:
            if button_name == "Vertical_Saccade":
                self.VS_b.configure(bg="white")
            elif button_name == "Horizontal_Saccade":
                self.HS_b.configure(bg="white")
            elif button_name == "Smooth_Circle":
                self.SC_b.configure(bg="white")
            elif button_name == "Smooth_Vertical":
                self.SV_b.configure(bg="white")
            elif button_name == "Smooth_Horizontal":
                self.SH_b.configure(bg="white")

        self.start_b.configure(state="disabled", bg="#eee")

        for item in self.controller.activeButtons:
            if self.controller.activeButtons[item] is True:
                self.start_b.configure(state="normal", bg="#adffab")
                break

    def reset_buttons(self):
        self.VS_b.configure(bg="white")
        self.HS_b.configure(bg="white")
        self.SC_b.configure(bg="white")
        self.SV_b.configure(bg="white")
        self.SH_b.configure(bg="white")
        self.start_b.configure(state="disabled", bg="#eee")

class Test_Routine_Canvas(tk.Canvas):
    '''
    Class to represent the "Main Canvas" of the application. Hosts the ball
    '''
    def __init__(self, master, controller):
        tk.Canvas.__init__(self, master)
        self.controller = controller
        self.config(height=controller.height, width=controller.width, bg="black")

