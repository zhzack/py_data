import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

class PathDisplayApp(QMainWindow):
    def __init__(self, file_path):
        super().__init__()
        self.setWindowTitle("轨迹展示")
        self.setGeometry(100, 100, 800, 600)
        self.points = []

        self.load_data(file_path)

    def load_data(self, file_path):
        """读取任务文件并提取节点数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                nodes = data.get("nodes", [])
                for node in nodes:
                    position = node.get('pos')
                    if position:
                        x = position.get('x')*100
                        y = position.get('y')*100
                        self.points.append((x, y))
        except Exception as e:
            print(f"读取任务文件时出错: {e}")

    def paintEvent(self, event):
        """绘制轨迹"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 设置画笔颜色和宽度
        pen = QPen(QColor(0, 0, 255), 2)
        painter.setPen(pen)

        # 绘制轨迹
        for i in range(1, len(self.points)):
            x1, y1 = self.points[i - 1]
            x2, y2 = self.points[i]
            # 反转y坐标以适应窗口坐标系，并转换为整数
            painter.drawLine(int(x1 + 400), int(300 - y1), int(x2 + 400), int(300 - y2))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    task_file_path = "CreatJsonforCirclePath/LinearPath.json"  # 替换为实际路径
    window = PathDisplayApp(task_file_path)
    window.show()

    sys.exit(app.exec_())
