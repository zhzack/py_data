import pandas as pd
import numpy as np
from scipy.ndimage import gaussian_filter1d
from scipy.signal import butter, filtfilt
from sklearn.linear_model import LinearRegression

class DataProcessor:
    @staticmethod
    def correct_sign(data1, data2, data3, threshold):
        corrected_data1 = data1.copy()
        corrected_data2 = data2.copy()
        corrected_data3 = data3.copy()
        
        # 计算前20个数据的平均值，确定初始符号
        initial_avg1 = np.mean(data1[:20])
        initial_avg2 = np.mean(data2[:20])
        initial_avg3 = np.mean(data3[:20])
        
        init_sign1 = np.sign(initial_avg1)
        init_sign2 = np.sign(initial_avg2)
        init_sign3 = np.sign(initial_avg3)
        
        # 初始化上一个值
        prev_value1 = init_sign1 * abs(corrected_data1[0])
        prev_value2 = init_sign2 * abs(corrected_data2[0])
        prev_value3 = init_sign3 * abs(corrected_data3[0])
        
        for i in range(1, len(corrected_data1)):
            
            
            # 保留原有符号检查逻辑
            if corrected_data1[i] * prev_value1 < 0 and abs(corrected_data1[i] - prev_value1) >= threshold:
                corrected_data1[i] = -corrected_data1[i]
            if corrected_data2[i] * prev_value2 < 0 and abs(corrected_data2[i] - prev_value2) >= threshold:
                corrected_data2[i] = -corrected_data2[i]
            if corrected_data3[i] * prev_value3 < 0 and abs(corrected_data3[i] - prev_value3) >= threshold:
                corrected_data3[i] = -corrected_data3[i]
        
            sum_vals = corrected_data1[i] + corrected_data2[i] + corrected_data3[i]
            
            # 符号纠正逻辑
            if sum_vals > 10:
                if abs(corrected_data1[i] - prev_value1) >= threshold:
                    corrected_data1[i] = -corrected_data1[i]
                if abs(corrected_data2[i] - prev_value2) >= threshold:
                    corrected_data2[i] = -corrected_data2[i]
                if abs(corrected_data3[i] - prev_value3) >= threshold:
                    corrected_data3[i] = -corrected_data3[i]
            
            # 更新上一个值
            prev_value1 = corrected_data1[i]
            prev_value2 = corrected_data2[i]
            prev_value3 = corrected_data3[i]
        
        return corrected_data1, corrected_data2, corrected_data3

    @staticmethod
    def moving_average(data, window_size):
        return np.convolve(data, np.ones(window_size) / window_size, mode='valid')
    
    @staticmethod
    def smooth_data_gaussian(data, sigma):
        return gaussian_filter1d(data, sigma=sigma)
    
    @staticmethod
    def butter_lowpass_filter(data, cutoff, fs, order=5):
        nyquist = 0.5 * fs
        normal_cutoff = cutoff / nyquist
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        y = filtfilt(b, a, data)
        return y
    
    @staticmethod
    def process_data(df, columns, threshold, smooth_method='gaussian', **kwargs):
        data1 = df[columns[0]].values
        data2 = df[columns[1]].values
        data3 = df[columns[2]].values
        
        corrected_data1, corrected_data2, corrected_data3 = DataProcessor.correct_sign(data1, data2, data3, threshold)
        
        if smooth_method == 'moving_average':
            window_size = kwargs.get('window_size', 5)
            smoothed_data1 = DataProcessor.moving_average(corrected_data1, window_size)
            smoothed_data2 = DataProcessor.moving_average(corrected_data2, window_size)
            smoothed_data3 = DataProcessor.moving_average(corrected_data3, window_size)
        elif smooth_method == 'gaussian':
            sigma = kwargs.get('sigma', 2)
            smoothed_data1 = DataProcessor.smooth_data_gaussian(corrected_data1, sigma)
            smoothed_data2 = DataProcessor.smooth_data_gaussian(corrected_data2, sigma)
            smoothed_data3 = DataProcessor.smooth_data_gaussian(corrected_data3, sigma)
        elif smooth_method == 'lowpass':
            cutoff = kwargs.get('cutoff', 0.1)
            fs = kwargs.get('fs', 1.0)
            order = kwargs.get('order', 5)
            smoothed_data1 = DataProcessor.butter_lowpass_filter(corrected_data1, cutoff, fs, order)
            smoothed_data2 = DataProcessor.butter_lowpass_filter(corrected_data2, cutoff, fs, order)
            smoothed_data3 = DataProcessor.butter_lowpass_filter(corrected_data3, cutoff, fs, order)
        elif smooth_method == 'linear_regression':
            x = np.arange(len(corrected_data1)).reshape(-1, 1)
            model1 = LinearRegression().fit(x, corrected_data1)
            model2 = LinearRegression().fit(x, corrected_data2)
            model3 = LinearRegression().fit(x, corrected_data3)
            smoothed_data1 = model1.predict(x)
            smoothed_data2 = model2.predict(x)
            smoothed_data3 = model3.predict(x)
        else:
            raise ValueError("Unknown smooth method: choose from 'moving_average', 'gaussian', 'lowpass', or 'linear_regression'")
        
        return smoothed_data1, smoothed_data2, smoothed_data3

# # 示例数据
# df = pd.DataFrame({
#     'data1': [1, -2, 3, 10, 5, -6, 7, -20, 9, 10, -11, 12, 13, 14, 15],
#     'data2': [2, -3, 4, 11, 6, -7, 8, -21, 10, 11, -12, 13, 14, 15, 16],
#     'data3': [3, -4, 5, 12, 7, -8, 9, -22, 11, 12, -13, 14, 15, 16, 17]
# })

# threshold = 20

# # 平滑方法: 'moving_average', 'gaussian', 'lowpass', or 'linear_regression'
# smoothed_data1, smoothed_data2, smoothed_data3 = DataProcessor.process_data(df, ['data1', 'data2', 'data3'], threshold, smooth_method='linear_regression')

# print(smoothed_data1)
# print(smoothed_data2)
# print(smoothed_data3)
