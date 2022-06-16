'''
EYEfollow 1.0
Ball Class 
Gian Favero and Steven Caro
December 2021
'''

from math import pi, sin, cos
from time import time

routine_duration = 15   # s
refresh_rate     = 1    # ms
frequency        = 0.2  # Hz

class Ball_Object: 
    def __init__(self, master, canvas, size):
        self.master = master
        self.canvas = canvas
        self.size = size
        self.ball = self.canvas.create_oval(0, 0, self.size, self.size, fill="white")

    def set_tests(self, tests):
        self.test_names = iter(tests)
    
    def move_ball(self):
        try:
            self.current_test = next(self.test_names)
            self.time_ref = time()
            self.draw()
        except StopIteration:
            self.test_names = []
            self.master.routine_finished()
        
        self.canvas.after(routine_duration * 1000, self.move_ball)

    def draw(self):
        x, y = self.get_coords(self.current_test, time())
        self.canvas.moveto(self.ball, x, y)

        if time() - self.time_ref < routine_duration:
            self.canvas.after(refresh_rate, self.draw)
        else:
            self.canvas.moveto(self.ball, self.master.width / 2, self.master.height / 2)
        
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

    
