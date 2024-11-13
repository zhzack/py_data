import numpy as np

# 常量定义
c = 3e8  # 光速
f = 7.98e9  # 频率
lambda_ = c / f  # 波长

# 接收器的坐标
receivers = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]])  # A, B, C

# 接收器之间的相位差
phi_AB = 145  # 例子值，单位为弧度
phi_CA = -157  # 例子值，单位为弧度
phi_BC = 12  # 例子值，单位为弧度

# 计算距离差
d_AB = lambda_ * phi_AB / (2 * np.pi)
d_CA = lambda_ * phi_CA / (2 * np.pi)
d_BC = lambda_ * phi_BC / (2 * np.pi)

def calculate_aoa(receivers, d_AB, d_CA, d_BC):
    # 使用三角几何方法推导发射端的坐标
    
    # 三角形顶点坐标
    A = receivers[0]
    B = receivers[1]
    C = receivers[2]
    
    # 距离差到达时间差
    d = np.array([d_AB, d_CA, d_BC])
    
    # 根据几何关系推导公式
    # 这里假设接收器的坐标已知，通过几何推导发射端的坐标
    
    # 解方程组求解信号源的坐标（x, y）
    x = (d[0]**2 - d[1]**2 + B[0]**2 + B[1]**2 - C[0]**2 - C[1]**2) / (2 * (B[0] - C[0]))
    y = (d[1]**2 - d[2]**2 + C[0]**2 + C[1]**2) / (2 * (C[1] - B[1]))
    
    # 计算方位角
    angle = np.arctan2(y, x)
    
    return (x, y), angle

# 计算发射端的坐标和方位角
emitter_position, angle = calculate_aoa(receivers, d_AB, d_CA, d_BC)

print(f'发射端的坐标: {emitter_position}')
print(f'信号源的方位角: {np.degrees(angle)} 度')
