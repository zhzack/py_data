import matplotlib.pyplot as plt
import numpy as np

def plot_concentric_circles(radius_list, center):
    fig, ax = plt.subplots()
    
    # 设置图形的比例为正方形
    ax.set_aspect('equal', adjustable='box')
    
    # 绘制每个圆
    for radius in radius_list:
        circle = plt.Circle(center, radius, fill=False, linestyle='dotted')
        ax.add_patch(circle)
    
    # 初始化轨迹
    trajectory_x = []
    trajectory_y = []
    colors = []
    
    # 设置初始点
    current_radius = radius_list[0]
    current_angle = 0  # 从 x 轴正半轴开始
    start_point = (0, 0)
    trajectory_x.append(start_point[0])
    trajectory_y.append(start_point[1])
    colors.append(current_angle)
    
    # 绘制从 (0, 0) 到第一个圆的轨迹
    angles = np.linspace(np.pi / 2, 3 * np.pi / 2, 500)
    for angle in angles:
        x = abs(center[1]) * np.cos(angle)
        y = abs(center[1]) * np.sin(angle) - abs(center[1])
        trajectory_x.append(x)
        trajectory_y.append(y)
        colors.append(angle)
    
    # 更新起始点为第一个圆的起点
    trajectory_x.append(center[0])
    trajectory_y.append(center[1] + current_radius)
    colors.append(np.pi / 2)

    for radius in radius_list:
        # 计算圆周上的点
        angles = np.linspace(np.pi / 2, np.pi / 2 + 2*np.pi, 1000)
        x_circle = center[0] + radius * np.cos(angles)
        y_circle = center[1] + radius * np.sin(angles)
        
        # 将圆周上的点添加到轨迹中
        trajectory_x.extend(x_circle)
        trajectory_y.extend(y_circle)
        colors.extend(angles)
        
        # 计算从当前圆到下一个圆的转弯轨迹
        if radius != radius_list[-1]:
            next_radius = radius_list[radius_list.index(radius) + 1]
            angle_step = np.pi / 100  # 调整转弯的角度步长，控制转弯的平滑度
            
            while current_radius > next_radius:
                current_angle += angle_step
                current_radius -= 0.01  # 调整半径步长，控制转弯的平滑度
                x = center[0] + current_radius * np.cos(current_angle)
                y = center[1] + current_radius * np.sin(current_angle)
                trajectory_x.append(x)
                trajectory_y.append(y)
                colors.append(current_angle)
    
    # 绘制轨迹
    scatter = ax.scatter(trajectory_x, trajectory_y, c=colors, cmap='hsv', s=1, label="Car Trajectory")
    fig.colorbar(scatter, ax=ax, label='Direction (radians)')
    
    # 设置轴的范围
    ax.set_xlim(-max(radius_list) - 12, max(radius_list) + 12)
    ax.set_ylim(-max(radius_list) - 12, max(radius_list) + 12)
    
    # 添加图例
    ax.legend()
    
    # 显示图形
    plt.grid(True)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Concentric Circles with Car Trajectory')
    plt.show()

# 定义半径列表
radius_list = [10,  2]
center = (0, -radius_list[0])  # 圆心

# 绘制同心圆和小车轨迹
plot_concentric_circles(radius_list, center)
