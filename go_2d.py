import matplotlib.pyplot as plt

class RealTimePlot:
    def __init__(self, max_points=None):
        self.fig, self.ax = plt.subplots()  # 创建图形和子图
        self.x_data = []
        self.y_data = []
        self.max_points = max_points

    def add_point(self, x, y, connect=True):
        """实时添加单个数据点，并选择是否将所有数据点连接起来"""
        self.x_data.append(x)
        self.y_data.append(y)

        # 检查是否超过最大点数量
        if self.max_points is not None and len(self.x_data) > self.max_points:
            self.x_data.pop(0)  # 移除最旧的数据点
            self.y_data.pop(0)

        # 绘制曲线
        self.ax.clear()  # 清空子图
        if connect:
            self.ax.plot(self.x_data, self.y_data, 'bo-')  # 绘制蓝色圆点和连线
        else:
            self.ax.plot(self.x_data, self.y_data, 'bo')  # 只绘制蓝色圆点
        self.ax.set_xlabel('X')  # 设置X轴标签
        self.ax.set_ylabel('Y')  # 设置Y轴标签
        # plt.draw()  # 更新图形

# 示例用法
if __name__ == "__main__":
    plotter = RealTimePlot(max_points=100)  # 最大点数量为10
    for i in range(100):
        plotter.add_point(i, i**2, connect=True)  # 实时添加单个数据点并连接起来
        plt.pause(0.5)  # 暂停0.5秒以观察效果
    plt.show()  # 显示图形
