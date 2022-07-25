'''
EYEfollow 1.0
Ball Class 
Gian Favero and Steven Caro
2022
'''

import tkinter as tk
from enum import Enum, auto
from math import pi, sin, cos
from time import time, time_ns, sleep
from open_gaze import EyeTracker
import pandas as pd

# TODO: Hide mouse

# Constants to control behaviour of the tests
routine_duration_freq    = {
    "Vertical_Saccade": {"Duration": 5, "Frequency": 0.4},
    "Horizontal_Saccade": {"Duration": 5, "Frequency": 0.4},
    "Smooth_Circle": {"Duration": 16, "Frequency": 6.5/16},
    "Smooth_Vertical": {"Duration": 22.5, "Frequency": 6.25/22.5},
    "Smooth_Horizontal": {"Duration": 27, "Frequency": 1/12},}      # s, Hz ball position update increment
#frequency           = 0.4     # Hz ball position update increment
draw_refresh_rate   = 10      # ms
countdown_duration  = 3       # s
state_machine_cycle = 100     # ms

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

        self.collect_data = False####################################################
        if self.collect_data:
            self.tracker = EyeTracker()

        # Initialize the ball (oval) shape
        self.ball_radius = 50
        self.ball = self.canvas.create_oval(0, 0, self.ball_radius, self.ball_radius, fill="white")
        self.canvas.itemconfig(self.ball, state='hidden')
        print(self.canvas.itemconfig(self.ball))

        # Initialize the countdown text items
        self.count = countdown_duration
        self.countdown_text = self.canvas.create_text(self.master.width/2, self.master.height/2, text=self.count, 
                                                      font=("Arial", 50, "bold"), fill="white")
        self.canvas.itemconfig(self.countdown_text, state='hidden')

        # Initialize the state machine variables
        self.state = Routine_State.idle
        self.current_test = None
        self.start_countdown = 0
        self.start_drawing = 0
        self.drawing_finished = 0

        # Pandas
        self.dfs = {}

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
                self.cancel()
            else:
                self.time_ref = time()
                self.start_countdown = 1
                self.state = Routine_State.countdown

                x, y = self.get_coords(self.current_test, 0) # Initialize position of ball
                self.canvas.moveto(self.ball, x, y)
                self.canvas.itemconfig(self.ball, state="normal")

        elif self.state == Routine_State.countdown:
            if self.start_countdown:
                self.update_countdown()
            else:
                self.start_drawing = 1
                self.state = Routine_State.drawing
                if self.collect_data:
                    self.start_collection()
                    
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
                    self.stop_collection()

        elif self.state == Routine_State.idle:
            pass

        self.move_ball_ref = self.canvas.after(state_machine_cycle, self.move_ball)
        
    def draw(self):
        '''
        Draws/moves the ball on the screen
        '''
        t = time_ns()/1e9 - self.time_ref
        x, y = self.get_coords(self.current_test, t)
        self.canvas.moveto(self.ball, x, y)

        if self.collect_data:
            try:
                while (msg := self.tracker.read_msg_async()) is not None:
                    self.tracker_data.append((time(), *msg))
            except:
                pass

        if t < routine_duration_freq[self.current_test]["Duration"]:
            self.draw_ref = self.canvas.after(draw_refresh_rate, self.draw)
        else:
            self.drawing_finished = 1

    def update_countdown(self):
        '''
        A function called to provide a countdown on the screen (prior to a test)
        '''
        self.canvas.itemconfig(self.countdown_text, text=f'{self.count}\nFollow the dot',state='normal')
        #self.canvas.itemconfig(self.ball, state='normal')
        self.canvas.itemconfig(self.ball, width=(3-self.count)*4)
        
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

        x = self.master.width / 2 + self.master.height*(f(t)[0]/2) - self.ball_radius / 2
        y = self.master.height*(1/2 + f(t)[1]/2) - self.ball_radius / 2
        
        return x, y 

    def vertical_saccade(self):
        return lambda t: (0, (int(routine_duration_freq["Vertical_Saccade"]["Frequency"] * t * 2) % 2 == 0) * 1.5 - 0.75)

    def horizontal_saccade(self):
        return lambda t: ((int(routine_duration_freq["Horizontal_Saccade"]["Frequency"] * t * 2) % 2 == 0) * 1.5 - 0.75, 0)

    def smooth_vertical(self):
        return lambda t: (0, 1 * cos(2 * pi * routine_duration_freq["Smooth_Vertical"]["Frequency"] * t))

    def smooth_horizontal(self):
        return lambda t: (1.5 * cos(2 * pi * routine_duration_freq["Smooth_Horizontal"]["Frequency"] * t), 0)

    def smooth_circle(self):
        return lambda t: (0.5 * sin(2 * pi * routine_duration_freq["Smooth_Circle"]["Frequency"] * t), 0.5 * cos(2 * pi * routine_duration_freq["Smooth_Circle"]["Frequency"] * t))

    def start_collection(self):
        try:
            self.tracker_data = list[tuple[float, str, dict[str, str]]]()
            self.tracker.send_data        = True
            self.tracker.send_pupil_left  = True
            self.tracker.send_pupil_right = True
            self.tracker.send_pog_left    = True
            self.tracker.send_pog_right   = True
            self.tracker.send_time        = True
        except:
            print('FAILED TO START')
            self.start_collection()
    
    def stop_collection(self):
        try:
            self.tracker.send_data        = False
            self.tracker.send_pupil_left  = False
            self.tracker.send_pupil_right = False
            self.tracker.send_pog_left    = False
            self.tracker.send_pog_right   = False
            self.tracker.send_time        = False
        except:
            print("FAILED TO STOP")
            self.stop_collection()
        while True:
            sleep(1e-2)
            if self.tracker.read_msg_async() is None:
                break
        self.tracker_data = self.serialize_tracker_data(self.tracker_data)
        self.dfs[self.current_test]=pd.DataFrame(self.tracker_data)

    def cancel(self):
        '''
        Cancel all test routines being run and reset variables
        '''
        try:
            self.draw_ref = self.canvas.after_cancel(self.draw_ref)
        except:
            pass

        self.canvas.itemconfig(self.countdown_text, state='hidden')

        self.state = Routine_State.idle
        self.current_test = None
        self.count = countdown_duration
        self.start_countdown = 0
        self.start_drawing = 0
        self.drawing_finished = 0
        
        if self.collect_data:
            self.exportData()

    def exportData(self):
        with pd.ExcelWriter("Test Results/Sample.xlsx") as writer:
            for key in self.dfs.keys():
                self.dfs[key].to_excel(writer, sheet_name=key)
    
    def serialize_tracker_data(self, data: list[tuple[float, str, dict[str, str]]]) -> str:
        result={}
        for key in [
                        "TIME",
                        "LPOGX", "LPOGY", "LPOGV",  # Sent by send_pog_left
                        "RPOGX", "RPOGY", "RPOGV",  # Sent by send_pog_right
                        "LPCX", "LPCY", "LPD", "LPS", "LPV",  # Sent by send_pupil_left
                        "RPCX", "RPCY", "RPD", "RPS", "RPV",  # Sent by send_pupil_right
                        ]:
                        result[key] = []

        for contents in data:
            try:
                if 'REC' in contents and 'TIME' in contents[2].keys():
                    for key in [
                            "TIME",
                            "LPOGX", "LPOGY", "LPOGV",  # Sent by send_pog_left
                            "RPOGX", "RPOGY", "RPOGV",  # Sent by send_pog_right
                            "LPCX", "LPCY", "LPD", "LPS", "LPV",  # Sent by send_pupil_left
                            "RPCX", "RPCY", "RPD", "RPS", "RPV",  # Sent by send_pupil_right
                            ]: 

                            result[key].append(float(contents[2][key]) if key in contents[2] else '')
            except:
                print(contents) # TODO get to the bottom of this (if program gets here, no data is written)
        return result

