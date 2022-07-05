'''
EYEfollow 1.0
Application Class
Gian Favero and Steven Caro
December 2022
'''

# Python Imports
from enum import Enum
import tkinter as tk
from tkinter.constants import CENTER
from tkinter.messagebox import *
import ctypes

# Project Imports
from testroutine import Test_Routine, Routine_State
from frames import Home_Screen, Test_Routine_Canvas

# Set resolution for screen
ctypes.windll.shcore.SetProcessDpiAwareness(1)

class Application(tk.Tk):

    class CURRENT_FRAME(Enum):
        HOME      = 1
        EYE_TEST  = 2
        COUNTDOWN = 3
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("EyeFollow, FC 2021")

        # Create container for application
        self.container = self.configure_container()

        # Configure screen/window attributes
        self.configure_screen_attributes()

        # Configure key bindings
        self.configure_binds()

        # Create the prompt button array
        self.activeButtons = {"Vertical_Saccade" : False, "Horizontal_Saccade" : False, "Smooth_Circle" : False,
                              "Smooth_Vertical" : False, "Smooth_Horizontal" : False}

        # Create an instance of the Home Screen frame
        self.frame = Home_Screen(master=self.container, controller=self)

        # Create an instance of the test routine canvas
        self.test_routine_canvas = Test_Routine_Canvas(master=self.container, controller=self)

        # Create an instance of the test routine canvas
        self.ball = Test_Routine(self, self.test_routine_canvas)

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
        # Display the test routine canvas 
        self.show_canvas(self.test_routine_canvas, self.CURRENT_FRAME.EYE_TEST)

        # Add the selected test options to a list
        tests = []
        for key, item in self.activeButtons.items():
            if item is True:
                tests.append(key)
        
        # Pass the list to the Ball_Object and update ball state
        self.ball.test_names = iter(tests)
        self.ball.state = Routine_State.update_test

if __name__ == '__main__':
    app = Application()
    app.mainloop()