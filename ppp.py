import serial
from serial.tools import list_ports
import csv
import time
from collections import deque

class SerialDataLogger:
    def __init__(self, target_description="USB to UART", baudrate=460800, csv_header=None, print_data=False):
        self.target_description = target_description
        self.baudrate = baudrate
        self.csv_header = csv_header
        self.print_data = print_data
        self.serial_port = None
        self.csv_writer = None
        self.data_list = deque(maxlen=10)

    def find_serial_port(self):
        ports = list_ports.comports()
        for port in ports:
            if self.target_description in port.description:
                return port.device
        return None

    def open_serial_port(self):
        port_name = self.find_serial_port()
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

    def create_parsed_data_file(self, filename):
        self.parsed_csv_file = open(filename, 'w', newline='')
        if self.csv_header:
            self.parsed_csv_writer = csv.DictWriter(self.parsed_csv_file, fieldnames=self.csv_header)
            self.parsed_csv_writer.writeheader()

    def update_data(self, data):
        if self.csv_writer:
            row = {}
            for item in data:
                key, value = item.split(':')
                row[key.strip()] = value.strip()
            self.csv_writer.writerow(row)
            self.csv_file.flush()  # Ensure data is written immediately
            # Parse data and write to parsed CSV file
            self.parsed_csv_writer.writerow(self.parse_data(row))
            self.parsed_csv_file.flush()  # Ensure data is written immediately
        self.data_list.append(row)

    def parse_data(self, data):
        # Example parsing logic
        parsed_data = {
            'Timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'Distance': data['Distance'],
            'AoAAzimuth': data['AoAAzimuth'],
            'AoAAzimuthFOM': data['AoAAzimuthFOM'],
            'AoAElevation': data['AoAElevation'],
            # Add more parsed fields as needed
        }
        return parsed_data

    def print_data(self):
        for row in self.data_list:
            print(row)

    def read_serial_data(self):
        while True:
            line = self.serial_port.readline().decode().strip()
            data = line.split(',')
            self.update_data(data)
            if self.print_data:
                print(data)

    def close(self):
        if self.serial_port:
            self.serial_port.close()
        if self.csv_file:
            self.csv_file.close()
        if self.parsed_csv_file:
            self.parsed_csv_file.close()

if __name__ == "__main__":
    target_description = "USB to UART"
    csv_header = ['sessionNumber', 'sessionID', 'MACAddress', 'status', 'Distance', 'AoAAzimuth', 'AoAAzimuthFOM', 'AoAElevation']
    parsed_csv_header = ['Timestamp', 'Distance', 'AoAAzimuth', 'AoAAzimuthFOM', 'AoAElevation']  # Add more fields as needed
    baudrate = 460800
    print_serial_data = True  # 设置为True以打印串口读取到的数据

    logger = SerialDataLogger(target_description, baudrate, csv_header, print_serial_data)
    if logger.open_serial_port():
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"data_{timestamp}.csv"
            parsed_filename = f"data_p_{timestamp}.csv"
            logger.create_csv_file(filename)
            logger.create_parsed_data_file(parsed_filename)
            logger.read_serial_data()
        except KeyboardInterrupt:
            pass
        finally:
            logger.close()
            print("Data logging stopped.")
    else:
        print("Unable to find the specified serial port.")
