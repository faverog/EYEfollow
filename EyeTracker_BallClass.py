'''
EYEfollow 1.0
Ball Class 
Gian Favero and Steven Caro
December 2021
'''

from math import pi, sin, cos
from time import sleep

class Ball:
    def __init__(self, master, canvas, size):
        self.master = master
        self.canvas = canvas
        self.size = size
        self.cycles = 0
        self.duration = 0
        self.testName = ""
        self.coords = [0,0]
        self.theta = 0
        self.radius = 0
        self.cycleTime = 0
        [self.xDelta, self.yDelta] = [0,0]
        [self.x1, self.x2] = [self.coords[0], self.coords[0]+self.size]
        [self.y1, self.y2] = [self.coords[1], self.coords[1]+self.size]
        self.ball = self.canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill="white")
        self.additionalBall = self.canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill="black")

    def move_ball(self):
        if self.master.answer == True:
            self.cycles = 0
            self.master.answer = False
            return

        # get current x&y of ball
        self.coords = self.canvas.coords(self.ball)[0], self.canvas.coords(self.ball)[1]
        self.canvas.update_idletasks()
        
        if self.testName == "Smooth_Horizontal" or self.testName == "Smooth_Vertical":
            if self.coords[0]+self.size >= self.canvas.winfo_width() or self.coords[0] <= 0:
                self.xDelta *= -1
                self.cycles += 1

            if self.coords[1]+self.size >= self.canvas.winfo_height() or self.coords[1] <= 0:
                self.yDelta *= -1
                self.cycles += 1
            
            # Move ball
            self.canvas.move(self.ball, self.xDelta, self.yDelta)
        
        elif self.testName == "Smooth_Circle":
            if self.theta + self.xDelta >= (self.cycles + 1)*2*pi:
                self.cycles += 1

            # Move ball
            self.theta += self.xDelta
            self.canvas.moveto(self.ball, self.master.width/2 + self.radius*cos(self.theta + self.xDelta), self.master.height/2 + self.radius*sin(self.theta + self.xDelta))

        elif self.testName == "Horizontal_Saccade":
            self.cycles += 1
            if self.cycles % 2 == 0:
                self.canvas.itemconfig(self.ball, fill="green")
                self.canvas.itemconfig(self.additionalBall, fill="white")
            else:
                self.canvas.itemconfig(self.ball, fill="white")
                self.canvas.itemconfig(self.additionalBall, fill="green")
            
        elif self.testName == "Vertical_Saccade":
            self.cycles += 1
            if self.cycles % 2 == 0:
                self.canvas.itemconfig(self.ball, fill="green")
                self.canvas.itemconfig(self.additionalBall, fill="white")
            else:
                self.canvas.itemconfig(self.ball, fill="white")
                self.canvas.itemconfig(self.additionalBall, fill="green")

        if self.cycles >= self.duration: # or (how to exit saccade tests)
            self.cycles = 0
            self.master.activeButtons[self.testName] = False
            self.master.test_routine()
            return

        self.canvas.after(self.cycleTime, self.move_ball)

    def set_test(self, testName):
        self.testName = testName
        self.canvas.itemconfig(self.additionalBall, fill="black")
        self.canvas.itemconfig(self.ball, fill="white")
        self.canvas.moveto(self.additionalBall, 0, 0)

        if testName == "Smooth_Horizontal":
            self.xDelta = 5
            self.yDelta = 0
            self.cycleTime = 5
            self.duration = 2
            self.canvas.moveto(self.ball, self.master.width/2, self.master.height/2)

        elif testName == "Smooth_Vertical":
            self.xDelta = 0
            self.yDelta = 5
            self.cycleTime = 5
            self.duration = 2
            self.canvas.moveto(self.ball, self.master.width/2, self.master.height/2)

        elif testName == "Smooth_Circle":
            self.xDelta = 0.01
            self.radius = self.master.height / 2.16
            self.theta = 0
            self.cycleTime = 5
            self.duration = 2
            self.canvas.moveto(self.ball, self.master.width/2, self.master.height/2)

        elif testName == "Horizontal_Saccade":
            self.cycleTime = 1500
            self.duration = 10
            self.canvas.moveto(self.ball, self.master.width/5, self.master.height/2)
            self.canvas.moveto(self.additionalBall, 4*self.master.width/5, self.master.height/2)
            self.canvas.itemconfig(self.additionalBall, fill="white")

        elif testName == "Vertical_Saccade":
            self.cycleTime = 1500
            self.duration = 10
            self.canvas.moveto(self.ball, self.master.width/2, self.master.height/8)
            self.canvas.moveto(self.additionalBall, self.master.width/2, 7*self.master.height/8)
            self.canvas.itemconfig(self.additionalBall, fill="white")