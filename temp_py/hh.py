import numpy as np
import matplotlib.pyplot as plt

# 设置参数
frequency = 7.98  # 信号频率，单位为GHz
speed_of_light = 3e8  # 光速，单位为m/s
wavelength = speed_of_light / (frequency * 1e9)  # 波长
side_length = wavelength / 2  # 正三角形的边长为半个波长

# 天线的位置（正三角形顶点）
antenna_positions = np.array([
    [0, 0],  # 天线1的位置
    [side_length, 0],  # 天线2的位置
    [side_length / 2, np.sqrt(3) / 2 * side_length]  # 天线3的位置
])

# 初始信号点的位置
signal_position = np.array([0.1, 1])

# 计算天线到信号点的距离
def calculate_distances(signal_position, antenna_positions):
    distances = np.linalg.norm(antenna_positions - signal_position, axis=1)
    return distances

# 计算相位差
def calculate_phase_differences(distances, wavelength):
    phase_differences = (distances / wavelength) * 2 * np.pi
    return phase_differences

# 设置绘图
fig, ax = plt.subplots()
ax.set_xlim(-0.5, 1)
ax.set_ylim(-0.5, 1.5)

# 绘制天线和信号点
antennas_plot, = ax.plot(antenna_positions[:, 0], antenna_positions[:, 1], 'bo', label='Antennas')
signal_plot, = ax.plot(signal_position[0], signal_position[1], 'ro', label='Signal Source')
lines = [ax.plot([], [], 'g-')[0] for _ in range(3)]

# 绘制相位差文本
phase_texts = [ax.text(-0.4, 1.4 - i * 0.1, '', fontsize=12) for i in range(3)]

# 更新函数
def update_plot(signal_position):
    distances = calculate_distances(signal_position, antenna_positions)
    phase_differences = calculate_phase_differences(distances, wavelength)

    # 更新信号点
    signal_plot.set_data(signal_position[0], signal_position[1])

    # 更新相位差文本
    for i, text in enumerate(phase_texts):
        text.set_text(f'Phase Diff {i+1}: {phase_differences[i]:.2f} rad')

    # 更新天线到信号点的线
    for i, line in enumerate(lines):
        line.set_data([antenna_positions[i, 0], signal_position[0]], [antenna_positions[i, 1], signal_position[1]])

    fig.canvas.draw_idle()

# 鼠标事件处理
class DraggablePoint:
    def __init__(self, point):
        self.point = point
        self.press = None
        self.background = None
        self.cidpress = point.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = point.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = point.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.point.axes: return
        contains, attrd = self.point.contains(event)
        if not contains: return
        x0, y0 = self.point.get_data()
        self.press = (x0[0], y0[0], event.xdata, event.ydata)

    def on_motion(self, event):
        if self.press is None: return
        if event.inaxes != self.point.axes: return
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        new_signal_position = np.array([x0 + dx, y0 + dy])
        self.point.set_data(new_signal_position[0], new_signal_position[1])
        update_plot(new_signal_position)

    def on_release(self, event):
        self.press = None
        self.point.figure.canvas.draw()

    def disconnect(self):
        self.point.figure.canvas.mpl_disconnect(self.cidpress)
        self.point.figure.canvas.mpl_disconnect(self.cidrelease)
        self.point.figure.canvas.mpl_disconnect(self.cidmotion)

# 使信号点可拖动
draggable_signal = DraggablePoint(signal_plot)

# 初始化绘图
update_plot(signal_position)

# 显示图形
plt.legend()
plt.show()
