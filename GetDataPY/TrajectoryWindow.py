import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d
from collections import deque

class TrajectoryWindow:
    def __init__(self, root, max_points=1000, smoothing=False, smoothing_sigma=2):
        self.root = root
        self.root.title("Trajectory Display")
        
        # Matplotlib Figure and Axis
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.max_points = max_points
        self.smoothing = smoothing
        self.smoothing_sigma = smoothing_sigma
        self.data = deque(maxlen=max_points)
        self.plot, = self.ax.plot([], [], 'bo-')

        # Fixed coordinate range
        self.ax.set_xlim(-200, 200)
        self.ax.set_ylim(-200, 200)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_title('Trajectory Display')
        
        # Initial plot settings
        self.ax.grid(True)
        self.canvas.draw()

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add_point(self, x, y):
        self.data.append((x, y))
        self.update_plot()

    def update_plot(self):
        if not self.data:
            return
        
        x, y = zip(*self.data)
        
        # Apply smoothing if needed
        if self.smoothing and len(x) > 1:
            x_smooth = gaussian_filter1d(x, sigma=self.smoothing_sigma)
            y_smooth = gaussian_filter1d(y, sigma=self.smoothing_sigma)
        else:
            x_smooth, y_smooth = x, y
        
        self.plot.set_data(x_smooth, y_smooth)
        self.ax.relim()
        self.ax.autoscale_view()
        self.ax.set_xlim(-200, 200)
        self.ax.set_ylim(-200, 200)
        self.canvas.draw()

    def show_all(self):
        self.update_plot()

    def show_recent(self, num_points):
        if not self.data:
            return

        recent_data = list(self.data)[-num_points:]
        if recent_data:
            x, y = zip(*recent_data)
            
            # Apply smoothing if needed
            if self.smoothing and len(x) > 1:
                x_smooth = gaussian_filter1d(x, sigma=self.smoothing_sigma)
                y_smooth = gaussian_filter1d(y, sigma=self.smoothing_sigma)
            else:
                x_smooth, y_smooth = x, y
            
            self.plot.set_data(x_smooth, y_smooth)
            self.ax.relim()
            self.ax.autoscale_view()
            self.ax.set_xlim(-200, 200)
            self.ax.set_ylim(-200, 200)
            self.canvas.draw()

    def on_closing(self):
        # Cancel any pending after events here
        self.root.after_cancel(self.after_id)
        self.root.destroy()

# 示例如何使用
if __name__ == "__main__":
    root = tk.Tk()
    traj_window = TrajectoryWindow(root, smoothing=True)  # 设置smoothing=True以启用平滑

    def add_random_point():
        x = np.random.uniform(-200, 200)
        y = np.random.uniform(-200, 200)
        traj_window.add_point(x, y)
        traj_window.after_id = root.after(1000, add_random_point)

    add_random_point()

    root.mainloop()
