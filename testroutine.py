'''
EYEfollow 1.0
Test Routine Class 
Gian Favero and Steven Caro
2022
'''

# Python Imports
from math import pi, sin, cos
from time import time, time_ns
from enum import Enum, auto
import traceback

# Module Imports
import tkinter as tk
from eyetracker import EyeTracker_DM

# Constants to control behaviour of the tests
test_params = {
    "Vertical_Saccade": {
        "Duration": 10,     # s
        "Frequency": 1,     # Hz
        "Instruction": "Look back and forth between\ndots as fast as possible"
    },
    "Horizontal_Saccade": {
        "Duration": 10, 
        "Frequency": 1,
        "Instruction": "Look back and forth between\ndots as fast as possible"
    },
    "Smooth_Circle": {
        "Duration": 16, 
        "Frequency": 6.5/16,
        "Instruction": "Follows the dot"
    },
    "Smooth_Vertical": {
        "Duration": 22.5,
        "Frequency": 3.25/22.5,
        "Instruction": "Follow the dot"
    },
    "Smooth_Horizontal": {
        "Duration": 27,
        "Frequency": 2/27,
        "Instruction": "Follow the dot"
    },
}

draw_refresh_rate   = 5       # ms
countdown_duration  = 3       # s
state_machine_cycle = 100     # ms
ball_radius = 12              # px

class Routine_State(Enum):
    '''
    Enum class for state of Ball object
    '''
    countdown   = auto()
    update_test = auto()
    drawing     = auto()
    idle        = auto()

class Test_Routine:
    '''
    Class that handles all eye-test routine related activity
    ''' 
    def __init__(self, master, canvas):
        self.master = master
        self.canvas: tk.Canvas = canvas

        # Configure data collection
        self.collect_data = True
        if self.collect_data:
            self.tracker = EyeTracker_DM(master=self)

        # Initialize the ball (oval) shapes
        self.ball_radius = ball_radius
        self.ball = self.canvas.create_oval(0, 0, self.ball_radius, self.ball_radius, fill="white")
        self.canvas.itemconfig(self.ball, state='hidden')

        self.saccade_ball = self.canvas.create_oval(0, 0, self.ball_radius, self.ball_radius, fill="white")
        self.canvas.itemconfig(self.saccade_ball, state='hidden')

        # Initialize Participant's Name
        self.participant_name = "Default Participant"

        # Initialize the countdown text items
        self.count = countdown_duration
        self.countdown_text = self.canvas.create_text(self.master.width/2, self.master.height/2, text=self.count,
                                                      font=("Arial", 35, "bold"), justify='center', fill="white")
        self.canvas.itemconfig(self.countdown_text, state='hidden')

        # Initialize/reset the state machine variables
        self.variable_reset()

        # Call 'main loop' of the class
        self.move_ball()
    
    def move_ball(self):
        '''
        Main loop for the class. Handles and transitions main state machine
        '''
        if self.state == Routine_State.update_test:
            self.current_test = next(self.test_names, "Done")
            if self.current_test == "Done":
                self.master.routine_finished()
                if self.collect_data:
                    self.tracker.export_data()
                self.cancel()
            else:
                self.time_ref = time()
                self.start_countdown = 1
                self.state = Routine_State.countdown

        elif self.state == Routine_State.countdown:
            if self.start_countdown:
                self.update_countdown()
            else:
                self.start_drawing = 1
                self.state = Routine_State.drawing
                if self.collect_data:
                    self.tracker.start_collection()
                    
        elif self.state == Routine_State.drawing:
            if self.start_drawing:
                self.start_drawing = 0
                self.time_ref = time()
                self.canvas.itemconfig(self.ball, state='normal')
                self.draw()
            elif not self.start_drawing and self.drawing_finished:
                self.drawing_finished = 0
                self.state = Routine_State.update_test
                if self.collect_data:
                    self.tracker.stop_collection()

        elif self.state == Routine_State.idle:
            pass

        self.move_ball_ref = self.canvas.after(state_machine_cycle, self.move_ball)
        
    def draw(self):
        '''
        Draws/moves the ball on the screen
        '''
        t = time_ns()/1e9 - self.time_ref

        if "Saccade" in self.current_test:
            top_ball_colour, bottom_ball_colour = self.saccade_colour_monitor()

            self.canvas.itemconfig(self.ball, fill=top_ball_colour)
            self.canvas.itemconfig(self.saccade_ball, fill=bottom_ball_colour)
        else:
            x_cen, y_cen = self.get_coords(self.current_test, t)
            self.canvas.moveto(self.ball, x_cen - self.ball_radius/2, y_cen - self.ball_radius/2)
            self.canvas.configure(bg="black")

        if self.collect_data:
            try:
                while (msg := self.tracker.read_msg_async()) is not None:
                    self.tracker.tracker_data.append((time(), *msg))
                    self.get_pog(msg)
            except:
                traceback.print_exc()
                pass

        if t < test_params[self.current_test]["Duration"]:
            self.draw_ref = self.canvas.after(draw_refresh_rate, self.draw)
        else:
            self.canvas.itemconfig(self.ball, state="hidden", fill='white')
            self.canvas.itemconfig(self.saccade_ball, state="hidden", fill='white')
            self.drawing_finished = 1

    def update_countdown(self):
        '''
        A function called to provide a countdown on the screen (prior to a test)
        '''
        radius = 50 - ((50 - self.ball_radius)/countdown_duration)*(countdown_duration-self.count)

        if "Saccade" in self.current_test:
            ball_coords, saccade_ball_coords = self.get_coords(self.current_test, 0)
            self.canvas.moveto(self.ball, ball_coords[0] - self.ball_radius/2, ball_coords[1] - self.ball_radius/2)
            self.canvas.moveto(self.saccade_ball, saccade_ball_coords[0] - self.ball_radius/2, saccade_ball_coords[1] - self.ball_radius/2)
            self.canvas.itemconfig(self.saccade_ball, state="normal")
        else:
            x_cen, y_cen = self.get_coords(self.current_test, 0)
            self.canvas.coords(self.ball, x_cen-radius/2, y_cen-radius/2, x_cen+radius/2, y_cen+radius/2)
        
        self.canvas.itemconfig(self.ball, state="normal")
        self.canvas.itemconfig(self.countdown_text, text=f'{self.count}\n{test_params[self.current_test]["Instruction"]}',state='normal')
        
        if time() - self.time_ref >= 1:  
            self.count -= 1
            self.time_ref = time()

        if self.count <= -1:
            self.start_countdown = 0
            self.canvas.itemconfig(self.countdown_text,state='hidden')
            self.count = countdown_duration
        
    def get_coords(self, test, t):
        '''
        Prescribes the coordinates of where the ball (oval) should be drawn according to test as a function of time
        test: test_name
        t: time
        '''
        if test == "Vertical_Saccade":
            f = self.vertical_saccade()
        elif test == "Horizontal_Saccade":
            f = self.horizontal_saccade()
        elif test == "Smooth_Vertical":
            f = self.smooth_vertical()
        elif test == "Smooth_Horizontal":
            f = self.smooth_horizontal()
        elif test == "Smooth_Circle":
            f = self.smooth_circle()
        
        # Saccade tests return 2 constant sets of points for the balls (on either end of screen)
        if "Saccade" in self.current_test:
            return f(t)
        # All other tests send an x-y coordinate as a function of time
        else:
            x_cen = self.master.width / 2 + self.master.height*(f(t)[0]/2)
            y_cen = self.master.height*(1/2 + f(t)[1]/2)
            
            return x_cen, y_cen 

    def vertical_saccade(self):
        # Returns one x-y set for top-middle of screen, one x-y set for bottom-middle of screen
        return lambda t: [(self.master.width / 2, self.master.height*(1/2+0.75/2)),
                          (self.master.width / 2, self.master.height*(1/2-0.75/2))]

    def horizontal_saccade(self):
        # Returns one x-y set for left-middle of screen, one x-y set for right-middle of screen
        return lambda t: [(self.master.width / 2 + self.master.height*1.5/2, self.master.height/2), 
                          (self.master.width / 2 - self.master.height*1.5/2, self.master.height/2)]

    def smooth_vertical(self):
        return lambda t: (0, 0.95 * cos(2 * pi * test_params["Smooth_Vertical"]["Frequency"] * t))

    def smooth_horizontal(self):
        return lambda t: (1.5 * cos(2 * pi * test_params["Smooth_Horizontal"]["Frequency"] * t), 0)

    def smooth_circle(self):
        return lambda t: (0.5 * cos(2 * pi * test_params["Smooth_Circle"]["Frequency"] * t), 0.5 * sin(2 * pi * test_params["Smooth_Circle"]["Frequency"] * t))

    def get_pog(self, msg):
        '''
        Get live right/left POG data
        '''
        if "TIME" in msg[1].keys():
            self.left_eye_pog = [float(msg[1]["LPOGX"]), float(msg[1]["LPOGY"])]
            self.right_eye_pog = [float(msg[1]["RPOGX"]), float(msg[1]["RPOGY"])]
        else:
            self.left_eye_pog = [0, 0]
            self.right_eye_pog = [0, 0]

    def saccade_colour_monitor(self):
        '''
        Monitors the left and right POG during a saccade test and returns the colour of the balls
        If participant is looking at a ball, turn it green
        '''
        if self.current_test == "Vertical_Saccade":
            if self.right_eye_pog[1] > 0.55 and self.left_eye_pog[1] > 0.55:
                top_ball_colour = "green"
                bottom_ball_colour = "white"
            elif self.right_eye_pog[1] < 0.55 and self.left_eye_pog[1] < 0.55:
                top_ball_colour = "white"
                bottom_ball_colour = "green"
            else:
                top_ball_colour = "white"
                bottom_ball_colour = "white"
        elif self.current_test == "Horizontal_Saccade":
            if self.right_eye_pog[0] > 0.55 and self.left_eye_pog[0] > 0.55:
                top_ball_colour = "green"
                bottom_ball_colour = "white"
            elif self.right_eye_pog[0] < 0.55 and self.left_eye_pog[0] < 0.55:
                top_ball_colour = "white"
                bottom_ball_colour = "green"
            else:
                top_ball_colour = "white"
                bottom_ball_colour = "white"

        return top_ball_colour, bottom_ball_colour

    def variable_reset(self):
        # Reset the data collection variables
        self.tracker.dfs = {}
        self.left_eye_pog = [0, 0]
        self.right_eye_pog = [0, 0]

        # Reset the state machine variables
        self.state = Routine_State.idle
        self.test_names = []
        self.current_test = None
        self.tracker.current_test = None
        self.start_countdown = 0
        self.start_drawing = 0
        self.drawing_finished = 0
    
    def cancel(self):
        '''
        Cancels all test routines being run and reset variables
        '''
        try:
            self.draw_ref = self.canvas.after_cancel(self.draw_ref)
        except:
            pass

        # Stop data collection
        if self.collect_data and self.state is not Routine_State.countdown:    
            self.tracker.stop_collection()
        
        # Ensure the moving ball and the countdown text are hidden
        self.canvas.itemconfig(self.countdown_text, state='hidden')
        self.canvas.itemconfig(self.ball, state="hidden")
        self.canvas.coords(self.ball, 0, 0, self.ball_radius, self.ball_radius)
        self.canvas.itemconfig(self.saccade_ball, state="hidden")

        # Reset state and test variables
        self.variable_reset()
