import os
import json
import time
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QLabel,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QAction,
    QFileDialog,
    QGridLayout,
    QInputDialog,
    QDialog,
)
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QFormLayout,
    QLineEdit,
    QDialogButtonBox,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
)
from PyQt5.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QDialogButtonBox,
    QVBoxLayout,
    QToolBar,
)
from PyQt5.QtCore import QThread, pyqtSignal


from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mqtt_client import MQTTClient
from real_time_plot import RealTimePlot
from serial_reader import SerialDataReader


class SerialDataReaderThread(QThread):
    data_received = pyqtSignal(str)  # Signal to emit received data

    def __init__(self, reader):
        super().__init__()
        self.reader = reader
        self.running = True

    def run(self):
        while self.running:
            try:
                data = self.reader.read_serial_data()
                formatted_data = ", ".join(data)
                # print(data)
                self.data_received.emit(formatted_data)  # Emit data to GUI
            except Exception as e:
                self.data_received.emit(f"Error: {str(e)}")
            time.sleep(0.1)  # Sleep to prevent high CPU usage

    def stop(self):
        self.running = False


class MQTTGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.serial_reader = SerialDataReader()
        self.initUI()

        self.mqtt_client = MQTTClient()
        self.mqtt_client.set_on_connect_callback(self.on_connect_status)
        self.mqtt_client.set_on_message_callback(self.on_message_received)
        self.config = self.mqtt_client.get_config()
        self.robot_topics = self.config.get("robot_topics", [])
        self.res_topics = self.config.get("res_topics", {})
        # print(self.robot_topics, self.res_topics)
        self.mqtt_res_obj = {}

        self.mqtt_client.connect()
        self.mqtt_client.subscribe(self.robot_topics + list(self.res_topics.values()))

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_connection_status)
        self.timer.start(1000)  # 每秒检查一次连接状态

        self.plot_mqtt = RealTimePlot(self.canvas_mqtt)
        self.plot_uwb = RealTimePlot(self.canvas_uwb)

        if self.serial_reader.open_serial_port():
            self.start_serial_thread()
        else:
            self.message_display.setText("Failed to open serial port.")

    def initUI(self):
        self.setWindowTitle("MQTT客户端")
        self.setGeometry(100, 100, 800, 600)

        # # 创建菜单栏
        # menubar = self.menuBar()
        # menu = menubar.addMenu("菜单")

        # 创建发布和接收按钮
        pub_action = QAction("上传任务文件", self)
        pub_action.triggered.connect(self.btn_pub_send_task_file)
        # menu.addAction(pub_action)

        sub_action = QAction("任务下发", self)
        sub_action.triggered.connect(self.btn_task_set)
        # menu.addAction(sub_action)

        # 创建工具栏并添加按钮a和b
        toolbar = QToolBar("工具栏")
        self.addToolBar(toolbar)
        toolbar.addAction(sub_action)
        toolbar.addAction(pub_action)

        # 布局
        grid_layout = QGridLayout()
        self.status_label = QLabel("", self)
        self.host_label = QLabel("", self)
        self.client_id_label = QLabel("", self)
        self.task_status_label = QLabel("", self)
        self.current_task_id_label = QLabel("", self)
        self.current_robot_status_label = QLabel("", self)

        labels = [
            ("连接状态:", self.status_label),
            ("服务器地址:", self.host_label),
            ("客户端ID:", self.client_id_label),
            ("车辆状态:", self.task_status_label),
            ("任务ID:", self.current_task_id_label),
            ("机器人状态:", self.current_robot_status_label),
        ]

        for i, (text, widget) in enumerate(labels):
            grid_layout.addWidget(QLabel(text), 0, 2 * i)
            grid_layout.addWidget(widget, 0, 2 * i + 1)

        robot_message_main_layout = QVBoxLayout()
        robot_message_main_layout.addWidget(QLabel("系统消息", self))
        self.robot_message_label = QLabel("```", self)
        robot_message_main_layout.addWidget(self.robot_message_label)

        self.message_display = QTextEdit(self)
        self.message_display.setReadOnly(True)

        self.figure = Figure()
        self.canvas_mqtt = FigureCanvas(self.figure)
        self.canvas_mqtt.setFixedSize(200, 200)
        
        self.figure = Figure()
        self.canvas_uwb = FigureCanvas(self.figure)
        self.canvas_uwb.setFixedSize(200, 200)

        main_layout = QVBoxLayout()
        main_layout.addLayout(grid_layout)
        main_layout.addLayout(robot_message_main_layout)
        main_layout.addWidget(self.message_display)
        main_layout.addWidget(self.canvas_uwb)
        main_layout.addWidget(self.canvas_mqtt)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def start_serial_thread(self):
        self.serial_thread = SerialDataReaderThread(self.serial_reader)
        self.serial_thread.data_received.connect(self.update_display)
        self.serial_thread.start()

    def str_to_obj(self, data):
        data = data.split(",")
        # 将串口的数据与配置文件中的key对应起来
        header = self.mqtt_client.config["headers"]
        row = {}
        for i, key in enumerate(header):
            if i < len(data):
                row[key] = data[i].strip()
                # print("key:", key, "value:", row[key])
            else:
                row[key] = ""
        row["timestamp"] = int(round(time.time() * 1000))
        return row

    def update_display(self, data):
        # print("Received data:", data)
        data = self.str_to_obj(data)
        # self.plot_uwb.update_plot(int(data['x']),int(data['y']))
        # print("Converted data:", data)
        if self.mqtt_res_obj == {}:
            return
        data = dict(data, **self.mqtt_res_obj)
        
        # print("Formatted data:", data)
        self.message_display.append(str(data))

        print(data)
        # exit()
        self.message_display.verticalScrollBar().setValue(
            self.message_display.verticalScrollBar().maximum()
        )

    def show_message(self, title, message, is_warning=False):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Warning if is_warning else QMessageBox.Information)
        msg_box.exec_()

    def open_file_dialog(self, file_name=False):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        current_path = os.path.dirname(os.path.realpath(__file__))
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择文件",
            os.path.join(current_path, "CreatJsonforCirclePath"),
            "JSON Files (*.json)",
            options=options,
        )
        if file_name:
            return os.path.basename(file_path)
        return file_path if file_path else None

    def edit_task_set(self, task_set_msg):
        dialog = QDialog()
        dialog.setWindowTitle("设置任务")

        layout = QVBoxLayout()
        form_layout = QFormLayout()
        input_fields = {}

        for key, value in task_set_msg.items():
            if key == "task_file":
                file_button = QPushButton(task_set_msg["task_file"])
                file_button.clicked.connect(
                    lambda: file_button.setText(self.open_file_dialog(True))
                )
                form_layout.addRow(key, file_button)
                input_fields[key] = file_button
            else:
                input_field = QLineEdit(str(value))
                form_layout.addRow(key, input_field)
                input_fields[key] = input_field

        layout.addLayout(form_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        dialog.setLayout(layout)

        if dialog.exec_() == QDialog.Accepted:
            for key, input_field in input_fields.items():
                if key == "task_file":
                    task_set_msg[key] = input_field.text()
                else:
                    task_set_msg[key] = input_field.text()
            return task_set_msg
        else:
            return None

    def btn_pub_send_task_file(self):
        file_path = self.open_file_dialog()
        if file_path:
            self.mqtt_client.pub_send_task_file(file_path)

    def btn_task_set(self):
        config = self.mqtt_client.get_config()
        task_set_msg = config["pub_config"]["task_set"]["task_set"]
        # print(task_set_msg)
        task_set_msg_temp = self.edit_task_set(task_set_msg)
        # print(task_set_msg_temp)
        # if task_set_msg !=task_set_msg_temp:
        self.mqtt_client.config["pub_config"]["task_set"][
            "task_set"
        ] = task_set_msg_temp
        self.mqtt_client.pub_task_set()

        #     self.show_message("提示", "设置成功", is_warning=True)

        # self.show_message("提示", "接收成功", is_warning=True)

    def on_connect_status(self, status):
        self.status_label.setText(f"{status}")
        self.host_label.setText(f"{self.mqtt_client.broker}")
        self.client_id_label.setText(f"{self.mqtt_client.client_id}")

    def merge_data(self, msg):
        payload = json.loads(msg.payload)
        pose = payload.get("pose", {})
        task_status = payload.get("task_status", "未知")
        current_task_id = payload.get("current_task_id", "未知")
        time_stamp = payload.get("timestamp", "未知")
        current_robot_status = payload.get("current_robot_status", "未知")

        msg_object = {
            "local_angle": pose.get("local_angle", 0),
            "local_x": pose.get("local_x", 0),
            "local_y": pose.get("local_y", 0),
            "current_task_id": current_task_id,
            "latitude": pose.get("latitude", 0),
            "longitude": pose.get("longitude", 0),
            "altitude": pose.get("altitude", 0),
            "rev_time": int(time.time() * 1000),
            "timestamp": time_stamp,
            "task_status": task_status,
            "current_robot_status": current_robot_status,
            "topic": msg.topic,
        }

        self.task_status_label.setText(f"{task_status}")
        self.current_task_id_label.setText(f"{current_task_id}")
        self.current_robot_status_label.setText(f"{current_robot_status}")
        return msg_object

    def handle_robot_heart_beat(self, msg):
        msg_object = self.merge_data(msg)
        self.plot_mqtt.update_plot(msg_object["local_x"], msg_object["local_y"])
        self.mqtt_res_obj = self.merge_data(msg)
        # self.message_display.append(str(msg_object))
        # self.message_display.verticalScrollBar().setValue(
        #     self.message_display.verticalScrollBar().maximum()
        # )

    def handle_res_message(self, msg):
        try:
            payload = json.loads(msg.payload.decode())
            code = payload.get("code", None)
            print(code)
            topic_handlers = {
                self.res_topics.get("task_set"): self.handle_task_set_response,
                self.res_topics.get("control"): self.handle_control_response,
                self.res_topics.get("setting"): self.handle_setting_response,
                self.res_topics.get(
                    "send_task_file"
                ): self.handle_send_task_file_response,
                self.res_topics.get(
                    "request_task_file"
                ): self.handle_request_task_file_response,
            }
            handler = topic_handlers.get(msg.topic)
            if handler:
                handler(payload, code)
            else:
                print(f"Unhandled topic `{msg.topic}` with payload: {payload}")
        except json.JSONDecodeError:
            print(f"Received invalid JSON from `{msg.topic}`: {msg.payload.decode()}")

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

    def on_message_received(self, msg):
        if msg.topic in self.robot_topics:
            if msg.topic == self.robot_topics[0]:
                self.handle_robot_heart_beat(msg)
            else:
                self.handle_robot_message(msg)
        elif msg.topic in self.res_topics.values():
            self.handle_res_message(msg)

    def handle_robot_message(self, msg):
        self.robot_message_label.setText(
            f"Robot Topic `{msg.topic}`: {msg.payload.decode()}"
        )
        print(f"Robot Topic `{msg.topic}`: {msg.payload.decode()}")

    def check_connection_status(self):
        self.status_label.setText(
            "已连接" if self.mqtt_client.is_connected() else "断开"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MQTTGui()
    gui.show()
    sys.exit(app.exec_())
