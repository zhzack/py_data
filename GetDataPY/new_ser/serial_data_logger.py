import serial
from serial.tools import list_ports
import csv
import time
from collections import deque
import sys
import threading


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
    def __init__(
        self,
        target_description="USB to UART",
        baudrate=460800,
        csv_header=None,
        print_data=False,
        max_lines=0,
    ):
        self.target_description = target_description
        self.baudrate = baudrate
        self.csv_header = csv_header
        self.print_data = print_data
        self.max_lines = max_lines
        self.serial_port = None
        self.csv_writer = None
        self.data_list = deque(maxlen=max_lines if max_lines > 0 else None)
        self.filename = ""
        self.start_time = 0
        self.end_time = 0
        self.last_session_id = -1
        self.filter = MovingAverageFilter(
            window_size=5
        )  # Initialize the filter with a window size of 5

    @staticmethod
    def find_serial_port(target_description="USB to UART"):
        ports = list_ports.comports()
        for port in ports:
            if target_description in port.description:
                return port.device
        return None

    def open_serial_port(self):
        port_name = SerialDataLogger.find_serial_port(self.target_description)
        if port_name:
            self.serial_port = serial.Serial(port_name, self.baudrate)
            return True
        else:
            return False

    def create_csv_file(self, filename):
        self.csv_file = open(filename, "w", newline="")
        if self.csv_header:
            self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=self.csv_header)
            self.csv_writer.writeheader()
            print("CSV file created with header:", self.csv_header)

    def update_data(self, data):
        if self.csv_writer:
            row = {}
            for i, key in enumerate(self.csv_header):
                if i < len(data):
                    row[key] = data[i].strip()
                else:
                    row[key] = ""
            row["timestamp"] = int(round(time.time() * 1000))

            temp = int(row["sessionNumber"])
            if self.last_session_id != -1:
                row["drop_count"] = temp - self.last_session_id-1
            else:
                row["drop_count"] = 0
            self.last_session_id = temp

            self.csv_writer.writerow(row)
            self.csv_file.flush()
            if self.print_data:
                print(row)
                # for key, value in row.items():
                #     pass
                #     print(f"{key}: {value}")
            else:
                print("Not printing data")
        self.data_list.append(row)

        if self.max_lines > 0 and len(self.data_list) >= self.max_lines:
            self.end_time = time.time()
            duration = self.end_time - self.start_time
            print("程序运行时间：", duration, "秒")
            sys.exit()

    def read_serial_data(self, update_gui_func=None):
        while True:
            try:
                line = self.serial_port.readline().decode().strip()
                data = line.split(",")
                for i in range(len(data)):
                    if ":" in data[i]:
                        data[i] = data[i].strip()
                        _, data[i] = data[i].split(":", 1)
                if len(data) == len(self.csv_header) - 2:
                    self.update_data(data)
                    
                    if update_gui_func and "Distance" in self.csv_header:
                        distance_index = self.csv_header.index("Distance")
                        temp = data[distance_index].replace(" ", "")
                        if temp != "65535":
                            update_gui_func(temp)
                else:
                    print("数据格式不正确，跳过该行数据：", line)
            except Exception as e:
                print("读取串口数据时发生错误：", e)

    def close(self):
        if self.serial_port:
            self.serial_port.close()
        if self.csv_file:
            self.csv_file.close()
