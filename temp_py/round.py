import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 定义参数
c = 3e8  # 光速
f = 7.98e9  # 频率
lambda_ = c / f  # 波长
a = lambda_ / 2  # 正三角形边长
r = a / np.sqrt(3)  # 正三角形顶点到中心的距离
R = 5  # 发射端旋转的半径
omega = 2 * np.pi * 0.1  # 旋转角速度
num_revolutions = 1  # 旋转圈数

# 计算旋转所需的总帧数
frames_per_revolution = 100
total_frames = num_revolutions * frames_per_revolution

# 定义正三角形的顶点坐标
A = np.array([0, 2 * r / np.sqrt(3)])
B = np.array([-r, -r / np.sqrt(3)])
C = np.array([r, -r / np.sqrt(3)])

# 计算距离函数
def distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2)**2))

# 计算相位函数
def phase(d):
    return (2 * np.pi * d) / lambda_

# 旋转并缩放三角形
def rotate_scale_triangle(A, B, C, angle_deg, scale_factor):
    angle_rad = np.deg2rad(angle_deg)
    rotation_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad)],
                                [np.sin(angle_rad), np.cos(angle_rad)]])
    points = np.array([A, B, C]).T * scale_factor
    rotated_points = np.dot(rotation_matrix, points)
    return rotated_points.T

# 设置动画
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 18))
ax1.set_xlim(-1.5*R, 1.5*R)
ax1.set_ylim(-1.5*R, 1.5*R)
ax1.set_aspect('equal')

ax2.set_xlim(0, total_frames / 10.0)
ax2.set_ylim(-280, 280)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Phase Difference (degrees)')

ax3.set_xlim(0, total_frames / 10.0)
ax3.set_ylim(0, 2*R)
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Distance (m)')

# 新的正三角形的顶点坐标
angle_deg = 60
A_new, B_new, C_new = rotate_scale_triangle(A, B, C, angle_deg, 10)

triangle, = ax1.plot([], [], 'b')
triangle1, = ax1.plot([], [], 'b')
transmitter, = ax1.plot([], [], 'ro')

time_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes)

# 创建相位差文本
phase_text_A_B = ax1.text(1.05, 0.6, '', transform=ax1.transAxes, fontsize=12)
phase_text_C_A = ax1.text(1.05, 0.5, '', transform=ax1.transAxes, fontsize=12)
phase_text_B_C = ax1.text(1.05, 0.4, '', transform=ax1.transAxes, fontsize=12)

phases = [[], [], [], [], []]  # 新增两个列表用于存储最小和最大相位差取反后的值
distances = [[], [], []]
lines_phases = [ax2.plot([], [], label=f"pd {pair}")[0] for pair in ['A-B', 'C-A', 'B-C']]
line_min_phase = ax2.plot([], [], label="Min pd", color='black', linestyle='--')[0]  # 新增曲线
line_max_phase = ax2.plot([], [], label="Max pd", color='red', linestyle='--')[0]  # 新增曲线
lines_phases.append(line_min_phase)
lines_phases.append(line_max_phase)
lines_distances = [ax3.plot([], [], label=f"Distance to {point}")[0] for point in ['A', 'B', 'C']]

ax2.legend()
ax3.legend()

# 定义相位偏移量（以角度为单位）
theta_offset = np.deg2rad(90)

def calculate_phase_difference(P, A, B, C):
    d_A = distance(P, A)
    d_B = distance(P, B)
    d_C = distance(P, C)

    phi_A = phase(d_A)
    phi_B = phase(d_B)
    phi_C = phase(d_C)

    # 计算相位差并转换为度
    phase_diff_A_B = np.degrees(phi_A - phi_B)
    phase_diff_C_A = np.degrees(phi_C - phi_A)
    phase_diff_B_C = np.degrees(phi_B - phi_C)

    return phase_diff_A_B, phase_diff_C_A, phase_diff_B_C, d_A, d_B, d_C

def init():
    triangle.set_data([A_new[0], B_new[0], C_new[0], A_new[0]], [A_new[1], B_new[1], C_new[1], A_new[1]])
    triangle1.set_data([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]])
    transmitter.set_data([], [])
    time_text.set_text('')
    phase_text_A_B.set_text('')
    phase_text_C_A.set_text('')
    phase_text_B_C.set_text('')
    for line in lines_phases + lines_distances:
        line.set_data([], [])
        
    return [triangle, transmitter, time_text, phase_text_A_B, phase_text_C_A, phase_text_B_C] + lines_phases + lines_distances

def update(frame):
    t = frame / 10.0
    x = R * np.cos(omega * t + theta_offset)
    y = R * np.sin(omega * t + theta_offset)
    P = np.array([x, y])

    phase_diff_A_B, phase_diff_C_A, phase_diff_B_C, d_A, d_B, d_C = calculate_phase_difference(P, A, B, C)

    transmitter.set_data(np.array([x]), np.array([y]))

    time_text.set_text(f'Time = {t:.1f}s')

    phases[0].append(phase_diff_A_B)
    phases[1].append(phase_diff_C_A)
    phases[2].append(phase_diff_B_C)
    min_phase_diff = -(min(phase_diff_A_B, phase_diff_C_A, phase_diff_B_C))  # 计算最小相位差并取反
    max_phase_diff = -(max(phase_diff_A_B, phase_diff_C_A, phase_diff_B_C))  # 计算最大相位差并取反
    phases[3].append(min_phase_diff)
    phases[4].append(max_phase_diff)

    distances[0].append(d_A)
    distances[1].append(d_B)
    distances[2].append(d_C)

    phase_text_A_B.set_text(f'pd A-B: {phase_diff_A_B:.2f}°')
    phase_text_C_A.set_text(f'pd C-A: {phase_diff_C_A:.2f}°')
    phase_text_B_C.set_text(f'pd B-C: {phase_diff_B_C:.2f}°')

    for i, line in enumerate(lines_phases):
        line.set_data(np.arange(len(phases[i])) / 10.0, phases[i])

    for i, line in enumerate(lines_distances):
        line.set_data(np.arange(len(distances[i])) / 10.0, distances[i])

    return [triangle, transmitter, time_text, phase_text_A_B, phase_text_C_A, phase_text_B_C] + lines_phases + lines_distances

ani = FuncAnimation(fig, update, frames=range(total_frames), init_func=init, interval=100, blit=False)

plt.show()
