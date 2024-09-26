import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d
from collections import deque

class Trajectory:
    def __init__(self, color='blue', max_points=1000, smoothing=False, smoothing_sigma=2):
        self.color = color
        self.max_points = max_points
        self.smoothing = smoothing
        self.smoothing_sigma = smoothing_sigma
        self.data = deque(maxlen=max_points)
        self.plot = None  # Matplotlib Line2D object will be assigned later

    def add_point(self, x, y):
        self.data.append((x, y))
    
    def add_points(self, points):
        self.data.extend(points)

    def get_smoothed_data(self):
        if not self.data:
            return [], []
        
        x, y = zip(*self.data)
        
        if self.smoothing and len(x) > 1:
            x_smooth = gaussian_filter1d(x, sigma=self.smoothing_sigma)
            y_smooth = gaussian_filter1d(y, sigma=self.smoothing_sigma)
        else:
            x_smooth, y_smooth = x, y
            
        return x_smooth, y_smooth


class TrajectoryWindow:
    def __init__(self, root, max_points=1000, smoothing=False, smoothing_sigma=2):
        self.root = root
        self.root.title("Trajectory Display")
        
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.trajectories = []  # List to hold Trajectory objects

        # Fixed coordinate range
        self.ax.set_xlim(-200, 200)
        self.ax.set_ylim(-200, 200)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_title('Trajectory Display')
        
        self.ax.grid(True)
        self.canvas.draw()

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add_trajectory(self, trajectory):
        trajectory.plot, = self.ax.plot([], [], 'o-', color=trajectory.color)
        self.trajectories.append(trajectory)
        self.update_plot()

    def update_plot(self):
        for trajectory in self.trajectories:
            x_smooth, y_smooth = trajectory.get_smoothed_data()
            trajectory.plot.set_data(x_smooth, y_smooth)
        
        self.ax.relim()
        self.ax.autoscale_view()
        self.ax.set_xlim(-200, 200)
        self.ax.set_ylim(-200, 200)
        self.canvas.draw()

    def show_all(self):
        self.update_plot()

    def on_closing(self):
        self.root.after_cancel(self.after_id)
        self.root.destroy()

# 示例如何使用
if __name__ == "__main__":
    root = tk.Tk()
    traj_window = TrajectoryWindow(root, smoothing=True)  # 设置smoothing=True以启用平滑

    # 创建并添加两条轨迹
    traj1 = Trajectory(color='blue')
    traj2 = Trajectory(color='red')
    
    traj_window.add_trajectory(traj1)
    traj_window.add_trajectory(traj2)

    def add_random_points():
        # 生成随机点并添加到两条轨迹中
        traj1.add_points([(np.random.uniform(-200, 200), np.random.uniform(-200, 200))])
        traj2.add_points([(np.random.uniform(-200, 200), np.random.uniform(-200, 200))])
        
        traj_window.update_plot()
        traj_window.after_id = root.after(50, add_random_points)

    add_random_points()
    root.mainloop()
