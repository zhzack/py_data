import base64
from datetime import datetime
import random
import time
import json
import os
from paho.mqtt import client as mqtt_client


current_path = os.path.dirname(os.path.realpath(__file__))

# 配置文件路径
CONFIG_FILE_PATH = os.path.join(current_path, "config", "config.json")
# 配置默认配置文件路径
DEFAULT_CONFIG_FILE_PATH = os.path.join(current_path, "config", "default_config.json")
# 默认配置
DEFAULT_CONFIG = {}
with open(DEFAULT_CONFIG_FILE_PATH, "r") as file:
    DEFAULT_CONFIG = json.load(file)


# 加载配置
def load_config():
    try:
        if os.path.exists(CONFIG_FILE_PATH):
            with open(CONFIG_FILE_PATH, "r") as file:
                config = json.load(file)
                return config
        else:
            # 如果配置文件不存在，创建默认配置文件
            with open(CONFIG_FILE_PATH, "w") as file:
                json.dump(DEFAULT_CONFIG, file, indent=4)
            return DEFAULT_CONFIG
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Error reading config file, using default settings: {e}")
        return DEFAULT_CONFIG


# 读取配置文件
config = load_config()

# 从配置文件中读取 MQTT 参数
broker = config.get("broker")
port = config.get("port")
keepalive_interval = config.get("keepalive_interval")
username = config.get("username")
password = config.get("password")

# 随机生成 client_id
client_id = f"python-mqtt-{random.randint(0, 1000)}"

# 订阅需要处理的 topic
robot_topics = ["/sy/robot/heart_beat", "/sy/robot/message"]

user_topics = {
    "task_set": "/sy/user/task_set",
    "control": "/sy/user/control",
    "arm_set": "/sy/user/arm_set",
    "send_task_file": "/sy/user/send_task_file",
    "setting": "/sy/user/setting",
    "request_task_file": "/sy/user/request_task_file",
}

res_topics = {
    "task_set": "/sy/res/user/task_set",
    "control": "/sy/res/user/control",
    "setting": "/sy/res/user/setting",
    "send_task_file": "/sy/res/user/send_task_file",
    "request_task_file": "/sy/res/user/request_task_file",
}

# 任务相关的数据
user_data = {
    "task_set": config["task_set"],
    "control": config["control"],
    "arm_set": config["arm_set"],
    "send_task_file": config["send_task_file"],
    "setting": config["setting"],
    "request_task_file": config["request_task_file"],
}


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port, keepalive=keepalive_interval)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        if msg.topic in robot_topics:
            if msg.topic == robot_topics[0]:
                handle_robot_heart_beat(msg)
            else:
                handle_robot_message(msg)
        elif msg.topic in res_topics.values():
            handle_res_message(msg)

    for topic in robot_topics + list(res_topics.values()):
        client.subscribe(topic)
    client.on_message = on_message


def handle_robot_message(msg):
    print(f"Robot Topic `{msg.topic}`: {msg.payload.decode()}")


def handle_robot_heart_beat(msg):
    pass


def handle_res_message(msg):
    try:
        payload = json.loads(msg.payload.decode())
        code = payload.get("code", None)
        if msg.topic == res_topics["task_set"]:
            handle_task_set_response(payload, code)
        elif msg.topic == res_topics["control"]:
            handle_control_response(payload, code)
        elif msg.topic == res_topics["setting"]:
            handle_setting_response(payload, code)
        elif msg.topic == res_topics["send_task_file"]:
            handle_send_task_file_response(payload, code)
        elif msg.topic == res_topics["request_task_file"]:
            handle_request_task_file_response(payload, code)
    except json.JSONDecodeError:
        print(f"Received invalid JSON from `{msg.topic}`: {msg.payload.decode()}")


def handle_task_set_response(payload, code):
    print(f"Task Set Response: {payload}, code: {code}")


def handle_control_response(payload, code):
    print(f"Control Response: {payload}, code: {code}")


def handle_setting_response(payload, code):
    print(f"Setting Response: {payload}, code: {code}")


def handle_send_task_file_response(payload, code):
    print(f"Send Task File Response: {payload}, code: {code}")


def handle_request_task_file_response(payload, code):
    print(f"Request Task File Response: {payload}, code: {code}")


def read_file_as_base64(file_path):
    with open(file_path, "rb") as file:
        encoded_content = base64.b64encode(file.read()).decode("utf-8")
    return encoded_content


def pub_send_task_file(file_path, client):
    user_data["send_task_file"]["file_name"] = file_path.split("/")[-1]
    user_data["send_task_file"]["basecode"] = read_file_as_base64(file_path)
    publish(client, "send_task_file", json.dumps(user_data["send_task_file"]))


def publish(client, topic_key, message):
    if topic_key in user_topics:
        topic = user_topics[topic_key]
        result = client.publish(topic, message)
        status = result[0]
        if status == 0:
            print(f"Send `{message}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
    else:
        print(f"Topic key `{topic_key}` not found")


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()  # 开启非阻塞循环
    while True:
        time.sleep(5)  # 每5秒发送一次心跳消息
        task_set_ = user_data["task_set"]
        task_set_["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pub_send_task_file(
            f"{current_path}/CreatJsonforCirclePath/CirclePath_Rad2m.json", client
        )


if __name__ == "__main__":
    run()
