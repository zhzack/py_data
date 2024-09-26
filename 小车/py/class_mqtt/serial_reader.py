import serial
from serial.tools import list_ports
import time

class SerialDataReader:
    def __init__(self, target_description="USB to UART", baudrate=460800, timeout=1):
        self.target_description = target_description
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_port = None

    @staticmethod
    def find_serial_port(target_description="USB to UART"):
        ports = list_ports.comports()
        for port in ports:
            if target_description in port.description:
                return port.device
        return None

    def open_serial_port(self):
        port_name = SerialDataReader.find_serial_port(self.target_description)
        if port_name:
            self.serial_port = serial.Serial(port_name, self.baudrate, timeout=self.timeout)
            return True
        else:
            return False

    def read_serial_data(self):
        if self.serial_port is None:
            raise Exception("Serial port is not open")

        line = self.serial_port.readline().decode().strip()
        data = line.split(",")
        for i in range(len(data)):
            if ":" in data[i]:
                data[i] = data[i].strip()
                _, data[i] = data[i].split(":", 1)
        return data

    def close(self):
        if self.serial_port:
            self.serial_port.close()
