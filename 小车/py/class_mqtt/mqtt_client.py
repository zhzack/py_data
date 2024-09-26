import base64
from datetime import datetime
import random
import time
import json
import os
from paho.mqtt import client as mqtt_client


class MQTTClient:
    def __init__(self):
        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.config_path = os.path.join(self.current_path, "config", "config.json")
        self.default_config_path = os.path.join(
            self.current_path, "config", "default_config.json"
        )
        self.config = self.load_config()
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
        self.on_connect_callback = None
        self.on_message_callback = None

    # @property
    # def value(self):
    #     return self._value

    # @value.setter
    # def value(self, value):
    #     if self._value != value:
    #         print(f"Value changed from {self._value} to {value}")
    #     self._value = value

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

    def get_config(self):
        self.config =self.load_config()
        
        return self.config

    def connect(self):
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = self.on_connect
        self.client.connect(self.broker, self.port, keepalive=self.keepalive_interval)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        status = "连接到MQTT Broker!" if rc == 0 else f"连接失败，返回码 {rc}"
        if self.on_connect_callback:
            self.on_connect_callback(status)

    def subscribe(self, topics):
        for topic in topics:
            self.client.subscribe(topic)
        self.client.on_message = self.on_message

    def on_message(self, client, userdata, msg):
        if self.on_message_callback:
            self.on_message_callback(msg)

    def set_on_connect_callback(self, callback):
        self.on_connect_callback = callback

    def set_on_message_callback(self, callback):
        self.on_message_callback = callback

    def publish(self, topic, message):
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
        self.publish(topic, json.dumps(data))

    def is_connected(self):
        return self.client.is_connected()

    def run(self, user_data, robot_topics, res_topics):
        self.connect()
        self.subscribe(robot_topics + list(res_topics.values()))
        # while True:
        #     time.sleep(5)
        #     task_set_ = user_data["task_set"]
        #     task_set_["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #     self.pub_send_task_file(
        #         f"{os.path.dirname(os.path.realpath(__file__))}/CreatJsonforCirclePath/CirclePath_Rad2m.json", user_data
        #     )


# 使用示例（假设其他必要的代码如用户数据和主题已定义）：

# if __name__ == "__main__":
#     current_path = os.path.dirname(os.path.realpath(__file__))
#     config_path = os.path.join(current_path, "config", "config.json")
#     default_config_path = os.path.join(current_path, "config", "default_config.json")

#     mqtt_client = MQTTClient(config_path, default_config_path)

#     def on_connect_status(status):
#         print(status)

#     def on_message_received(msg):
#         print(f"收到消息: {msg.topic} {msg.payload.decode()}")

#     mqtt_client.set_on_connect_callback(on_connect_status)
#     mqtt_client.set_on_message_callback(on_message_received)

#     user_data = {
#         "task_set": {"task": "example_task"},
#         "control": {},
#         "arm_set": {},
#         "send_task_file": {},
#         "setting": {},
#         "request_task_file": {},
#     }

#     robot_topics = ["/sy/robot/heart_beat", "/sy/robot/message"]
#     res_topics = {
#         "task_set": "/sy/res/user/task_set",
#         "control": "/sy/res/user/control",
#         "setting": "/sy/res/user/setting",
#         "send_task_file": "/sy/res/user/send_task_file",
#         "request_task_file": "/sy/res/user/request_task_file",
#     }

#     mqtt_client.run(user_data, robot_topics, res_topics)
