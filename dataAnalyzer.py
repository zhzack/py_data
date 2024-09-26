import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class DataAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.df = pd.read_csv(filename)
        self.distance_data = self.df['Distance']
        self.azimuth_data = self.df['AoAAzimuth']
        self.elevation_data = self.df['AoAElevation']
    
    def filter_data(self):
        nonzero_indices = np.nonzero(self.distance_data)[0]
        self.distance_data = self.distance_data.iloc[nonzero_indices]
        self.azimuth_data = self.azimuth_data.iloc[nonzero_indices]
        self.elevation_data = self.elevation_data.iloc[nonzero_indices]

    def calculate_coordinates(self):
        x = self.distance_data * np.sin(np.radians(self.elevation_data)) * np.sin(np.radians(self.azimuth_data))
        y = self.distance_data * np.sin(np.radians(self.elevation_data)) * np.cos(np.radians(self.azimuth_data))
        z = self.distance_data * np.cos(np.radians(self.elevation_data))
        return x, y, z

    def calculate_statistics(self):
        mean_distance = self.distance_data.mean()
        std_distance = self.distance_data.std()
        range_distance = self.distance_data.max() - self.distance_data.min()
        return mean_distance, std_distance, range_distance

    def plot_3d_coordinates(self):
        x, y, z = self.calculate_coordinates()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # ax.set_xlim(-50,50)
        # ax.set_ylim(-50,50)
        # ax.set_zlim(-50,50)
        ax.scatter(x, y, z)
        print(len(x))

        # 连接点
        # for i in range(len(x) - 1):
        #     ax.plot([x[i], x[i+1]], [y[i], y[i+1]], [z[i], z[i+1]], c='gray')

        mean_distance, std_distance, range_distance = self.calculate_statistics()
        ax.set_title(f"Distance avg: {mean_distance:.2f}, StandardDeviation: {std_distance:.2f}, Range: {range_distance:.2f}")
        plt.show()

if __name__ == "__main__":
    analyzer = DataAnalyzer("data_20240426_162322.csv")
    # analyzer.filter_data()
    analyzer.plot_3d_coordinates()
