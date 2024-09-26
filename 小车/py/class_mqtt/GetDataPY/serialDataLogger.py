import serial
from serial.tools import list_ports
import csv
import time
from collections import deque

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
            
    def update_data(self, data):
        if self.csv_writer:
            row = {}
            for i, key in enumerate(self.csv_header):

                if i < len(data):
                    row[key] = data[i].strip()
                else:
                    row[key] = ""
            row["timestamp"] = int(round(time.time() * 1000))
            self.csv_writer.writerow(row)
            self.csv_file.flush()

        self.data_list.append(row)

        


    def read_serial_data(self):
        while True:
            line = self.serial_port.readline().decode().strip()
            data = line.split(",")
            for i in range(len(data)):
                if ":" in data[i]:
                    data[i] = data[i].strip()
                    _, data[i] = data[i].split(":", 1)
            if len(data) == len(self.csv_header) - 1:
                self.update_data(data)
                if self.print_data:
                    print(data)

    def close(self):
        if self.serial_port:
            self.serial_port.close()
        if self.csv_file:
            self.csv_file.close()


if __name__ == "__main__":


    target_description = "USB to UART"
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
        "RSSI",
    ]

    headers = [
        "sessionNumber",
        "PdoaFirst",
        "PdoaSecond",
        "PdoaThird",
        "AoAElevation",
        "AoAAzimuth",
        "Distance",
        "x",
        "y",
        "z",
        "x1",
        "y1",
        "z1",
        "AoAAzimuth1",
    ]

    headers = [
        "sessionNumber",
        "PdoaFirst",
        "PdoaSecond",
        "PdoaThird",
        "AoAElevation",
        "AoAAzimuth",
        "Distance",
        "x",
        "y",
        "z",
        "DstPdoaFirst",
        "DstPdoaSecond",
        "DstPdoaThird",
        "RSSI",
        "timestamp",
    ]

    baudrate = 460800
    print_serial_data = 1
    max_lines = 400
    max_lines = 0

    logger = SerialDataLogger(
        target_description, baudrate, headers, print_serial_data, max_lines
    )
    if logger.open_serial_port():
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            logger.filename = f"data_{timestamp}.csv"
            logger.create_csv_file(logger.filename)
            logger.read_serial_data()
        except KeyboardInterrupt:
            print(logger.filename)

        finally:
            logger.close()
            print("Data logging stopped.")
