import tkinter as tk
from tkinter import ttk
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RealTimeDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("实时串口数据展示")
        self.root.attributes('-fullscreen', True)
        
        # 主标签
        self.label_var = tk.StringVar()
        self.label = tk.Label(root, textvariable=self.label_var, font=("Helvetica", 32), bg='white', fg='red')
        self.label.pack(expand=True, fill='both')
        
        # 右下角的标签
        self.other_data_var = tk.StringVar()
        self.other_data_label = tk.Label(root, textvariable=self.other_data_var, font=("Helvetica", 16), bg='white', fg='blue')
        self.other_data_label.pack(side='bottom', anchor='se', padx=10, pady=10)
        
        # 图表区域
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 初始化图表数据
        self.x_data = []  # x 轴索引
        self.y_data = []  # y 轴值
        self.index = 0    # 数据点的索引
        
        self.ax.set_title("实时数据曲线")
        self.ax.set_xlabel("数据点")
        self.ax.set_ylabel("值")
        
        # 时间戳
        self.timestamp = int(time.time() * 1000)
        
        # 更新图表的定时器
        self.update_plot_interval = 100  # 更新频率（毫秒）
        self.update_plot()

        # 绑定窗口调整事件
        self.root.bind("<Configure>", self.update_font_size)

    def get_timestamp(self):
        return int(time.time() * 1000)
    
    def update_label(self, value):
        self.update_background_color(value)
        now_time = int(time.time() * 1000)
        dis_time = now_time - self.timestamp
        self.timestamp = now_time
        
        self.label_var.set(f"{value} ")
        self.other_data_var.set(f"{dis_time} ")
        
        if value != 65535:
            self.update_plot_data(value)
    
    def update_font_size(self, event=None):
        new_size = min(self.root.winfo_width() // 2, self.root.winfo_height() // 2)
        self.label.config(font=("Helvetica", new_size))

    def update_background_color(self, value):
        if value == '65535':
            self.label.configure(fg='green', bg='white')
        else:
            self.label.configure(fg='red', bg='white')

    def update_plot_data(self, value):
        # 更新数据
        self.x_data.append(self.index)
        self.y_data.append(value)
        self.index += 1
        
        # 只保留最近 100 个数据点
        if len(self.x_data) > 100:
            self.x_data.pop(0)
            self.y_data.pop(0)

        # 清空图表并重新绘制
        self.ax.clear()
        self.ax.plot(self.x_data, self.y_data, label="数据变化")
        self.ax.set_title("实时数据曲线")
        self.ax.set_xlabel("数据点")
        self.ax.set_ylabel("值")
        self.ax.legend()
        
        # 绘制图表
        self.canvas.draw()

    def update_plot(self):
        self.update_plot_data(0)  # 触发更新，初始值设置为 0
        self.root.after(self.update_plot_interval, self.update_plot)  # 定时器调用

    def start(self):
        self.root.mainloop()

# 示例代码来运行你的应用
if __name__ == "__main__":
    root = tk.Tk()
    app = RealTimeDisplayApp(root)
    app.start()
