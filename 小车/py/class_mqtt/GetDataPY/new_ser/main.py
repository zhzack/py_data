import time
import threading
from serial_data_logger import SerialDataLogger
from realtime_display import RealTimeDisplayApp
import tkinter as tk

def main(enable_gui=False):
    target_description = "USB to UART"
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
        "timestamp"
    ]

    baudrate = 460800
    print_serial_data = 1
    max_lines = 300

    logger = SerialDataLogger(target_description, baudrate, headers, print_serial_data, max_lines)
    if logger.open_serial_port():
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            logger.filename = f"data_{timestamp}.csv"
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
    args = parser.parse_args()

    main(enable_gui=args.gui)
