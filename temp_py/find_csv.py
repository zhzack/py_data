import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import OptionMenu, StringVar

class FileSelector:
    def __init__(self, root):
        self.root = root
        self.csv_files = self.find_csv_files()
        self.current_index = 0
        self.selected_file = StringVar()
        self.selected_file.set(self.csv_files[0])

        menu = OptionMenu(root, self.selected_file, *self.csv_files, command=self.plot_file)
        menu.pack()

        prev_button = tk.Button(root, text='上一个', command=self.prev_file)
        prev_button.pack(side='left')

        next_button = tk.Button(root, text='下一个', command=self.next_file)
        next_button.pack(side='right')

        self.fig = None
        self.ax = None

    def find_csv_files(self):
        csv_files = []
        for file in os.listdir('.'):
            if file.startswith("data_") and file.endswith(".csv") and len(file) == 24:
                csv_files.append(file)
        return csv_files

    def plot_file(self, *args):
        selected_filename = self.selected_file.get()
        index = self.csv_files.index(selected_filename)
        self.current_index = index
        self.plot_current_file()

    def plot_current_file(self):
        if self.fig is None:
            self.create_figure()
        else:
            self.update_figure()
            
    
        

    def create_figure(self):
        filename = self.csv_files[self.current_index]
        df = pd.read_csv(filename)

        distance_data = df['Distance']
        azimuth_data = df['AoAAzimuth']
        elevation_data = df['AoAElevation']

        nonzero_indices = np.nonzero(distance_data)[0]
        distance_data = distance_data.iloc[nonzero_indices]
        azimuth_data = azimuth_data.iloc[nonzero_indices]
        elevation_data = elevation_data.iloc[nonzero_indices]

        x = distance_data * np.sin(np.radians(elevation_data)) * np.sin(np.radians(azimuth_data))
        y = distance_data * np.sin(np.radians(elevation_data)) * np.cos(np.radians(azimuth_data))
        z = distance_data * np.cos(np.radians(elevation_data))

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.scatter(x, y, z)
        self.ax.set_title(f"当前文件: {filename}", fontproperties="SimHei")

        mean_distance = distance_data.mean()
        std_distance = distance_data.std()
        range_distance = distance_data.max() - distance_data.min()
        print( mean_distance, std_distance, range_distance)

        plt.show()

    def update_figure(self):
        filename = self.csv_files[self.current_index]
        df = pd.read_csv(filename)

        distance_data = df['Distance']
        azimuth_data = df['AoAAzimuth']
        elevation_data = df['AoAElevation']

        nonzero_indices = np.nonzero(distance_data)[0]
        distance_data = distance_data.iloc[nonzero_indices]
        azimuth_data = azimuth_data.iloc[nonzero_indices]
        elevation_data = elevation_data.iloc[nonzero_indices]

        x = distance_data * np.sin(np.radians(elevation_data)) * np.sin(np.radians(azimuth_data))
        y = distance_data * np.sin(np.radians(elevation_data)) * np.cos(np.radians(azimuth_data))
        z = distance_data * np.cos(np.radians(elevation_data))

        self.ax.clear()
        self.ax.scatter(x, y, z)
        self.ax.set_title(f"当前文件: {filename}", fontproperties="SimHei")

        mean_distance = distance_data.mean()
        std_distance = distance_data.std()
        range_distance = distance_data.max() - distance_data.min()

        mean_azimuth = azimuth_data.mean()
        std_azimuth = azimuth_data.std()
        range_azimuth = azimuth_data.max() - azimuth_data.min()

        mean_elevation = elevation_data.mean()
        std_elevation = elevation_data.std()
        range_elevation = elevation_data.max() - elevation_data.min()

        print(filename)
        print(f"Distance avg: {mean_distance:.2f}, StandardDeviation: {std_distance:.2f}, Range: {range_distance:.2f}")
        print(f"azimuth: {mean_azimuth:.2f}, StandardDeviation: {std_azimuth:.2f}, Range: {range_azimuth:.2f}")
        print(f"elevation: {mean_elevation:.2f}, StandardDeviation: {std_elevation:.2f}, Range: {range_elevation:.2f}")

        self.fig.canvas.draw()  # 更新坐标系

    def prev_file(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.plot_current_file()

    def next_file(self):
        if self.current_index < len(self.csv_files) - 1:
            self.current_index += 1
            self.plot_current_file()

if __name__ == "__main__":
    root = tk.Tk()
    file_selector = FileSelector(root)
    root.mainloop()
