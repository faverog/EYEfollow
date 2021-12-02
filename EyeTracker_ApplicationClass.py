import tkinter as tk
import ctypes
from tkinter.constants import CENTER

# Set resolution for screen
ctypes.windll.shcore.SetProcessDpiAwareness(1)

class Ball:
    def __init__(self, canvas, size, coords, testName):
        self.x1 = coords[0]
        self.y1 = coords[1]
        self.x2 = coords[0] + size
        self.y2 = coords[1] + size
        if testName == "Smooth_Horizontal":
            self.xDelta = 5
            self.yDelta = 0
        elif testName == "Smooth_Vertical":
            self.xDelta = 0
            self.yDelta = 5
        elif testName == "Smooth_Circle":
            # self.xDelta, self.yDelta = circleCalc()
            pass
        self.canvas = canvas
        self.coords = coords
        self.size = size
        self.ball = self.canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill="white")

    def move_ball(self):
        # get current x&y of ball
        self.coords = self.canvas.coords(self.ball)[0], self.canvas.coords(self.ball)[1]
        self.canvas.update_idletasks()
        if self.coords[0]+self.size >= self.canvas.winfo_width() or self.coords[0] <= 0:
            self.xDelta *= -1
        if self.coords[1]+self.size >= self.canvas.winfo_height() or self.coords[1] <= 0:
            self.yDelta *= -1
        self.canvas.move(self.ball, self.xDelta, self.yDelta)
        self.canvas.after(10, self.move_ball)

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("EyeFollow, FC 2021")
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
        
        frame = Home_Screen(master=container, controller=self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

        self.main_canvas = Main_Canvas(master=container, controller=self)

        self.activeButtons = []
        
    def toggle_fullscreen(self, event=None):
            self.attributes("-fullscreen", True)
            self.update_idletasks()
            self.width = self.winfo_width()
            self.height = self.winfo_height()

    def end_fullscreen(self, event=None):
        self.attributes("-fullscreen", False)
        self.state("zoomed")
        self.update_idletasks()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
    
    def show_canvas(self):
        '''Show the main canvas'''
        self.main_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        tk.Misc.lift(self.main_canvas)
        self.test_routine("Smooth_Vertical")
        
    def activate_button(self, page_name):
        self.activeButtons.append((str(page_name)))

    def test_routine(self, tests):
        ball1= Ball(self.main_canvas, 15, [self.width/2, self.height/2], self.activeButtons[0])
        ball1.move_ball()

class Home_Screen(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.configure(bg="white")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(7, weight=1)

        self.VS_b = tk.Button(self, text = 'Vertical Saccade', bg = "white",
                              command=lambda: [controller.activate_button("Vertical_Saccade"), self.onOff(0)])
        self.HS_b = tk.Button(self, text = 'Horizontal Saccade', bg = "white",
                              command=lambda: [controller.activate_button("Horizontal_Saccade"), self.onOff(1)])
        self.SC_b = tk.Button(self, text = 'Smooth Circle', bg = "white", 
                              command=lambda: [controller.activate_button("Smooth_Circle"), self.onOff(2)])
        self.SV_b = tk.Button(self, text = 'Smooth Vertical', bg="white",
                              command=lambda: [controller.activate_button("Smooth_Vertical"), self.onOff(3)])
        self.SH_b = tk.Button(self, text = 'Smooth Horizontal', bg="white",
                              command=lambda: [controller.activate_button("Smooth_Horizontal"), self.onOff(4)])
        self.start_b = tk.Button(self, text = 'START', bg = "#eee", state="disabled", height=5, width=20, command=lambda:controller.show_canvas())

        self.VS_b.grid(row=1, column=2, padx=10)
        self.HS_b.grid(row=1, column=3, padx=10)
        self.SC_b.grid(row=1, column=4, padx=10)
        self.SV_b.grid(row=1, column=5, padx=10)
        self.SH_b.grid(row=1, column=6, padx=10)
        self.start_b.grid(row=2, column=0, columnspan = 8, pady=75)

        self.buttonStatus = [False, False, False, False, False]
        
    def onOff(self, b_id):
        self.buttonStatus[b_id] = not self.buttonStatus[b_id]
        
        if self.buttonStatus[b_id] is True:
            match b_id:
                case 0:
                    self.VS_b.configure(bg="#adffab")
                case 1:
                    self.HS_b.configure(bg="#adffab")
                case 2:
                    self.SC_b.configure(bg="#adffab")
                case 3:
                    self.SV_b.configure(bg="#adffab")
                case 4:
                    self.SH_b.configure(bg="#adffab")
        else:
            match b_id:
                case 0:
                    self.VS_b.configure(bg="white")
                case 1:
                    self.HS_b.configure(bg="white")
                case 2:
                    self.SC_b.configure(bg="white")
                case 3:
                    self.SV_b.configure(bg="white")
                case 4:
                    self.SH_b.configure(bg="white")

        self.start_b.configure(state="disabled", bg="#eee")

        for items in self.buttonStatus:
            if items is True:
                self.start_b.configure(state="normal", bg="#adffab")
                break

class Main_Canvas(tk.Canvas):
    def __init__(self, master, controller):
        tk.Canvas.__init__(self, master)
        self.controller = controller
        self.config(height=controller.height, width=controller.width, bg="black")

if __name__ == '__main__':
    app = Application()
    app.mainloop()