'''
EYEfollow 1.0
Ball Class 
Gian Favero and Steven Caro
2022
'''

from math import pi, sin, cos
from time import time
import tkinter as tk

routine_duration = 15      # s
refresh_rate     = 1       # ms
frequency        = 0.5     # Hz

class Ball_Object: 
    def __init__(self, master, canvas, size):
        self.master = master
        self.canvas: tk.Canvas = canvas
        self.size = size
        self.ball = self.canvas.create_oval(0, 0, self.size, self.size, fill="white")

        # Initialize the countdown items
        self.count = 5
        self.countdown_text = self.canvas.create_text(self.master.width/2, self.master.height/2, text=self.count, 
                                                      font=("Arial", 50, "bold"), fill="white")
        self.canvas.itemconfig(self.countdown_text, state='hidden')

    def run_tests(self):
        self.start_countdown()
        self.move_ball()
    
    def move_ball(self):
        if self.countdown_complete:
            try:
                self.current_test = next(self.test_names)
                self.time_ref = time()
                self.draw()
            except StopIteration:
                self.test_names = []
                self.cancel()
                self.master.routine_finished()
        
        self.move_ball_ref = self.canvas.after((routine_duration + 5) * 1000, self.move_ball)

    def draw(self):
        t = time() - self.time_ref
        x, y = self.get_coords(self.current_test, t)
        self.canvas.moveto(self.ball, x, y)

        if t < routine_duration + 5:
            self.draw_ref = self.canvas.after(refresh_rate, self.draw)
        else:
            self.canvas.moveto(self.ball, self.master.width / 2, self.master.height / 2)

    def start_countdown(self):
        self.canvas.itemconfig(self.countdown_text, text=self.count,state='normal')
        self.count -= 1

        if self.count > -1:
            self.countdown_complete = False
            self.canvas.after(1 * 1000, self.start_countdown)
        else:
            self.countdown_complete = True            
            self.canvas.itemconfig(self.countdown_text,state='hidden')
            self.count = 5
        
    def get_coords(self, test, t):
        match test:
            case "Vertical_Saccade":
                f = self.vertical_saccade()
            case "Horizontal_Saccade":
                f = self.horizontal_saccade()
            case "Smooth_Vertical":
                f = self.smooth_vertical()
            case "Smooth_Horizontal":
                f = self.smooth_horizontal()
            case "Smooth_Circle":
                f = self.smooth_circle()

        x = self.master.width / 2 + self.master.height*(f(t)[0]/2) - self.size / 2
        y = self.master.height*(1/2 + f(t)[1]/2) - self.size / 2
        
        return x, y 

    def cancel(self):
        '''
        Cancel all test routines being run
        '''
        self.canvas.after_cancel(self.move_ball_ref)
        self.canvas.after_cancel(self.draw_ref)

    def vertical_saccade(self):
        return lambda t: (0, (int(frequency * t * 2) % 2 == 0) * 1.25 - 0.75)

    def horizontal_saccade(self):
        return lambda t: ((int(frequency * t * 2) % 2 == 0) * 1.25 - 0.75, 0)

    def smooth_vertical(self):
        return lambda t: (0, 0.75 * cos(2 * pi * frequency * t))

    def smooth_horizontal(self):
        return lambda t: (0.75 * cos(2 * pi * frequency * t), 0)

    def smooth_circle(self):
        return lambda t: (0.75 * sin(2 * pi * frequency * t), 0.75 * cos(2 * pi * frequency * t))

    
