import os
import json
import time
import csv
from mqtt_client import MQTTClient
from serial_reader import SerialDataReader


class DataLogger:
    def __init__(self):
        self.mqtt_client = MQTTClient()
        self.mqtt_client.connect()
        self.config = self.mqtt_client.get_config()
        self.robot_topics = self.config.get("robot_topics", [])
        self.res_topics = self.config.get("res_topics", {})
        self.mqtt_client.subscribe(
            self.robot_topics + list(self.res_topics.values()))

        self.serial_reader = SerialDataReader()
        self.mqtt_res_obj = {}
        self.csv_file = self.setup_csv_file()
        self.mqtt_client.set_on_message_callback(self.on_message_received)

    def setup_csv_file(self):
        timestamp = time.strftime("%Y%m%d_%H%M%S")

        file_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "data", f"{timestamp}.csv")

        with open(file_path, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(["sessionNumber",
                             "PdoaFirst",
                             "PdoaSecond",
                             "PdoaThird",
                             "AoAElevation",
                             "AoAAzimuth",
                             "Distance",
                             "x",
                             "y",
                             "z",
                             "RSSI",
                             "timestamp", "local_angle", "local_x", "local_y", "current_task_id",
                            "task_status",  "current_robot_status","car_time",])
        return file_path

    def on_message_received(self, msg):
        # print(1)
        if msg.topic in self.robot_topics:
            if msg.topic == self.robot_topics[0]:
                self.handle_robot_heart_beat(msg)
            else:
                self.handle_robot_message(msg)
        elif msg.topic in self.res_topics.values():
            self.handle_res_message(msg)

    def handle_robot_heart_beat(self, msg):

        # msg_object = self.merge_data(msg)
        # self.plot_mqtt.update_plot(msg_object["local_x"], msg_object["local_y"])
        self.mqtt_res_obj = self.merge_data(msg)
        # print(self.mqtt_res_obj)
        # self.message_display.append(str(msg_object))
        # self.message_display.verticalScrollBar().setValue(
        #     self.message_display.verticalScrollBar().maximum()
        # )

    def str_to_obj(self, data):
        data = data.split(",")
        header = self.mqtt_client.config["headers"]
        # print(len(data),len(header))
        if len(data) != len(header)-1:
            return ""
        row = {key: data[i].strip() if i < len(
            data) else "" for i, key in enumerate(header)}
        row["timestamp"] = int(round(time.time() * 1000))
        return row

    def merge_data(self, msg):
        payload = json.loads(msg.payload)
        timestamp = payload.get("timestamp", "")
        pose = payload.get("pose", {})
        print(pose)
        return {
            "local_angle": pose.get("local_angle", 0),
            "local_x": pose.get("local_x", 0),
            "local_y": pose.get("local_y", 0),
            "current_task_id": payload.get("current_task_id", "未知"),
            "task_status": payload.get("task_status", "未知"),
            "current_robot_status": payload.get("current_robot_status", "未知"),
            "car_time": timestamp
        }

    def log_data(self, data):
        with open(self.csv_file, mode='a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            print(data)
            writer.writerow(data)

    def run(self):
        if not self.serial_reader.open_serial_port():
            print("Failed to open serial port.")
            return

        while True:
            try:
                data = self.serial_reader.read_serial_data()
                # print(data)

                data = self.str_to_obj(data)
                # print(data)

                if data == '':
                    continue
                data = dict(data, **self.mqtt_res_obj)
                print(data)

                if self.mqtt_res_obj:  # Only log if there is response data
                    self.log_data(data.values())

                time.sleep(0.1)  # Control the reading frequency
            except Exception as e:
                print(f"Error: {str(e)}")


if __name__ == "__main__":
    logger = DataLogger()
    logger.run()
