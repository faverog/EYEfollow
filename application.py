'''
EYEfollow 1.0
Application Class
Gian Favero and Steven Caro
2022
'''

# Python Imports
from enum import Enum
import os
import sys
from time import sleep
import ctypes
import traceback

# Module Imports
import pygetwindow as gw
import tkinter as tk
from tkinter.constants import CENTER
from tkinter.messagebox import *
from tkinter.simpledialog import askstring

# Project Imports
from testroutine import Test_Routine, Routine_State
from frames import Home_Screen, Test_Routine_Canvas

# Set resolution for screen
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# Window title
window_title = "EYEfollow, 2022"

class Application(tk.Tk):

    class CURRENT_FRAME(Enum):
        HOME      = 1
        EYE_TEST  = 2
        COUNTDOWN = 3
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title(window_title)

        # Take path to save data from command line
        self.path = sys.argv[1]
        
        # Create container for application
        self.container = self.configure_container()

        # Configure screen/window attributes
        self.configure_screen_attributes()
        self.EYEfollow_window = gw.getWindowsWithTitle(window_title)[0]
        self.gazepoint_window = gw.getWindowsWithTitle("Gazepoint")[0]

        # Configure key bindings
        self.configure_binds()

        # Create the prompt button array
        self.activeButtons = {
            "Vertical_Saccade": False,
            "Horizontal_Saccade": False,
            "Smooth_Circle": False,
            "Smooth_Vertical": False,
            "Smooth_Horizontal": False
        }

        # Create an instance of the Home Screen frame
        self.frame = Home_Screen(master=self.container, controller=self)

        # Create an instance of the test routine canvas
        self.test_routine_canvas = Test_Routine_Canvas(master=self.container, controller=self)

        # Create an instance of a test routine object (displayed on test_routine_canvas)
        self.test_routine = Test_Routine(self, self.test_routine_canvas)

        # Show the home screen
        self.show_home()

        self.update_idletasks()

    def configure_container(self):
        '''
        Define the container and grid of the application
        '''
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        return container

    def configure_screen_attributes(self):
        '''
        Configure the sizing and attributes of the screen window
        '''
        self.attributes("-fullscreen", True)
        self.resizable(False, False)
        self.update_idletasks()
        self.width = self.winfo_width()
        self.height = self.winfo_height()

    def configure_binds(self):
        '''
        Set up key bindings for program
        '''
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)
        self.bind("<q>", self.quit_routine)
        
    def toggle_fullscreen(self, event=None):
        '''
        Toggle window size to fullscreen
        '''
        self.attributes("-fullscreen", True)
        self.width = self.winfo_width()
        self.height = self.winfo_height()

    def end_fullscreen(self, event=None):
        '''
        Toggle window size to minimized
        '''
        self.attributes("-fullscreen", False)
        self.state("zoomed")
        self.config(cursor="arrow")
        self.width = self.winfo_width()
        self.height = self.winfo_height()
    
    def show_canvas(self, canvas: tk.Canvas, current_frame: CURRENT_FRAME):
        '''
        Raise the Test Routine Canvas to the top of the stack and start test routine
        '''
        canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.canvas = canvas
        tk.Misc.lift(canvas)
        self.current_frame = current_frame
        self.update_idletasks()

    def show_home(self):
        '''
        Raise the Home Screen to the top of the stack
        '''
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.tkraise()
        self.current_frame = self.CURRENT_FRAME.HOME

    def quit_routine(self, event=None):
        '''
        End a vision test routine prematurely
        '''
        if self.current_frame == self.CURRENT_FRAME.EYE_TEST:
            answer = askyesno(title='Quit Routine',
                    message='Are you sure you want to quit?')
            if answer:
                self.frame.tkraise()
                self.config(cursor="arrow")
                self.test_routine.cancel()

                self.reset_buttons()

                self.current_frame = self.CURRENT_FRAME.HOME
    
    def routine_finished(self, event=None):
        '''
        Define exit behaviour once the selected vision therapy tests have been completed
        '''
        answer = showinfo(title="Completion", message="Eye Test Complete")
        if answer:
            self.frame.tkraise() 

            self.activeButtons = {"Vertical_Saccade" : True, "Horizontal_Saccade" : True, 
                                "Smooth_Circle" : True,    "Smooth_Vertical" : True, 
                                "Smooth_Horizontal" : True}
            
            # Reset the home screen buttons
            self.reset_buttons()

            # Return the arrow cursor
            self.config(cursor="arrow")

            self.current_frame = self.CURRENT_FRAME.HOME
        
    def activate_button(self, button_name):
        '''
        Activate a button on the prompt menu
        '''
        if self.activeButtons[button_name] is False:
            self.activeButtons[button_name] = True
        else:
            self.activeButtons[button_name] = False

    def reset_buttons(self):
        '''
        Reset the prompt menu buttons
        '''
        for key in self.activeButtons.keys():
            self.activeButtons[key] = False
        
        self.frame.reset_buttons()

    def create_test_routine(self):
        '''
        Create the array of routines selected for the current sequence of vision tests
        '''
        # Bring calibration window to the forefront
        self.activate_gazepoint()

        while gw.getActiveWindowTitle() == "Gazepoint Control x64" and not None:
            sleep(10e-2)

        # Get participant's name
        participant_name = askstring("Input Name", f"Input Participant's Name{30*' '}")

        if participant_name is None:
            self.reset_buttons()
            self.EYEfollow_window.activate()
        else:
            if participant_name == '':
                participant_name = "Sample_Participant"

            # Activate EYEfollow window
            self.EYEfollow_window.activate()

            # Hide mouse
            self.config(cursor="none")

            # Display the test routine canvas 
            self.show_canvas(self.test_routine_canvas, self.CURRENT_FRAME.EYE_TEST)

            # Add the selected test options to a list
            tests = []
            for key, item in self.activeButtons.items():
                if item is True:
                    tests.append(key)
            
            # Pass the participant name and list to the Test Routine and update the test_routine state
            self.test_routine.participant_name = participant_name
            self.test_routine.test_names = iter(tests)
            self.test_routine.current_test = next(self.test_routine.test_names)
            self.test_routine.state = Routine_State.update_test

    def activate_gazepoint(self):
        # Check if window was accidentally closed
        self.gazepoint_window = None if "Gazepoint Control x64" not in gw.getAllTitles() else self.gazepoint_window

        try:
            if self.gazepoint_window is None:
                os.startfile('C:/Program Files (x86)/Gazepoint/Gazepoint/bin64/Gazepoint.exe')
                sleep(2)
                self.gazepoint_window = gw.getWindowsWithTitle("Gazepoint")[0]
            else:
                self.gazepoint_window.activate()
                sleep(0.2)
        except:
            traceback.print_exc()

if __name__ == '__main__':
    # Start Gazepoint Control
    try:
        os.startfile('C:/Program Files (x86)/Gazepoint/Gazepoint/bin64/Gazepoint.exe')
        sleep(2)
    except:
        traceback.print_exc()

    app = Application()
    app.mainloop()

    # Close Gazepoint Control
    try:
        os.system("TASKKILL /IM Gazepoint.exe")
    except:
        traceback.print_exc()
