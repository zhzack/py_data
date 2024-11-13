import serial
from serial.tools import list_ports
import csv
import time
from collections import deque
import sys
import pandas as pd

import matplotlib.pyplot as plt

from custom3DPlot import Custom3DPlot
from displayValueApp import MainApp
import calculate

class MovingAverageFilter:
    def __init__(self, window_size):
        self.window_size = window_size
        self.windows = [deque(maxlen=window_size) for _ in range(3)]

    def add_data(self, data):
        for i in range(3):
            self.windows[i].append(data[i])

    def get_filtered_data(self):
        return tuple(
            sum(window) / len(window) if len(window) > 0 else 0.0
            for window in self.windows
        )

class SerialDataLogger:
    def __init__(self, target_description="USB to UART", baudrate=460800, csv_header=None, print_data=False, max_lines=0):
        self.target_description = target_description
        self.baudrate = baudrate
        self.csv_header = csv_header
        self.print_data = print_data
        self.max_lines = max_lines
        self.serial_port = None
        self.csv_writer = None
        self.data_list = deque(maxlen=max_lines if max_lines > 0 else None)
        self.filename=""
        self.start_time = 0
        self.end_time = 0
        self.filter = MovingAverageFilter(window_size=5)  # Initialize the filter with a window size of 5

    @staticmethod
    def find_serial_port(target_description="USB to UART"):
        ports = list_ports.comports()
        for port in ports:
            print("找到符合条件的串口：")
            print("串口名称:", port.device)
            print("串口描述:", port.description)
            print("串口硬件ID:", port.hwid)
            print("=======================================================")
            if target_description in port.description:
                return port.device
        return None
    
    @staticmethod
    def all_c(file_name):
        calculate.data_ca(file_name)
        
        # SerialDataLogger.ll_data(file_name)
    @staticmethod
    def process_values1(pdoa1, pdoa2, pdoa3):
        values = [pdoa1, pdoa2, pdoa3]
        sorted_values = sorted(values)
        pdoaX=156
        if sorted_values == [pdoa3, pdoa1, pdoa2]:
            return pdoa1,0
        elif sorted_values == [pdoa2, pdoa3, pdoa1]:
            return pdoa3,120
        elif sorted_values == [pdoa1, pdoa2, pdoa3]:
            return pdoa2,240
        
        elif sorted_values == [pdoa1, pdoa3, pdoa2] and pdoa1>=-pdoaX:
            return pdoa1,0
        
        elif sorted_values == [pdoa3, pdoa2, pdoa1] and pdoa1<=pdoaX:
            return pdoa1,0
        
        elif sorted_values == [pdoa3, pdoa2, pdoa1] and pdoa3>=-pdoaX:
            return pdoa3,120
        
        elif sorted_values == [pdoa2, pdoa1, pdoa3] and pdoa3<=pdoaX:
            return pdoa3,120
        
        elif sorted_values == [pdoa2, pdoa1, pdoa3] and pdoa2>=-pdoaX:
            return pdoa2,240
        
        elif sorted_values == [pdoa1, pdoa3, pdoa2] and pdoa2<=pdoaX:
            return pdoa2,240
        
        return pdoaX,(0)



    @staticmethod
    def process_values(pdoa1, pdoa2, pdoa3):
        values = [pdoa1, pdoa2, pdoa3]
        sorted_values = sorted(values)
        
        if sorted_values == [pdoa2, pdoa1, pdoa3]:
            offset = 0
        elif sorted_values == [pdoa2, pdoa3, pdoa1]:
            offset = 1
        elif sorted_values == [pdoa3, pdoa2, pdoa1]:
            offset = 2
        elif sorted_values == [pdoa3, pdoa1, pdoa2]:
            offset = 3
        elif sorted_values == [pdoa1, pdoa3, pdoa2]:
            offset = 4
        elif sorted_values == [pdoa1, pdoa2, pdoa3]:
            offset = 5
        
        second_value = float(sorted_values[1])
        second_value = (second_value if offset % 2 == 0 else -second_value) + offset * 180
        print(int(second_value/3),"------",offset * 180,offset,sorted_values)
        return second_value/3

    

    def open_serial_port(self):
        port_name = SerialDataLogger.find_serial_port(self.target_description)
        if port_name:
            self.serial_port = serial.Serial(port_name, self.baudrate)
            return True
        else:
            return False

    def create_csv_file(self, filename):
        self.csv_file = open(filename, 'w', newline='')
        if self.csv_header:
            self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=self.csv_header)
            self.csv_writer.writeheader()

    @staticmethod
    def data_ca(filename):
        df = pd.read_csv(filename)
        
        # 要统计的列名称
        columns_to_analyze = ['Distance', 'AoAAzimuth', 'AoAElevation', 'PdoaFirst', 'PdoaSecond', 'PdoaThird']

        # 创建一个空的字典，用于存储统计结果
        stats = {
            '列名': [],
            '均值': [],
            '中位数': [],
            '方差': [],
            '标准差': [],
            '最大值': [],
            '最小值': []
        }
        # 计算每列的统计信息
        for column in columns_to_analyze:
            stats['列名'].append(column)
            stats['均值'].append(df[column].mean())
            stats['中位数'].append(df[column].median())
            stats['方差'].append(df[column].var())
            stats['标准差'].append(df[column].std())
            stats['最大值'].append(df[column].max())
            stats['最小值'].append(df[column].min())
        # 获取特定列的名称
        column_name = 'sessionNumber'

        # 获取第一行的值
        first_row_value = df[column_name].iloc[0]

        # 获取最后一行的值
        last_row_value = df[column_name].iloc[-1]

        # 获取行数
        num_rows = df.shape[0]

        # 计算最后一行的值减去第一行的值与行数的比值（以百分比展示）
        percentage_change = (num_rows/(last_row_value - first_row_value) ) * 100
        

        # 将统计信息转换为 DataFrame
        stats_df = pd.DataFrame(stats)
        print(stats_df)
        print(f"last_row,{last_row_value},first_row,{first_row_value},num_rows,{num_rows},percentage,{percentage_change}")
    

    def update_data(self, data):
        if self.csv_writer:
            row = {}
            for i, key in enumerate(self.csv_header):
                # if key == 'PdoaFirst':
                #     pdoa1, pdoa2, pdoa3 = float(data[i]), float(data[i+1]), float(data[i+2])
                #     self.filter.add_data((pdoa1, pdoa2, pdoa3))
                #     filtered_pdoa1, filtered_pdoa2, filtered_pdoa3 = self.filter.get_filtered_data()
                #     row['PdoaFirst'] = filtered_pdoa1
                #     row['PdoaSecond'] = filtered_pdoa2
                #     row['PdoaThird'] = filtered_pdoa3
                #     # SerialDataLogger.process_values1(filtered_pdoa1,filtered_pdoa2,filtered_pdoa3)
                #     SerialDataLogger.process_values1(pdoa1, pdoa2, pdoa3)
                #     continue
                if i < len(data):
                    row[key] = data[i].strip()
                
                    
                    
                    
                else:
                    row[key] = '' 
                    
            # AoAAzimuth1=calculate.process_pdoaToAng(float(row['PdoaFirst']),float(row['PdoaSecond']),float(row['PdoaThird']))
            # app.controller.set_value(AoAAzimuth1)
            # x,y,z=Custom3DPlot.spherical_to_cartesian(AoAAzimuth1,float(row['Distance']),0)
            # row['x1']=x
            # row['y1']=y
            # row['z1']=z
            # row['AoAAzimuth1']=AoAAzimuth1
            # print(f"angle:{AoAAzimuth1}")
            row['timestamp'] =  int(round(time.time() * 1000))
            # row['Distance']
            # app.update_display_again(row['Distance'])
            
            self.csv_writer.writerow(row)
            self.csv_file.flush()
            
            
        self.data_list.append(row)
        
        if self.max_lines > 0 and len(self.data_list) >= self.max_lines:
            self.end_time = time.time()
            duration = self.end_time - self.start_time
            # SerialDataLogger.all_c(self.filename)
            print("程序运行时间：", duration, "秒")
            sys.exit()

    def plot_3d_coordinates(self):
        fig = plt.figure()
        ax2 = fig.add_subplot(projection='3d')

        xs = [float(row['x']) for row in self.data_list]
        ys = [float(row['y']) for row in self.data_list]
        zs = [float(row['z']) for row in self.data_list]
        ax2.scatter(xs, ys, zs, c='g', marker='o', label='Coordinates')
        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.set_zlabel('Z')
        ax2.set_title('XYZ Coordinates')

        plt.show()

    def read_serial_data(self):
        while True:
            line = self.serial_port.readline().decode().strip()
            data = line.split(',')
            for i in range(len(data)):
                if ':' in data[i]:
                    data[i] = data[i].strip()
                    _, data[i] = data[i].split(':', 1)
            if len(data) == len(self.csv_header)-1:
                self.update_data(data)       
                if self.print_data:
                    print(data)

    def close(self):
        if self.serial_port:
            self.serial_port.close()
        if self.csv_file:
            self.csv_file.close()

if __name__ == "__main__":
    # app = MainApp()
    # app.run()
    
    headers = [
        "sessionNumber",
        "sessionID",
        "MACAddress",
        "status",
        "Distance",
        "AoAAzimuth",
        "AoAAzimuthFOM",
        "AoAElevation",
        "AoAElevationFOM",
        "PdoaFirst",
        "PdoaSecond",
        "PdoaThird",
        "DstAoAAzimuth",
        "DstAoAAzimuthFOM",
        "DstAoAElevation",
        "DstAoAElevationFOM",
        "DstPdoaFirst",
        "DstPdoaSecond",
        "DstPdoaThird",
        "RSSI"
    ]
    
    headers = [
        "sessionNumber",
        "PdoaFirst",
        "PdoaSecond",
        "PdoaThird",
        "AoAElevation",
        "AoAAzimuth",
        "Distance",
        "x","y","z",
        "x1",
        "y1",
        "z1",
        "AoAAzimuth1"
    ]
    
    headers = [
        "sessionNumber",
        "PdoaFirst",
        "PdoaSecond",
        "PdoaThird",
        "AoAElevation",
        "AoAAzimuth",
        "Distance",
        "x","y","z",
        "DstPdoaFirst",
        "DstPdoaSecond",
        "DstPdoaThird",
        "RSSI",
        "timestamp"
    ]
    target_description = "USB to UART"
    target_description = "WCH USB-SERIAL Ch D"

    baudrate = 460800
    print_serial_data = 1
    max_lines = 400
    max_lines = 0

    logger = SerialDataLogger(target_description, baudrate, headers, print_serial_data, max_lines)
    if logger.open_serial_port():
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            logger.filename = f"data_{timestamp}.csv"
            logger.create_csv_file(logger.filename)
            logger.start_time = time.time() 
            logger.read_serial_data()
        except KeyboardInterrupt:
            print(logger.filename)
            # Custom3DPlot.plot_trajectory(logger.filename)
            # SerialDataLogger.all_c(logger.filename)
            
        finally:
            logger.close()
            print("Data logging stopped.")
