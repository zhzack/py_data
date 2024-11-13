import serial.tools.list_ports
import csv
import time
import matplotlib.pyplot as plt
from collections import deque
import numpy as np

# 定义目标串口描述字符串
target_description = "USB to UART"

# 获取所有可用串口
ports = serial.tools.list_ports.comports()

# 遍历所有串口并找到符合条件的串口
target_port = None
for port in ports:
    if target_description in port.description:
        target_port = port
        break

# 如果未找到符合条件的串口
if target_port is None:
    print("未找到符合条件的串口。")
else:
    print("找到符合条件的串口：")
    print("串口名称:", target_port.device)
    print("串口描述:", target_port.description)
    print("串口硬件ID:", target_port.hwid)
    print("=======================================================")

    # 打开符合条件的串口
    ser = serial.Serial(target_port.device, 460800)  # 这里的波特率需要根据实际情况修改

    # 创建CSV文件并写入表头
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"data_{timestamp}.csv"
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['###', 'ranging_seq', 'dst_mac_address', 'distance_cm', 'elevation1', 'azimuth1', 'x', 'y']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # 实时读取串口数据并写入CSV文件
        data_list = deque(maxlen=10)
        fig, ax = plt.subplots()

        def update_plot():
            ax.clear()
            distance_cm = [float(data['distance_cm']) for data in data_list]
            elevation1 = [float(data['elevation1']) for data in data_list]
            azimuth1 = [float(data['azimuth1']) for data in data_list]
            
            x = -np.array(distance_cm) * np.cos(np.radians(elevation1)) * np.sin(np.radians(azimuth1))
            y = np.array(distance_cm) * np.cos(np.radians(elevation1)) * np.cos(np.radians(azimuth1))

            # 绘制点
            ax.scatter(x, y, c=np.arange(len(data_list)), cmap='viridis')

            # 绘制渐变色线
            for i in range(len(data_list) - 1):
                ax.plot([x[i], x[i+1]], [y[i], y[i+1]], c='gray', alpha=0.5)

            # 绘制另外一条颜色不同的线
            x_last = x[-1] if len(x) > 0 else 0
            y_last = y[-1] if len(y) > 0 else 0
            ax.plot([0, x_last], [0, y_last], c='red')

            ax.set_xlim([-100, 100])  # X轴范围
            ax.set_ylim([-100, 100])  # Y轴范围

            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_title('Real-time Data Change')

        def on_data_received(data):
            print(data)  # 打印数据
            row = {
                '###': data[0],
                'ranging_seq': data[1].strip(),
                'dst_mac_address': data[2].strip(),
                'distance_cm': data[3].strip(),
                'elevation1': data[4].strip(),
                'azimuth1': data[5].strip(),
                'x': data[6].strip(),
                'y': data[7].strip(),
            }
            writer.writerow(row)
            data_list.append(row)
            update_plot()
            plt.pause(0.01)

            # 计算坐标值
            distance_cm = float(data[3])
            elevation1 = float(data[4])
            azimuth1 = float(data[5])
            x = distance_cm * np.cos(np.radians(elevation1)) * np.sin(np.radians(azimuth1))
            y = distance_cm * np.cos(np.radians(elevation1)) * np.cos(np.radians(azimuth1))

            # 打印坐标值
            print("Computed Coordinates:")
            print(f"X: {x}, Y: {y}")

        while True:  # 实时读取串口数据
            line = ser.readline().decode().strip()
            if line.startswith('###'):
                data = line.split(',')
                on_data_received(data)

    print("数据已保存到文件:", filename)
