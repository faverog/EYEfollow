class Ball:
    def __init__(self, master, canvas, size):
        self.master = master
        self.canvas = canvas
        self.size = size
        self.cycles = 0
        self.testName = ""
        self.coords = [0,0]
        [self.xDelta, self.yDelta] = [0,0]
        [self.x1, self.x2] = [self.coords[0], self.coords[0]+self.size]
        [self.y1, self.y2] = [self.coords[1], self.coords[1]+self.size]
        self.ball = self.canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill="white")

    def move_ball(self):
        if self.master.answer == True:
            self.master.answer = False
            return

        # get current x&y of ball
        self.coords = self.canvas.coords(self.ball)[0], self.canvas.coords(self.ball)[1]
        self.canvas.update_idletasks()

        if self.coords[0]+self.size >= self.canvas.winfo_width() or self.coords[0] <= 0:
            self.xDelta *= -1
            self.cycles += 1

        if self.coords[1]+self.size >= self.canvas.winfo_height() or self.coords[1] <= 0:
            self.yDelta *= -1
            self.cycles += 1

        if self.cycles >= 2:
            self.cycles = 0
            self.master.activeButtons[self.testName] = False
            self.master.test_routine()
            return

        self.canvas.move(self.ball, self.xDelta, self.yDelta)
        self.canvas.after(5, self.move_ball)

    def set_test(self, testName):
        self.testName = testName
        if testName == "Smooth_Horizontal":
            self.xDelta = 5
            self.yDelta = 0
            self.canvas.moveto(self.ball, self.master.width/2, self.master.height/2)
        elif testName == "Smooth_Vertical":
            self.xDelta = 0
            self.yDelta = 5
            self.canvas.moveto(self.ball, self.master.width/2, self.master.height/2)
        elif testName == "Smooth_Circle":
            # self.xDelta, self.yDelta = circleCalc()
            pass