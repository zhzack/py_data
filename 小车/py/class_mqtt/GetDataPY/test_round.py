import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import calculate

class RotatingPointAnimation:
    def __init__(self, R=100, omega=2 * np.pi, num_revolutions=2, frames_per_revolution=360):
        # 定义参数
        self.R = R  # 点D的初始位置在(100, 0)
        self.omega = omega # 旋转角速度 (1周/秒)
        self.num_revolutions = num_revolutions  # 旋转圈数
        self.frames_per_revolution = frames_per_revolution
        self.total_frames = num_revolutions * frames_per_revolution  # 计算旋转所需的总帧数

        # 定义点A、B和C的位置
        self.A = np.array([-1, -np.sqrt(3) / 3])
        self.B = np.array([1, -np.sqrt(3) / 3])
        self.C = np.array([0, 2 * np.sqrt(3) / 3])
        self.AB_distance = np.linalg.norm(self.B - self.A)  # 点A和点B之间的距离

        # 存储距离和arcsin值的数组
        self.distances_DA = np.zeros(self.total_frames)
        self.distances_DB = np.zeros(self.total_frames)
        self.distances_DC = np.zeros(self.total_frames)
        self.arcsin_values1 = np.zeros(self.total_frames)
        self.arcsin_values2 = np.zeros(self.total_frames)
        self.arcsin_values3 = np.zeros(self.total_frames)
        self.angles = np.zeros(self.total_frames)  # 存储D点的方位角

        # 初始化图像
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 12))
        self.init_plot()

    def distance(self, point1, point2):
        return np.sqrt(np.sum((point1 - point2)**2))

    def init_plot(self):
        self.ax1.set_xlim(-110, 110)
        self.ax1.set_ylim(-110, 110)
        self.ax1.set_aspect('equal')

        self.D_marker, = self.ax1.plot([], [], 'ro')  # 点D
        self.ABC_line, = self.ax1.plot([], [], 'bo-')  # 点A、B和C
        self.D_trail, = self.ax1.plot([], [], 'r--')  # 点D的轨迹
        self.origin_line, = self.ax1.plot([], [], 'k-')  # 从原点到点D的线

        self.distance_line_DA, = self.ax2.plot([], [], label="Distance D-A")
        self.distance_line_DB, = self.ax2.plot([], [], label="Distance D-B")
        self.distance_line_DC, = self.ax2.plot([], [], label="Distance D-C")
        
        self.arcsin_line1, = self.ax2.plot([], [], label="arcsin((D-A) - (D-C) / d)")
        self.arcsin_line2, = self.ax2.plot([], [], label="arcsin((D-C) - (D-B) / d)")
        self.arcsin_line3, = self.ax2.plot([], [], label="arcsin((D-B) - (D-A) / d)")
        
        self.angle_line, = self.ax2.plot([], [], label="D Point Angle (degrees)", linestyle='--')

        self.ax2.set_xlim(0, self.num_revolutions)
        self.ax2.set_ylim(-200, 360)
        self.ax2.set_xlabel('Time (s)')
        self.ax2.set_ylabel('Distance / Arcsin Value / Angle')
        self.ax2.legend()

    def init(self):
        self.D_marker.set_data([], [])
        self.D_trail.set_data([], [])
        self.ABC_line.set_data([], [])
        self.origin_line.set_data([], [])
        self.distance_line_DA.set_data([], [])
        self.distance_line_DB.set_data([], [])
        self.distance_line_DC.set_data([], [])
        self.arcsin_line1.set_data([], [])
        self.arcsin_line2.set_data([], [])
        self.arcsin_line3.set_data([], [])
        self.angle_line.set_data([], [])
        return self.D_marker, self.D_trail, self.ABC_line, self.origin_line, self.arcsin_line1, self.arcsin_line2, self.arcsin_line3, self.angle_line

    def switch_line(self, line):
        if line == 'DA':
            self.distance_line_DA.set_data(self.distances_DA, self.arcsin_values1)
            self.arcsin_line1.set_data(self.distances_DA, self.arcsin_values1)
    
    def update(self, frame):
        t = frame / self.frames_per_revolution
        theta = self.omega * t
        y = -self.R * np.cos(theta)
        x = self.R * np.sin(theta)
        D = np.array([x, y])

        # 更新点D的位置
        self.D_marker.set_data(x, y)

        # 更新点D的轨迹
        if frame == 0:
            self.D_trail.set_data([x], [y])
        else:
            old_x, old_y = self.D_trail.get_data()
            self.D_trail.set_data(np.append(old_x, x), np.append(old_y, y))

        # 更新原点到点D的线
        self.origin_line.set_data([0, x], [0, y])

        # 计算距离
        d_D_A = self.distance(D, self.A)
        d_D_B = self.distance(D, self.B)
        d_D_C = self.distance(D, self.C)
        distance_diff1 = d_D_B - d_D_C
        distance_diff2 = d_D_A - d_D_B
        distance_diff3 = d_D_C - d_D_A

        # 计算中间值
        ratio1 = distance_diff1 / self.AB_distance 
        ratio2 = distance_diff2 / self.AB_distance 
        ratio3 = distance_diff3 / self.AB_distance 
        
        ratio0,offSet=calculate.process_values(ratio1*180, ratio2*180, ratio3*180)
        
        offSet+=60
        # print(np.degrees(theta))
        # if theta==np.radians(150):
        #     print(f"ratio*180:{ratio1*180,ratio2*180,ratio3*180}")

        # 计算反正弦值（弧度）
        arcsin_radians1 = np.arcsin(ratio1)
        arcsin_radians2 = np.arcsin(ratio2)
        arcsin_radians3 = np.arcsin(ratio3)
        
        arcsin_radians0 = np.arcsin(ratio0/180)

        # 将弧度转换为度数
        arcsin_degrees0 = np.degrees(arcsin_radians0)+offSet
        # print(f"np.degrees(arcsin_radians0):{np.degrees(arcsin_radians0)}arcsin_degrees0:{arcsin_degrees0},offSet:{offSet}")
        
        # arcsin_degrees1 = arcsin_degrees0
        
        arcsin_degrees1 = np.degrees(arcsin_radians1) 
        arcsin_degrees2 = np.degrees(arcsin_radians2)
        arcsin_degrees3 = np.degrees(arcsin_radians3)
        
        degress_list = [int(arcsin_degrees1),int(arcsin_degrees2),int(arcsin_degrees3)]
        
        # print(f"degress_list:{degress_list}")
        
        if 60 in degress_list or -60 in degress_list:
            # print(f"60ratio*180:{ratio1*180,ratio2*180,ratio3*180}")
            print(f"degress_list:{degress_list}")
        
        arcsin_degrees0,offset,x=calculate.process_degree1(arcsin_degrees1,arcsin_degrees2,arcsin_degrees3)
        
        
        
        # print(np.degrees(theta))
        
        # if abs(arcsin_degrees1-60)<=0.3:
        #     print(f"60ratio*180:{ratio1*180,ratio2*180,ratio3*180}")
        # if abs(arcsin_degrees1+60)<=0.3:
        #     print(f"-60ratio*180:{ratio1*180,ratio2*180,ratio3*180}")
        
        # if abs(arcsin_degrees1-30)<=0.2:
        #     print(f"30ratio*180:{ratio1*180,ratio2*180,ratio3*180}")
        # if abs(arcsin_degrees1+30)<=0.2:
        #     print(f"-30ratio*180:{ratio1*180,ratio2*180,ratio3*180}")
        

        # 保存距离
        self.distances_DA[frame] = d_D_A
        self.distances_DB[frame] = d_D_B
        self.distances_DC[frame] = d_D_C
        
        self.distances_DA[frame] = (arcsin_degrees0+offset)%360
        self.distances_DB[frame] = offset
        # self.distances_DA[frame] = ratio1*180
        # self.distances_DB[frame] = ratio2*180
        # self.distances_DC[frame] = ratio3*180
        
        self.arcsin_values1[frame] = arcsin_degrees1
        self.arcsin_values2[frame] = arcsin_degrees2
        self.arcsin_values3[frame] = arcsin_degrees3

        # 计算并保存方位角
        angle = (-np.degrees(theta) + 360) % 360  # 将角度范围限制在0-360度之间
        self.angles[frame] = angle

        # 更新曲线
        self.distance_line_DA.set_data(np.arange(frame + 1) / self.frames_per_revolution, self.distances_DA[:frame + 1])
        self.distance_line_DB.set_data(np.arange(frame + 1) / self.frames_per_revolution, self.distances_DB[:frame + 1])
        # self.distance_line_DC.set_data(np.arange(frame + 1) / self.frames_per_revolution, self.distances_DC[:frame + 1])
        self.arcsin_line1.set_data(np.arange(frame + 1) / self.frames_per_revolution, self.arcsin_values1[:frame + 1])
        self.arcsin_line2.set_data(np.arange(frame + 1) / self.frames_per_revolution, self.arcsin_values2[:frame + 1])
        self.arcsin_line3.set_data(np.arange(frame + 1) / self.frames_per_revolution, self.arcsin_values3[:frame + 1])
        self.angle_line.set_data(np.arange(frame + 1) / self.frames_per_revolution, self.angles[:frame + 1])

        # 更新ABC三角形的位置
        self.ABC_line.set_data([-1, 1, 0, -1], [-np.sqrt(3) / 3, -np.sqrt(3) / 3, 2 * np.sqrt(3) / 3, -np.sqrt(3) / 3])

        return self.D_marker, self.D_trail, self.ABC_line, self.origin_line, self.arcsin_line1, self.arcsin_line2, self.arcsin_line3, self.angle_line

    def animate(self):
        ani = FuncAnimation(self.fig, self.update, frames=range(self.total_frames), init_func=self.init, blit=False, interval=100)
        plt.show()

# 创建实例并运行动画
animation = RotatingPointAnimation()
animation.animate()
