import numpy as np
import matplotlib.pyplot as plt

# 定义等边三角形的三个顶点
triangle_points = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]])

# 绘制等边三角形
plt.figure(figsize=(8, 6))
plt.plot([triangle_points[0, 0], triangle_points[1, 0], triangle_points[2, 0], triangle_points[0, 0]],
         [triangle_points[0, 1], triangle_points[1, 1], triangle_points[2, 1], triangle_points[0, 1]], 'r-')

# 定义三角形外的一个点
external_point = np.array([0, 10.5])

# 绘制三角形外的点
plt.plot(external_point[0], external_point[1], 'bo')

# 计算三角形顶点到外点的方位角
angles = []
for point in triangle_points:
    vector = external_point - point
    angle = np.arctan2(vector[1], vector[0])  # 计算方位角
    angles.append(angle)

# 输出方位角
for i, angle in enumerate(angles):
    print(f"Point {i+1} to external point angle: {np.degrees(angle)} degrees")

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Equilateral Triangle with External Point')
plt.axis('equal')
plt.grid(True)
plt.show()
