import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class RealTimePlot:
    def __init__(self, canvas):
        self.canvas = canvas
        self.figure = self.canvas.figure
        self.ax = self.figure.add_subplot(111)
        self.line, = self.ax.plot([], [], 'r-')
        self.x_data = []
        self.y_data = []
        self.max_points = 100

        self.ax.set_xlabel("Local X")
        self.ax.set_ylabel("Local Y")
        self.ax.set_title("sdfsdf")

    def init_plot(self):
        self.line.set_data([], [])
        return self.line,

    def update_plot(self, x, y):
        self.x_data.append(x)
        self.y_data.append(y)

        if len(self.x_data) > self.max_points:
            self.x_data = self.x_data[-self.max_points:]
            self.y_data = self.y_data[-self.max_points:]

        self.line.set_data(self.x_data, self.y_data)
        self.ax.relim()
        self.ax.autoscale_view()

        self.canvas.draw()
        return self.line,

    def animate(self):
        self.anim = FuncAnimation(self.figure, self.update_plot, init_func=self.init_plot, blit=True)
        self.canvas.draw()
