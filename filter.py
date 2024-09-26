import numpy as np
import matplotlib.pyplot as plt
from filterpy.kalman import KalmanFilter

# 模拟一行一行生成数据的生成器
def data_generator():
    np.random.seed(42)
    data_length = 100
    for value in np.sin(np.linspace(0, 10, data_length)) + np.random.normal(0, 0.5, data_length):
        yield value

# 增量式移动平均滤波
def incremental_moving_average(new_value, buffer, window_size):
    buffer.append(new_value)
    if len(buffer) > window_size:
        buffer.pop(0)
    return np.mean(buffer)

# 增量式加权移动平均滤波
def incremental_weighted_moving_average(new_value, buffer, weights):
    buffer.append(new_value)
    if len(buffer) > len(weights):
        buffer.pop(0)
    return np.dot(buffer, weights[-len(buffer):]) / np.sum(weights[-len(buffer):])

# 增量式指数加权移动平均滤波
def incremental_ewma(new_value, prev_ewma, alpha):
    return alpha * new_value + (1 - alpha) * prev_ewma

# 增量式卡尔曼滤波
def initialize_kalman_filter():
    kf = KalmanFilter(dim_x=1, dim_z=1)
    kf.x = np.array([[0.]])  # 初始状态
    kf.F = np.array([[1]])  # 状态转移矩阵
    kf.H = np.array([[1]])  # 观测矩阵
    kf.P = np.array([[1]])  # 状态协方差矩阵
    kf.R = np.array([[0.01]])  # 观测噪声协方差
    kf.Q = np.array([[0.01]])  # 过程噪声协方差
    return kf

def incremental_kalman_filter(kf, new_value):
    kf.predict()
    kf.update([new_value])
    return kf.x[0][0]

# # 参数设置
# window_size = 5
# weights = np.array([1, 2, 3, 2, 1])
# alpha = 0.3

# # 初始化滤波器
# moving_avg_buffer = []
# weighted_moving_avg_buffer = []
# prev_ewma = 0
# kf = initialize_kalman_filter()

# # 存储滤波结果
# data = []
# moving_avg_data = []
# weighted_moving_avg_data = []
# ewma_data = []
# kalman_data = []

# # 实时读取数据并更新滤波结果
# for new_value in data_generator():
#     data.append(new_value)
#     moving_avg_data.append(incremental_moving_average(new_value, moving_avg_buffer, window_size))
#     weighted_moving_avg_data.append(incremental_weighted_moving_average(new_value, weighted_moving_avg_buffer, weights))
#     prev_ewma = incremental_ewma(new_value, prev_ewma, alpha)
#     ewma_data.append(prev_ewma)
#     kalman_data.append(incremental_kalman_filter(kf, new_value))

# # 绘图比较滤波效果
# plt.figure(figsize=(14, 8))
# plt.plot(data, label='Original Data', color='gray', linestyle='dashed')
# plt.plot(moving_avg_data, label='Moving Average Filter')
# plt.plot(weighted_moving_avg_data, label='Weighted Moving Average Filter')
# plt.plot(ewma_data, label='Exponential Weighted Moving Average Filter')
# plt.plot(kalman_data, label='Kalman Filter')

# plt.legend()
# plt.title('Comparison of Different Filters')
# plt.show()
