import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import numpy as np

class RealTimePlot:
    def __init__(self, y_data):
        self.y_data_series = y_data
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], label='Data')
        self.ax.legend()

        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(min(y_data) - 10, max(y_data) + 10)

        self.x_data = list(range(len(y_data)))
        self.y_data = list(y_data)

        self.ani = animation.FuncAnimation(self.fig, self.update, interval=1000, blit=True)

    def update(self, frame):
        self.line.set_data(self.x_data, self.y_data)
        self.ax.set_xlim(0, len(self.x_data))
        self.ax.set_ylim(min(self.y_data) - 10, max(self.y_data) + 10)
        return self.line,

    def add_data_point(self, new_data):
        self.x_data.append(len(self.x_data))
        self.y_data.append(new_data)
        self.y_data_series = self.y_data_series.append(pd.Series([new_data]), ignore_index=True)

    def show(self):
        plt.show()

# 示例调用
data = {'Data': [10, -20, 30, 5, 25]}
df = pd.DataFrame(data)

# 创建一个 RealTimePlot 实例
plot = RealTimePlot(df['Data'])

# 添加新的数据点
plot.add_data_point(15)
plot.add_data_point(20)

# 显示图形
plot.show()
