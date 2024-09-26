import os
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from custom3DPlot import Custom3DPlot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import calculate
# from serialDataLogger import SerialDataLogger

class FileDragDropApp:
    def __init__(self, root, callback_function):
        self.root = root
        self.root.geometry("400x400")  # 设置窗口大小
        self.root.title("File Drag and Drop App")  # 设置窗口标题
        self.file_paths=[]

        # 创建一个标签用于显示文件路径
        self.label = tk.Label(self.root, text="拖拽文件到这里", bg="lightgray", font=("Helvetica", 12), padx=10, pady=10)
        self.label.pack(expand=True, fill=tk.BOTH)

        # 创建一个列表框用于显示文件列表
        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(expand=True, fill=tk.BOTH)

        # 绑定拖拽事件
        self.label.drop_target_register(DND_FILES)
        self.label.dnd_bind('<<Drop>>', self.on_drop)

        # 清除列表的按钮
        self.clear_button = tk.Button(self.root, text="清除列表", command=self.clear_list)
        
        self.clear_button.pack(side=tk.TOP, anchor=tk.NE)

        # 绑定列表元素点击事件
        self.listbox.bind("<Double-Button-1>", self.on_listbox_click)

        # 保存回调函数
        self.callback_function = callback_function

    def on_drop(self, event):
        csv_list=event.data.split()
        csv_list.sort()
        calculate.merge_csv_files(csv_list)
        
        for csv in csv_list:
            file_name = os.path.basename(csv)
            # file_name=file_name.replace('{','')
            # file_name=file_name.replace('}','')
            self.listbox.insert(tk.END, file_name)
            
            # calculate.data_ca(csv)
            
            if csv in self.file_paths:
                # print("元素已存在")
                pass
            else:
                # print("元素不存在")
                # print(csv)
                

                self.file_paths.append(csv)
                if len(csv_list)==1 :
                    Custom3DPlot.plot_data(csv, "", "")
                    
                    # Custom3DPlot.plot_trajectory(csv, "", "")

    def clear_list(self):
        self.listbox.delete(0, tk.END)
        self.file_paths.clear()
    
    
    
    @staticmethod
    def plot_spherical_coordinates(csv_file):
        # 从CSV文件中读取数据
        data = np.genfromtxt(csv_file, delimiter=',', skip_header=1)

        # 解析数据
        AoAElevation = np.radians(data[:, 7])  # 将俯仰角转换为弧度
        Distance = data[:, 4]
        AoAAzimuth = np.radians(data[:, 5])  # 将方位角转换为弧度

        # 将球面坐标系转换为笛卡尔坐标系
        # x = Distance * np.cos(AoAElevation) * np.sin(AoAAzimuth)
        # y = Distance * np.cos(AoAElevation) * np.cos(AoAAzimuth)
        # z = Distance * np.sin(AoAElevation)
        
        x = Distance * np.sin(np.radians(AoAElevation)) * np.sin(np.radians(AoAAzimuth))
        y = Distance * np.sin(np.radians(AoAElevation)) * np.cos(np.radians(AoAAzimuth))
        z = Distance * np.cos(np.radians(AoAElevation))

        # 绘制三维坐标系
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')

        # 绘制点
        ax.scatter(x, y, z, c='b', marker='o', label='Points')

        # 设置坐标轴标签
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('3D Coordinate System')

        plt.show()

    def on_listbox_click(self, event):
        # 获取选中的文件索引
        selection_index = self.listbox.curselection()
        if selection_index:
            file_index = selection_index[0]
            file_path = self.file_paths[file_index]

            print(file_path)
            calculate.data_ca(file_path)
            # 调用回调函数
            # SerialDataLogger.data_ca(file_path)
            # Custom3DPlot.plot_data(file_path, "", "")
            # Custom3DPlot.plot_trajectory(file_path)
            
            Custom3DPlot.plot_ang(file_path)
            
            
            # Custom3DPlot.plot_pdoa(file_path)
            
            # Custom3DPlot.plot_data("data_20240517_130045.csv","","")
            # FileDragDropApp.plot_spherical_coordinates(file_path)
            # df = pd.read_csv(file_path)
            


def main():
    # 创建一个Tkinter应用程序
    root = TkinterDnD.Tk()

    # 创建一个FileDragDropApp实例，并传入回调函数
    app = FileDragDropApp(root, None)

    # 运行程序
    root.mainloop()

if __name__ == "__main__":
    main()
