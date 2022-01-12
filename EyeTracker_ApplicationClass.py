'''
EYEfollow 1.0
Application Class
Gian Favero and Steven Caro
December 2021
'''

import tkinter as tk
from tkinter.constants import CENTER
from tkinter.messagebox import *
import ctypes

from EyeTracker_BallClass import Ball
from EyeTracker_HomeScreenClass import Home_Screen
from EyeTracker_MainCanvasClass import Main_Canvas

# Set resolution for screen
ctypes.windll.shcore.SetProcessDpiAwareness(1)

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("EyeFollow, FC 2021")
        self.answer = False
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.attributes("-fullscreen", True)
        self.resizable(False, False)
        self.update_idletasks()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)
        self.bind("<q>", self.quit_routine)
        
        self.frame = Home_Screen(master=container, controller=self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.tkraise()

        self.main_canvas = Main_Canvas(master=container, controller=self)

        self.activeButtons = {"Vertical_Saccade" : False, "Horizontal_Saccade" : False, "Smooth_Circle" : False,
                            "Smooth_Vertical" : False, "Smooth_Horizontal" : False}

        self.ball = Ball(self, self.main_canvas, 15)
        
    def toggle_fullscreen(self, event=None):
        self.attributes("-fullscreen", True)
        self.update_idletasks()
        self.width = self.winfo_width()
        self.height = self.winfo_height()

    def end_fullscreen(self, event=None):
        self.attributes("-fullscreen", False)
        self.state("zoomed")
        self.config(cursor="arrow")
        self.update_idletasks()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
    
    def show_canvas(self):
        '''Show the main canvas'''
        self.main_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        tk.Misc.lift(self.main_canvas)
        self.test_routine()

    def quit_routine(self, event=None):
        self.answer = askyesno(title='Quit Routine',
                message='Are you sure you want to quit?')
        if self.answer:
            self.frame.tkraise()
            self.config(cursor="arrow")
            self.activeButtons = {"Vertical_Saccade" : False, "Horizontal_Saccade" : False, "Smooth_Circle" : False,
                                    "Smooth_Vertical" : False, "Smooth_Horizontal" : False}
            for key in self.activeButtons.keys():
                self.frame.onOff(key)
    
    def routine_finished(self, event=None):
        answer = showinfo(title="Completion", message="Eye Test Complete")
        if answer:
            self.frame.tkraise() 
            self.activeButtons = {"Vertical_Saccade" : False, "Horizontal_Saccade" : False, "Smooth_Circle" : False,
                                    "Smooth_Vertical" : False, "Smooth_Horizontal" : False}
            for key in self.activeButtons.keys():
                self.frame.onOff(key)
        
    def activate_button(self, page_name):
        if self.activeButtons[page_name] is False:
            self.activeButtons[page_name] = True
        else:
            self.activeButtons[page_name] = False

    # Also add calibration at beginning
    def test_routine(self):
        allFalse = True
        for key, item in self.activeButtons.items():
            if item is True:
                allFalse=False
                self.config(cursor="none")
                self.ball.set_test(key)
                self.ball.move_ball()
                break
        if allFalse is True:
            self.routine_finished()
            self.config(cursor="arrow")

if __name__ == '__main__':
    app = Application()
    app.mainloop()