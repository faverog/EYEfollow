'''
EYEfollow 1.0
Main Canvas Class
Gian Favero and Steven Caro
December 2021
'''

import tkinter as tk

class Main_Canvas(tk.Canvas):
    def __init__(self, master, controller):
        tk.Canvas.__init__(self, master)
        self.controller = controller
        self.config(height=controller.height, width=controller.width, bg="black")