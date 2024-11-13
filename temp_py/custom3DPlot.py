import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
from dataProcessor import DataProcessor
import math
import filter

class Custom3DPlot:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
    
    @staticmethod
    def process_degree(degree1, degree2, degree3):
        values = [degree1, degree2, degree3]
        sorted_values = sorted(values)
        degreeX=60
        if sorted_values == [degree3, degree1, degree2]:
            return degree1,0
        elif sorted_values == [degree2, degree3, degree1]:
            return degree3,120
        elif sorted_values == [degree1, degree2, degree3]:
            return degree2,240
        
        elif sorted_values == [degree1, degree3, degree2] and degree1>=-degreeX:
            return degree1,0
        
        elif sorted_values == [degree3, degree2, degree1] and degree1<=degreeX:
            return degree1,0
        
        elif sorted_values == [degree3, degree2, degree1] and degree3>=-degreeX:
            return degree3,120
        
        elif sorted_values == [degree2, degree1, degree3] and degree3<=degreeX:
            return degree3,120
        
        elif sorted_values == [degree2, degree1, degree3] and degree2>=-degreeX:
            return degree2,240
        
        elif sorted_values == [degree1, degree3, degree2] and degree2<=degreeX:
            return degree2,240
        
        return degreeX,(0)

    @staticmethod
    def process_values(pdoa1, pdoa2, pdoa3):
        values = [pdoa1, pdoa2, pdoa3]
        sorted_values = sorted(values)
        pdoaX=156
        if sorted_values == [pdoa3, pdoa1, pdoa2]:
            return pdoa1,0
        elif sorted_values == [pdoa2, pdoa3, pdoa1]:
            return pdoa3,120
        elif sorted_values == [pdoa1, pdoa2, pdoa3]:
            return pdoa2,240
        
        elif sorted_values == [pdoa1, pdoa3, pdoa2] and pdoa1>=-pdoaX:
            return pdoa1,0
        
        elif sorted_values == [pdoa3, pdoa2, pdoa1] and pdoa1<=pdoaX:
            return pdoa1,0
        
        elif sorted_values == [pdoa3, pdoa2, pdoa1] and pdoa3>=-pdoaX:
            return pdoa3,120
        
        elif sorted_values == [pdoa2, pdoa1, pdoa3] and pdoa3<=pdoaX:
            return pdoa3,120
        
        elif sorted_values == [pdoa2, pdoa1, pdoa3] and pdoa2>=-pdoaX:
            return pdoa2,240
        
        elif sorted_values == [pdoa1, pdoa3, pdoa2] and pdoa2<=pdoaX:
            return pdoa2,240
        
        return pdoaX,(0)
    # 实时将pdoa转为角度0-360
    @staticmethod
    def process_pdoaToAng(pdoa_first, pdoa_second, pdoa_third):
        pdoa_first = np.where(pdoa_first>180,180,pdoa_first)
        pdoa_second = np.where(pdoa_second>180,180,pdoa_second)
        pdoa_third = np.where(pdoa_third>180,180,pdoa_third)
        pdoa_first = np.where(pdoa_first>-180,pdoa_first,-180)
        pdoa_second = np.where(pdoa_second>-180,pdoa_second,-180)
        pdoa_third = np.where(pdoa_third>-180,pdoa_third,-180)
        
        pdoa_first /=180
        pdoa_second /=180
        pdoa_third /=180
        
        # Custom3DPlot.process_values(pdoa_first,pdoa_second,pdoa_third)
        pdoa_ressult,pdoa_offset=Custom3DPlot.process_values(pdoa_first, pdoa_third,pdoa_second)
        
        # print(f"np.arcsin(pdoa_first):{np.arcsin(pdoa_first)}")
        # print(f"np.arcsin(pdoa_second):{np.arcsin(pdoa_second)}")
        # print(f"np.arcsin(pdoa_third):{np.arcsin(pdoa_third)}")
        
        
        arcsin_degrees1=np.degrees(np.arcsin(pdoa_first))
        arcsin_degrees2=np.degrees(np.arcsin(pdoa_second))
        arcsin_degrees3=np.degrees(np.arcsin(pdoa_third))
        # print(f"arcsin_degrees1:{arcsin_degrees1}")
        # print(f"arcsin_degrees2:{arcsin_degrees2}")
        # print(f"arcsin_degrees3:{arcsin_degrees3}")
        
        degree_result,degree_offset=Custom3DPlot.process_degree(arcsin_degrees1,arcsin_degrees2,arcsin_degrees3)
        return degree_result+degree_offset+60


    @staticmethod
    def plot_ang(filename):
        # 初始化结果数组
        results = []
        
        pdoa_ressults=[]


        # 逐行读取 CSV 文件
        df = pd.read_csv(filename)
        # pdoa0_first  = df['PdoaFirst']
        # pdoa0_second = df['PdoaSecond']
        # pdoa0_third  = df['PdoaThird']
        
        # pdoa0_first = np.where(pdoa0_first>180,180,pdoa0_first)
        # pdoa0_second = np.where(pdoa0_second>180,180,pdoa0_second)
        # pdoa0_third = np.where(pdoa0_third>180,180,pdoa0_third)
        
        # pdoa0_first = np.where(pdoa0_first>-180,pdoa0_first,-180)
        # pdoa0_second = np.where(pdoa0_second>-180,pdoa0_second,-180)
        # pdoa0_third = np.where(pdoa0_third>-180,pdoa0_third,-180)
        
        
        
        # arcsin_radians1 = np.arcsin(pdoa0_first/180)
        # arcsin_radians2 = np.arcsin(pdoa0_second/180)
        # arcsin_radians3 = np.arcsin(pdoa0_third/180)
        
        # arcsin_degrees1 = np.degrees(arcsin_radians1)
        # arcsin_degrees2 = np.degrees(arcsin_radians2)
        # arcsin_degrees3 = np.degrees(arcsin_radians3)
        
        
        
        # pdoa_offset = 180/214
        moving_avg_buffer1 = []
        moving_avg_data1 = []
        moving_avg_buffer2 = []
        moving_avg_data2 = []
        moving_avg_buffer3 = []
        moving_avg_data3 = []
        for index, row in df.iterrows():
            # 提取数据
            pdoa_first = row['PdoaFirst'] 
            pdoa_second = row['PdoaSecond'] 
            pdoa_third = row['PdoaThird'] 
            degree_result=Custom3DPlot.process_pdoaToAng(pdoa_first,pdoa_second,pdoa_third)
            
            
            # arcsin_radians = np.arcsin(pdoa_ressult/214)
            
            # 将弧度转换为度数
            # arcsin_degrees = np.degrees(arcsin_radians)+pdoa_offset

            # print(f"degree_result:{degree_result}")
            # 保存结果到数组中
            results.append(degree_result)
            # pdoa_ressults.append(pdoa_ressult)
            

        # 将结果转换为 numpy 数组（可选）
        results = np.array(results)
        pdoa_ressults = np.array(pdoa_ressults)


        # 创建一个图表
        plt.figure(figsize=(10, 6))

        # 绘制每个结果的折线图
        plt.plot(df.index, results, label=' degrees')
        # plt.plot(df.index, pdoa_ressults, label=' Pdoa')
        
        # plt.plot(df.index,arcsin_degrees0, label=' arcsin_degrees0')
        # plt.plot(df.index,arcsin_degrees1, label=' arcsin_degrees1')
        # plt.plot(df.index,arcsin_degrees2, label=' arcsin_degrees2')
        # plt.plot(df.index,arcsin_degrees3, label=' arcsin_degrees3')


        # 添加标题和标签
        plt.title("filename")
        plt.xlabel('Index')
        plt.ylabel('Degrees')
        plt.legend()

        # 显示图表
        plt.show()

    @staticmethod
    def plot_pdoa(filename):
        df = pd.read_csv(filename)
        # PdoaFirst,PdoaSecond,PdoaThird
        temp=200
        # 提取数据
        ratio1= df['PdoaFirst']/temp
        ratio2 = df['PdoaSecond']/temp
        ratio3= df['PdoaThird']/temp

        # 计算反正弦值（弧度）
        arcsin_radians1 = np.arcsin(ratio1)
        arcsin_radians2 = np.arcsin(ratio2)
        arcsin_radians3 = np.arcsin(ratio3)

        # 将弧度转换为度数
        arcsin_degrees1 = np.degrees(arcsin_radians1)
        arcsin_degrees2 = np.degrees(arcsin_radians2)
        arcsin_degrees3 = np.degrees(arcsin_radians3)

        # 绘制每个结果的折线图
        plt.plot(df.index, arcsin_degrees1, label='PdoaFirst (degrees)')
        plt.plot(df.index, arcsin_degrees2, label='PdoaSecond (degrees)')
        plt.plot(df.index, arcsin_degrees3, label='PdoaThird (degrees)')

        # 添加标题和标签
        plt.title('PDoA Values in Degrees')
        plt.xlabel('Index')
        plt.ylabel('Degrees')
        plt.legend()

        # 显示图表
        plt.show()

    @staticmethod
    def spherical_to_cartesian(azimuth, distance, elevation=0):
        # 将角度转换为弧度
        azimuth_rad = math.radians(azimuth)
        elevation_rad = math.radians(elevation)

        # 计算x, y, z
        x = distance * math.cos(elevation_rad) * math.cos(azimuth_rad)
        y = distance * math.cos(elevation_rad) * math.sin(azimuth_rad)
        z = distance * math.sin(elevation_rad)

        return x, y, z
 
    @staticmethod
    def plot_trajectory(filename):
        df = pd.read_csv(filename)
        
        # 提取数据
        ele = df['AoAElevation']
        azi = df['AoAAzimuth']
        rho = df['Distance']
        
        # azi = np.where(azi > 0, 90, -90)
        
        # # 将角度转换为弧度
        # theta = np.radians(ele)
        # phi = np.radians(azi)
        
        # # 计算新的笛卡尔坐标
        # zz = rho * np.sin(theta)
        # xx = rho * np.sin(phi) * np.cos(theta)
        # yy = rho * np.cos(phi) * np.cos(theta)

        # # 重新计算x1和y1的值
        # x1 = -xx
        # y1 = zz
        # z1 = yy
        
        # # 将计算结果添加到数据框
        # df['x1'] = x1
        # df['y1'] = y1
        
        # 提取 x, y 坐标用于绘制
        x = df['x']
        y = df['y']
        
        # 提取 x1, y1 坐标用于绘制
        x1 = df['x1']
        y1 = df['y1']
        
        # 轨迹点的数量
        num_points = len(df)
        
        # 创建从红色到蓝色的颜色映射
        colormap = plt.cm.jet
        normalize = plt.Normalize(vmin=0, vmax=num_points-1)
        
        # 创建一个标量映射器
        scalar_mappable = plt.cm.ScalarMappable(norm=normalize, cmap=colormap)
        
        # 绘制原始轨迹
        for i in range(num_points - 1):
            plt.plot(x[i:i+2], y[i:i+2], color=scalar_mappable.to_rgba(1))
        
        # 绘制新计算的轨迹点
        plt.scatter(x1, y1, color='green', label='New Points')
        
        # 在起点和终点处绘制标记点
        plt.scatter(x[0], y[0], color='red', label='Start (Original)')
        plt.scatter(x.iloc[-1], y.iloc[-1], color='blue', label='End (Original)')
        
        # 设置图表标题和轴标签，并显示图例
        plt.title('Trajectory')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.show()
      
    @staticmethod  
    def plot_data(filename,sdfs,dsgfdg):
        # 读取CSV文件
        df = pd.read_csv(filename)

        # 提取需要的数据
        x = df['sessionNumber']
        y_distance = df['Distance']
        y_azimuth = df['AoAAzimuth']
        y_elevation = df['AoAElevation']
        y_PdoaFirst =df['PdoaFirst']
        y_PdoaSecond =df['PdoaSecond']
        y_PdoaThird =df['PdoaThird']
        y_sum_pdoa = df['new_column'] =df['PdoaThird']+df['PdoaSecond']+df['PdoaFirst']
        # y_rssi = df['RSSI']
        
        # 使用DataProcessor处理数据
        columns=["PdoaFirst","PdoaSecond","PdoaThird"]
        
        y_s_PdoaFirst,y_s_PdoaSecond,y_s_PdoaThird =DataProcessor.process_data(df,columns,threshold=5, smooth_method='lowpass', sigma=2)
        # y_s_PdoaFirst  = DataProcessor.process_data(df, 'PdoaFirst', threshold=5, smooth_method='lowpass', sigma=2)
        # y_s_PdoaSecond = DataProcessor.process_data(df, 'PdoaSecond', threshold=5, smooth_method='lowpass', sigma=2)
        # y_s_PdoaThird  = DataProcessor.process_data(df, 'PdoaThird', threshold=5, smooth_method='lowpass', sigma=2)


        # 绘制折线图
        plt.figure(figsize=(10, 6))

        plt.plot(x, y_distance, label='Distance')
        plt.plot(x, y_azimuth, label='AoAAzimuth')
        plt.plot(x, y_elevation, label='AoAElevation')
        plt.plot(x, y_PdoaFirst, label='PdoaFirst')
        plt.plot(x, y_PdoaSecond, label='PdoaSecond')
        plt.plot(x, y_PdoaThird, label='PdoaThird')
        
        plt.plot(x, y_sum_pdoa, label='y_sum_pdoa')
        
        # plt.plot(x, y_s_PdoaFirst,  label='s_PdoaFirst')
        # plt.plot(x, y_s_PdoaSecond, label='s_PdoaSecond')
        # plt.plot(x, y_s_PdoaThird,  label='s_PdoaThird')
        
        
        # plt.plot(x, y_rssi, label='RSSI')
        

        plt.xlabel('sessionNumber')
        plt.ylabel('Value')
        plt.title(filename+str(sdfs)+"_"+str(dsgfdg))
        plt.legend()

        plt.grid(True)
        plt.show()

    @staticmethod
    def add_single_spherical_point(distance, azimuth, elevation):
        # 将球坐标转换为直角坐标
        x = -distance * np.cos(np.radians(elevation)) * np.sin(np.radians(azimuth))
        z = distance * np.cos(np.radians(elevation)) * np.cos(np.radians(azimuth))
        y = distance * np.sin(np.radians(elevation))
        return x,y,z
        
        
    def add_points_from_arrays(self, distances, azimuths, color='r'):
        for distance in distances:
            for azimuth in azimuths:
                print(distance,azimuth)
                x,y,z=self.add_single_spherical_point(distance, azimuth, 0,color)
                # 添加点到图中
                self.ax.scatter(x, y, z, color=color)
                self.ax.text(x, y, z, "text", color='g')
                
    def add_points(self, azimuth, distance):
        for length in distance:
            points = []
            for angle in azimuth:
                x = -length * np.sin(np.radians(angle))
                z = length * np.cos(np.radians(angle))
                y = 0
                points.append([x, y, z])
            points = np.array(points)
            self.ax.plot(points[:, 0], points[:, 1], points[:, 2], color='g')
        
        
    def set_axis_limits(self, xlim=(-150, 150), ylim=(-150, 150), zlim=(-150, 150)):
        self.ax.set_xlim(*xlim)
        self.ax.set_ylim(*ylim)
        self.ax.set_zlim(*zlim)
        
    def set_axis_labels(self, xlabel='X', ylabel='Y', zlabel='Z'):
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.set_zlabel(zlabel)
        
    def show_plot(self):
        # 调整视角
        self.ax.view_init(elev=0, azim=0)  # 将视角调整到俯视，或者设置其他角度

        plt.show()
        
if __name__ == "__main__":

    Custom3DPlot.plot_ang("C:/Users/hu.qt/Desktop/y2024617/不等高180-150cm距离70cm两圈.csv")

    # Custom3DPlot.plot_ang("C:/Users/hu.qt/Desktop/y2024617/不等高180-150cm距离70cm两圈.csv")