from PyQt5.QtWidgets import (
    QMainWindow, QTextEdit, QLabel, QVBoxLayout, QWidget, QAction, 
    QGridLayout, QToolBar, QMessageBox, QPushButton, QDialog, 
    QFormLayout, QLineEdit, QDialogButtonBox,QFileDialog
)
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from serial_reader import SerialDataReader
from mqtt_client import MQTTClient
from real_time_plot import RealTimePlot

class MQTTGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.serial_reader = SerialDataReader()
        self.mqtt_client = MQTTClient()
        self.initUI()
        self.setup_connections()
        self.start_serial_thread()

    def initUI(self):
        self.setWindowTitle("MQTT客户端")
        self.setGeometry(100, 100, 800, 600)

        # 创建工具栏
        toolbar = QToolBar("工具栏")
        self.addToolBar(toolbar)

        pub_action = QAction("上传任务文件", self)
        pub_action.triggered.connect(self.btn_pub_send_task_file)
        toolbar.addAction(pub_action)

        sub_action = QAction("任务下发", self)
        sub_action.triggered.connect(self.btn_task_set)
        toolbar.addAction(sub_action)

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

        self.figure_mqtt = Figure()
        self.canvas_mqtt = FigureCanvas(self.figure_mqtt)
        self.canvas_mqtt.setFixedSize(200, 200)

        self.figure_uwb = Figure()
        self.canvas_uwb = FigureCanvas(self.figure_uwb)
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

    def setup_connections(self):
        self.mqtt_client.set_on_connect_callback(self.on_connect_status)
        self.mqtt_client.set_on_message_callback(self.on_message_received)
        self.mqtt_client.connect()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_connection_status)
        self.timer.start(1000)  # 每秒检查一次连接状态

    def start_serial_thread(self):
        self.serial_thread = SerialDataReaderThread(self.serial_reader)
        self.serial_thread.data_received.connect(self.update_display)
        self.serial_thread.start()

    def update_display(self, data):
        self.message_display.append(data)
        self.message_display.verticalScrollBar().setValue(
            self.message_display.verticalScrollBar().maximum()
        )

    def btn_pub_send_task_file(self):
        # 选择任务文件并上传
        file_path = self.open_file_dialog()
        if file_path:
            self.mqtt_client.pub_send_task_file(file_path)

    def btn_task_set(self):
        config = self.mqtt_client.get_config()
        task_set_msg = config["pub_config"]["task_set"]["task_set"]
        task_set_msg_temp = self.edit_task_set(task_set_msg)
        if task_set_msg_temp:
            self.mqtt_client.config["pub_config"]["task_set"]["task_set"] = task_set_msg_temp
            self.mqtt_client.pub_task_set()

    def edit_task_set(self, task_set_msg):
        dialog = QDialog(self)
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
        return None

    def open_file_dialog(self, file_name=False):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择文件",
            "",
            "JSON Files (*.json)",
            options=options,
        )
        if file_name:
            return os.path.basename(file_path)
        return file_path if file_path else None

    def on_connect_status(self, status):
        self.status_label.setText(f"{status}")
        self.host_label.setText(f"{self.mqtt_client.broker}")
        self.client_id_label.setText(f"{self.mqtt_client.client_id}")

    def on_message_received(self, msg):
        # 处理接收到的消息
        self.robot_message_label.setText(
            f"Robot Topic `{msg.topic}`: {msg.payload.decode()}"
        )

    def check_connection_status(self):
        self.status_label.setText(
            "已连接" if self.mqtt_client.is_connected() else "断开"
        )
