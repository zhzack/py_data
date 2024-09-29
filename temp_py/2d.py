import math
import matplotlib.pyplot as plt
import numpy as np

def calculate_arc_length(radius, angle_degrees):
    # 将角度从度转换为弧度
    angle_radians = math.radians(angle_degrees)
    
    # 计算弧长
    arc_length = angle_radians * radius
    return arc_length

def generate_arc_lengths(angle_degrees, min_radius, max_radius, num_points):
    radii = np.linspace(min_radius, max_radius, num_points)
    arc_lengths = [calculate_arc_length(r, angle_degrees) for r in radii]
    return radii, arc_lengths

def plot_arc_lengths(angle_degrees, min_radius, max_radius, num_points):
    radii, arc_lengths = generate_arc_lengths(angle_degrees, min_radius, max_radius, num_points)
    
    plt.figure(figsize=(10, 6))
    plt.plot(radii, arc_lengths, marker='o')
    plt.xlabel('Radius')
    plt.ylabel('Arc Length')
    plt.title(f'Arc Length vs Radius for {angle_degrees} Degrees')
    plt.grid(True)
    plt.show()

# 示例使用
angle_degrees = 5  # 角度，以度为单位
min_radius = 0      # 最小半径
max_radius = 2000     # 最大半径
num_points = 2000    # 生成的点数

plot_arc_lengths(angle_degrees, min_radius, max_radius, num_points)
