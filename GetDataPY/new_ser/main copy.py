import time
import threading
import os
from serial_data_logger import SerialDataLogger
from realtime_display import RealTimeDisplayApp
import tkinter as tk

def main(enable_gui=False, print_serial_data=1,description=""):
    target_description = "16"
    headers = [
        "sessionNumber",
        "PdoaFirst",
        "PdoaSecond",
        "PdoaThird",
        "AoAElevation",
        "AoAAzimuth",
        "Distance",
        "x", "y", "z",
        "DstPdoaFirst",
        "DstPdoaSecond",
        "DstPdoaThird",
        "RSSI",
        "timestamp",
        "drop_count"
    ]

    baudrate = 460800
    print_serial_data = 1
    max_lines = 0

    logger = SerialDataLogger(target_description, baudrate, headers, print_serial_data, max_lines)
    if logger.open_serial_port():
        try:
            # 获取当前文件的上上一层目录
            grandparent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

            # 获取当天日期作为文件夹名称
            date_folder = time.strftime("%Y%m%d")

            # 创建保存数据的文件夹路径
            data_folder = os.path.join(grandparent_dir, "Data", date_folder)
            os.makedirs(data_folder, exist_ok=True)

            # 创建文件名，附加文件描述
            timestamp = time.strftime("%H%M%S")
            description_part = f"_{description}" if description else ""
            logger.filename = os.path.join(data_folder, f"data_{timestamp}{description_part}.csv")

            logger.create_csv_file(logger.filename)
            logger.start_time = time.time()

            if enable_gui:
                root = tk.Tk()
                app = RealTimeDisplayApp(root)

                serial_thread = threading.Thread(target=logger.read_serial_data, args=(app.update_label,))
                serial_thread.daemon = True
                serial_thread.start()

                app.start()
            else:
                logger.read_serial_data()

        except KeyboardInterrupt:
            print(logger.filename)
        finally:
            logger.close()
            print("Data logging stopped.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Serial Data Logger with optional GUI display.")
    parser.add_argument("--gui", action="store_true", help="Enable GUI display")
    # parser.add_argument("filename", type=str, help="The name of the file to process")   
    # parser.add_argument("--desc", type=str, default="", help="Description to append to the filename")
    parser.add_argument("--desc", type=str, default="", help="Description to append to the filename")
    args = parser.parse_args()

    main(enable_gui=args.gui, description=args.desc)
