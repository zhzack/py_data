import serial.tools.list_ports
import csv
import time
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

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
        fieldnames = ['###', 'ranging_seq', 'dst_mac_address', 'distance_cm', 'elevation1', 'azimuth1', 'elevation2', 'azimuth2']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # 读取串口数据并写入CSV文件
        count = 0
        data_list = []
        while count < 100:  # 读取一百行数据后断开串口连接
            # 读取一行数据
            line = ser.readline().decode().strip()
            
            # 解析数据并写入CSV文件
            if line.startswith('###'):
                data = line.split(',')
                row = {
                    '###': data[0],
                    'ranging_seq': data[1].strip(),
                    'dst_mac_address': data[2].strip(),
                    'distance_cm': data[3].strip(),
                    'elevation1': data[4].strip(),
                    'azimuth1': data[5].strip(),
                    'elevation2': data[6].strip(),
                    'azimuth2': data[7].strip()
                }
                writer.writerow(row)
                data_list.append(row)
                count += 1
                print(row)  # 打印数据

        # 断开串口连接
        ser.close()

    print("数据已保存到文件:", filename)

    # 读取文件并生成折线图
    distance_cm = [float(data['distance_cm']) for data in data_list]
    elevation1 = [float(data['elevation1']) for data in data_list]
    azimuth1 = [float(data['azimuth1']) for data in data_list]
    x = range(1, len(distance_cm) + 1)

    plt.figure()
    plt.plot(x, distance_cm, label='distance_cm')
    plt.plot(x, elevation1, label='elevation1')
    plt.plot(x, azimuth1, label='azimuth1')
    plt.xlabel('Line Number')
    plt.ylabel('Value')
    plt.title('Real-time Data Change')
    plt.legend()
    plt.grid(True)

    # 保存折线图和关闭程序按钮
    ax_save = plt.axes([0.7, 0.01, 0.1, 0.05])
    ax_close = plt.axes([0.81, 0.01, 0.1, 0.05])
    button_save = Button(ax_save, 'Save Plot')
    button_close = Button(ax_close, 'Close Program')

    def save_plot(event):
        plot_timestamp = time.strftime("%Y%m%d_%H%M%S")
        plot_filename = f"plot_{plot_timestamp}.png"
        plt.savefig(plot_filename)
        print(f"折线图已保存到文件: {plot_filename}")

    def close_program(event):
        plt.close()

    button_save.on_clicked(save_plot)
    button_close.on_clicked(close_program)

    plt.show()
