import base64
from datetime import datetime
import random
import time
import json
import os
from paho.mqtt import client as mqtt_client
import threading


class MQTTClient:
    def __init__(self, queue):
        self.queue = queue
        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.config_path = os.path.join(
            self.current_path, "config", "config.json")
        self.default_config_path = os.path.join(
            self.current_path, "config", "default_config.json"
        )
        self.config = self.load_config()
        self.res_topics = self.config.get("res_topics", {})
        self.robot_topics = self.config.get("robot_topics", [])

        self.broker = self.config.get("broker")
        self.port = self.config.get("port")
        self.keepalive_interval = self.config.get("keepalive_interval")
        self.username = self.config.get("username")
        self.password = self.config.get("password")
        self.pub_config = self.config.get("pub_config")
        self.client_id = f"python-mqtt-{random.randint(0, 1000)}"
        self.client = mqtt_client.Client(
            mqtt_client.CallbackAPIVersion.VERSION1, self.client_id
        )

        # self.subscribe(self.robot_topics + list(self.res_topics.values()))

        self.on_connect_callback = None
        self.on_message_callback = None

        self.check_connection_interval = 1  # 每隔5秒检查一次连接
        self.check_connection_thread = None
        self.stop_checking = False  # 控制检查线程的退出

    # @property
    # def value(self):
    #     return self._value

    # @value.setter
    # def value(self, value):
    #     if self._value != value:
    #         print(f"Value changed from {self._value} to {value}")
    #     self._value = value

    def start_connection_check(self):
        """
        启动一个线程，定时检查 MQTT 连接状态。
        """
        self.stop_checking = False
        self.check_connection_thread = threading.Thread(
            target=self.check_connection_loop, daemon=True)
        self.check_connection_thread.start()

    def stop_connection_check(self):
        """
        停止检查线程。
        """
        self.stop_checking = True
        if self.check_connection_thread and self.check_connection_thread.is_alive():
            self.check_connection_thread.join()

    def check_connection_loop(self):
        """
        检查 MQTT 是否连接的循环函数。
        """
        print("检查mqtt连接")
        while not self.stop_checking:
            if not self.is_connected():
                print("MQTT 断开连接，正在尝试重连...")
                self.connect()
            time.sleep(self.check_connection_interval)

    def load_config(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as file:
                    return json.load(file)
            else:
                return self.load_default_config()
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"读取配置文件出错，使用默认设置: {e}")
            return self.load_default_config()

    def load_default_config(self):
        with open(self.default_config_path, "r") as file:
            default_config = json.load(file)
            with open(self.config_path, "w") as file:
                json.dump(default_config, file, indent=4)
            return default_config

    def save_config(self, new_config):
        """保存当前配置到文件中"""
        try:
            with open(self.config_path, "w") as file:
                json.dump(new_config, file, indent=4)
            print("配置已保存成功")
        except Exception as e:
            print(f"保存配置文件出错: {e}")

    def connect(self):

        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = self.on_connect
        try:
            self.client.connect(self.broker, self.port,
                                keepalive=self.keepalive_interval)

        except Exception as e:
            print(f'mqtt连接失败:{e}')
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        status = "连接到MQTT Broker!" if rc == 0 else f"连接失败，返回码 {rc}"
        print(status)
        if self.on_connect_callback:
            self.on_connect_callback(status)

    def subscribe(self, topics):
        print(topics)
        for topic in topics:
            self.client.subscribe(topic)
        self.client.on_message = self.on_message

    def on_message(self, client, userdata, msg):
        self.on_message_received(msg)
        if self.on_message_callback:
            self.on_message_callback(msg)

    def set_on_connect_callback(self, callback):
        print(f'mqtt连接状态:{callback}')
        self.on_connect_callback = (callback)

    def publish(self, topic, message):
        print(self.is_connected())
        result = self.client.publish(topic, message)
        status = result[0]
        if status == 0:
            print(f"发送消息到主题 `{topic}`成功")
        else:
            print(f"发送消息到主题 `{topic}` 失败")
        return status

    def read_file_as_base64(self, file_path):
        with open(file_path, "rb") as file:
            return base64.b64encode(file.read()).decode("utf-8")

    def pub_send_task_file(self, file_path):

        send_task_file = self.pub_config["send_task_file"]
        topic = send_task_file["topic"]
        data = send_task_file["send_task_file"]
        data["file_name"] = os.path.basename(file_path)
        data["basecode"] = self.read_file_as_base64(file_path)
        self.publish(topic, json.dumps(data))

    def pub_task_set(self):
        task_set = self.config["pub_config"]["task_set"]
        topic = task_set["topic"]
        data = task_set["task_set"]
        print("设置任务成功")

        self.save_config(self.config)

        self.publish(topic, json.dumps(data))

    def pub_task_control(self, cmd=0, start_from_id=0):
        # cmd
        # 0: 暂停任务
        # 1：开始任务
        # 2：任务终⽌
        # start_from_id
        # 任务节点按照1...N进⾏编号， start_from_id 标识从第⼏个任务点开始进⾏任务，之前编号的任
        # 务点将被跳过。
        control = self.config["pub_config"]["control"]
        topic = control["topic"]
        data = control["control"]
        data['cmd'] = cmd
        if start_from_id:
            data['start_from_id'] = start_from_id
        self.publish(topic, json.dumps(data))

    def pub_setting(self, heatbeat_interval=None, max_vehicle_speed_limit=None, min_vehicle_speed_limit=None, robot_arm_speed_rate=None):

        setting = self.config["pub_config"]["setting"]
        topic = setting["topic"]
        data = setting["setting"]
        if heatbeat_interval:
            # int值，表示多少毫秒ms上传依次
            data['heatbeat_interval'] = heatbeat_interval
        if max_vehicle_speed_limit:
            #   3.0, // double, 最⾼速度限制，km/h
            data['max_vehicle_speed_limit'] = max_vehicle_speed_limit
        if min_vehicle_speed_limit:
            #  1.0, // double, 最低速度限制, km/h
            data['min_vehicle_speed_limit'] = min_vehicle_speed_limit
        if robot_arm_speed_rate:
            #   0.25 // double，机械臂速度, m/s
            data['robot_arm_speed_rate'] = robot_arm_speed_rate

        self.publish(topic, json.dumps(data))

    def is_connected(self):
        isConnected = self.client.is_connected()
        if not isConnected:
            self.connect()
        return self.client.is_connected()

    def on_message_received(self, msg):
        # print(msg.topic)
        if msg.topic in self.robot_topics:
            if msg.topic == self.robot_topics[0]:
                self.handle_robot_heart_beat(msg)
            else:
                self.handle_robot_message(msg)
        elif msg.topic in self.res_topics.values():
            self.handle_res_message(msg)

    def merge_data(self, msg):
        payload = json.loads(msg.payload)
        pose = payload.get("pose", {})
        time_stamp = payload.get("timestamp", "未知")

        dt = datetime.strptime(time_stamp, '%Y-%m-%d %H:%M:%S')
        time_stamp = dt.timestamp()

        task_status = payload.get("task_status", "未知")
        current_robot_status = payload.get("current_robot_status", "未知")
        current_arm_status = payload.get("current_arm_status", "未知")
        current_task_id = payload.get("current_task_id", "未知")
        obstacle_status = payload.get("obstacle_status", "未知")
        battery_status = payload.get("battery_status", "未知")
        arm_id = payload.get("arm_id", "未知")
        arm_pose = payload.get("arm_pose", "未知")

        msg_object = {
            "local_angle": pose.get("local_angle", 0),
            "local_x": pose.get("local_x", 0),
            "local_y": pose.get("local_y", 0),
            "latitude": pose.get("latitude", 0),
            "longitude": pose.get("longitude", 0),
            "altitude": pose.get("altitude", 0),
            "rev_time": int(time.time() * 1000),
            "timestamp": time_stamp,
            "task_status": task_status,
            "current_task_id": current_task_id,
            "current_robot_status": current_robot_status,
            "current_arm_status": current_arm_status,
            "topic": msg.topic,
        }

        return msg_object

    def handle_robot_heart_beat(self, msg):
        msg_object = self.merge_data(msg)
        # x = float(msg_object["local_x"])*100-350
        # y = float(msg_object["local_y"])*100
        # cc = [{'car': {'x': x, 'y': -y,'StopFlag':1,'light_index':1}}]
        x = int((msg_object["local_x"])*100)
        y = int((msg_object["local_y"])*100)
        time = msg_object["timestamp"]
        cc = f'{time}, {x},{y}'

        # print(cc)
        self.queue.put(cc)

        # self.plot_mqtt.update_plot(msg_object["local_x"], msg_object["local_y"])
        # self.mqtt_res_obj = self.merge_data(msg)

        # self.message_display.append(str(msg_object))
        # self.message_display.verticalScrollBar().setValue(
        #     self.message_display.verticalScrollBar().maximum()
        # )

    def handle_robot_message(self, msg):
        # self.robot_message_label.setText(
        #     f"Robot Topic `{msg.topic}`: {msg.payload.decode()}"
        # )
        pass
        print(f"Robot Topic `{msg.topic}`: {msg.payload.decode()}")

    def handle_task_set_response(self, payload, code):
        print(f"Task Set Response: {payload}, code: {code}")

    def handle_control_response(self, payload, code):
        print(f"Control Response: {payload}, code: {code}")

    def handle_setting_response(self, payload, code):
        print(f"Setting Response: {payload}, code: {code}")

    def handle_send_task_file_response(self, payload, code):
        print(f"Send Task File Response: {payload}, code: {code}")
        # self.show_message(f"发布结果: {code}", f"{payload}")

    def handle_request_task_file_response(self, payload, code):
        print(f"Request Task File Response: {payload}, code: {code}")

    def handle_res_message(self, msg):
        try:
            payload = json.loads(msg.payload.decode())
            code = payload.get("code", None)
            # print(code)
            topic_handlers = {
                self.res_topics.get("task_set"):
                    self.handle_task_set_response,

                self.res_topics.get("control"):
                    self.handle_control_response,

                self.res_topics.get("setting"):
                    self.handle_setting_response,

                self.res_topics.get("send_task_file"):
                    self.handle_send_task_file_response,

                self.res_topics.get("request_task_file"):
                    self.handle_request_task_file_response,
            }
            handler = topic_handlers.get(msg.topic)
            if handler:
                handler(payload, code)
            else:
                print(f"Unhandled topic `{msg.topic}` with payload: {payload}")
        except json.JSONDecodeError:
            print(f"Received invalid JSON from `{
                  msg.topic}`: {msg.payload.decode()}")
