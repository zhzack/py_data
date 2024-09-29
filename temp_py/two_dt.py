import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 定义参数
R = 100  # 点C的初始位置在(100, 0)
omega = 2 * np.pi  # 旋转角速度 (1周/秒)
num_revolutions = 10  # 旋转圈数

# 计算旋转所需的总帧数
frames_per_revolution = 100
total_frames = num_revolutions * frames_per_revolution

# 定义点A和点B的位置
A = np.array([-1, 0])
B = np.array([1, 0])
AB_distance = np.linalg.norm(B - A)  # 点A和点B之间的距离

# 计算距离函数
def distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2)**2))

# 设置动画
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 12))
ax1.set_xlim(-110, 110)
ax1.set_ylim(-110, 110)
ax1.set_aspect('equal')

# 设置曲线
C_marker, = ax1.plot([], [], 'ro')  # 点C
AB_line, = ax1.plot([-1, 1], [0, 0], 'bo')  # 点A和点B
C_trail, = ax1.plot([], [], 'r--')  # 点C的轨迹

distance_line_A, = ax2.plot([], [], label="Distance C-A")
distance_line_B, = ax2.plot([], [], label="Distance C-B")
distance_diff_line, = ax2.plot([], [], label="Distance (C-B) - (C-A)")
arcsin_line, = ax2.plot([], [], label="arcsin((C-B) - (C-A) / AB_distance)")

ax2.set_xlim(0, total_frames / 10.0)
ax2.set_ylim(-2, 2)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Distance / Arcsin Value')
ax2.legend()

# 初始化函数
def init():
    C_marker.set_data([], [])
    C_trail.set_data([], [])
    distance_line_A.set_data([], [])
    distance_line_B.set_data([], [])
    distance_diff_line.set_data([], [])
    arcsin_line.set_data([], [])
    return C_marker, C_trail, distance_line_A, distance_line_B, distance_diff_line, arcsin_line

# 更新函数
def update(frame):
    t = frame / 100.0
    theta = omega * t
    x = R * np.cos(theta)
    y = R * np.sin(theta)
    C = np.array([x, y])

    # 更新点C的位置
    C_marker.set_data(x, y)

    # 更新点C的轨迹
    if frame == 0:
        C_trail.set_data([x], [y])
    else:
        old_x, old_y = C_trail.get_data()
        C_trail.set_data(np.append(old_x, x), np.append(old_y, y))

    # 计算距离
    d_C_A = distance(C, A)
    d_C_B = distance(C, B)
    distance_diff = d_C_B - d_C_A
    arcsin_value = np.arcsin(distance_diff / AB_distance)

    # 保存距离
    distances_A[frame] = d_C_A - 100
    distances_B[frame] = d_C_B - 100
    distances_diff[frame] = distance_diff
    arcsin_values[frame] = arcsin_value

    # 更新距离曲线
    distance_line_A.set_data(np.arange(frame + 1) / 10.0, distances_A[:frame + 1])
    distance_line_B.set_data(np.arange(frame + 1) / 10.0, distances_B[:frame + 1])
    distance_diff_line.set_data(np.arange(frame + 1) / 10.0, distances_diff[:frame + 1])
    arcsin_line.set_data(np.arange(frame + 1) / 10.0, arcsin_values[:frame + 1])

    return C_marker, C_trail, distance_line_A, distance_line_B, distance_diff_line, arcsin_line

# 存储距离和arcsin值的数组
distances_A = np.zeros(total_frames)
distances_B = np.zeros(total_frames)
distances_diff = np.zeros(total_frames)
arcsin_values = np.zeros(total_frames)

# 创建动画
ani = FuncAnimation(fig, update, frames=range(total_frames), init_func=init, blit=False, interval=100)

plt.show()
