import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import argparse
import time

class RealTimePlot:
    def __init__(self, num_lines):
        self.figure, self.ax = plt.subplots()
        self.lines = [self.ax.plot([], [], label=f'Line {i+1}')[0] for i in range(num_lines)]
        self.x_data = [[] for _ in range(num_lines)]
        self.y_data = [[] for _ in range(num_lines)]
        self.max_points = 100

        self.ax.set_xlabel("Local X")
        self.ax.set_ylabel("Local Y")
        self.ax.set_title("Real-time Data Plot")
        self.ax.legend()

    def init_plot(self):
        for line in self.lines:
            line.set_data([], [])
        return self.lines

    def update_plot(self, frame):
        # Just a dummy method to allow FuncAnimation to work
        return self.lines

    def add_data(self, data):
        # Data should be a list of tuples (x, y) for each line
        for i, (x, y) in enumerate(data):
            self.x_data[i].append(x)
            self.y_data[i].append(y)

            if len(self.x_data[i]) > self.max_points:
                self.x_data[i] = self.x_data[i][-self.max_points:]
                self.y_data[i] = self.y_data[i][-self.max_points:]

            self.lines[i].set_data(self.x_data[i], self.y_data[i])

        self.ax.relim()
        self.ax.autoscale_view()
        self.figure.canvas.draw()

    def start_animation(self):
        self.anim = FuncAnimation(self.figure, self.update_plot, init_func=self.init_plot, frames=np.linspace(0, 10, 200), blit=True)
        plt.show()

def main():
    num_lines = 5
    plot = RealTimePlot(num_lines)

    def add_random_data():
        frame = add_random_data.frame
        data = [(frame, np.random.random()) for _ in range(num_lines)]
        plot.add_data(data)
        add_random_data.frame += 1
        if add_random_data.frame < 200:
            plot.figure.canvas.manager.window.after(100, add_random_data)

    add_random_data.frame = 0
    plot.start_animation()
    add_random_data()

if __name__ == '__main__':
    main()
