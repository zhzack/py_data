import tkinter as tk
from tkinter import scrolledtext
from mqtt_client import MQTTClient
import os
import json
from datetime import datetime

class MQTTGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MQTT客户端")
        self.geometry("800x600")
        
        self.status_label = tk.Label(self, text="连接状态: 未连接")
        self.status_label.pack(pady=10)
        
        self.host_label = tk.Label(self, text="服务器地址: 未知")
        self.host_label.pack(pady=10)
        
        self.client_id_label = tk.Label(self, text="客户端ID: 未知")
        self.client_id_label.pack(pady=10)
        
        self.message_display = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=100, height=30)
        self.message_display.pack(pady=10)
        
        current_path = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(current_path, "config", "config.json")
        default_config_path = os.path.join(current_path, "config", "default_config.json")
        
        self.mqtt_client = MQTTClient(config_path, default_config_path)
        self.mqtt_client.set_on_connect_callback(self.on_connect_status)
        self.mqtt_client.set_on_message_callback(self.on_message_received)
        
        self.user_data = {
            "task_set": {
                "task": "example_task"
            },
            "control": {},
            "arm_set": {},
            "send_task_file": {},
            "setting": {},
            "request_task_file": {}
        }
        
        self.robot_topics = ["/sy/robot/heart_beat", "/sy/robot/message"]
        self.res_topics = {
            "task_set": "/sy/res/user/task_set",
            "control": "/sy/res/user/control",
            "setting": "/sy/res/user/setting",
            "send_task_file": "/sy/res/user/send_task_file",
            "request_task_file": "/sy/res/user/request_task_file",
        }
        
        self.mqtt_client.connect()
        self.mqtt_client.subscribe(self.robot_topics + list(self.res_topics.values()))
        
        self.check_connection_status()

    def on_connect_status(self, status):
        self.status_label.config(text=f'连接状态: {status}')
        if "连接到" in status:
            self.host_label.config(text=f'服务器地址: {self.mqtt_client.broker}')
            self.client_id_label.config(text=f'客户端ID: {self.mqtt_client.client_id}')
    
    def on_message_received(self, msg):
        self.message_display.insert(tk.END, f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - {msg.topic}: {msg.payload.decode()}\n')
        self.message_display.yview(tk.END)  # 自动滚动到最后
    
    def check_connection_status(self):
        if self.mqtt_client.is_connected():
            self.status_label.config(text='连接状态: 已连接')
        else:
            self.status_label.config(text='连接状态: 断开')
        self.after(1000, self.check_connection_status)  # 每秒检查一次连接状态

if __name__ == '__main__':
    app = MQTTGui()
    app.mainloop()
