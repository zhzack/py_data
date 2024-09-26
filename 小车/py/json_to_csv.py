import json
from typing import Counter
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

# 打开并读取 JSON 文件
with open('car_json/15m.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 定义用于存储数据的列表
local_x_values = []
local_y_values = []
task_status_values = []
local_angle_values = []
current_task_id_values=[]

# 访问 JSON 数据中的每个对象
for task in data:
    for msg in task['messages']:
        payload = json.loads(msg['payload'])
        pose = payload['pose']
        local_x = pose['local_x']
        local_y = pose['local_y']
        task_status = payload['task_status']
        local_angle = pose['local_angle']
        current_task_id = payload['current_task_id']
        arm_id = payload['arm_id']
        current_robot_status = payload['current_robot_status']

        # 只记录 task_status 不为 0 的数据
        if task_status == 2 and current_task_id != -1:
            local_x_values.append(local_x)
            local_y_values.append(local_y)
            current_task_id_values.append(current_task_id)
            local_angle_values.append(local_angle)

            # 检查 local_x 和 local_y 是否为 0
            # if local_x == 0 and local_y == 0:
            #     print(f"Timestamp: {payload['timestamp']}")
            if current_task_id == 0:
                print(f"Timestamp: {payload['timestamp']}")
max_current_task_id = max(current_task_id_values)
min_current_task_id = min(current_task_id_values)
# 打印结果
print(f"Max current_task_id: {max_current_task_id}")
print(f"Min current_task_id: {min_current_task_id}")        
        
# 创建索引列表
indexes = list(range(len(local_x_values)))
# 使用 Counter 统计 current_task_id 的出现次数

task_id_counts = Counter(current_task_id_values)

# 按 current_task_id 排序并打印结果
sorted_task_id_counts = sorted(task_id_counts.items())

# 打印统计结果
print("current_task_id 统计结果：")
for task_id, count in task_id_counts.items():
    print(f"Task ID: {task_id}, Count: {count}")


# # 创建渐变颜色
colors = plt.cm.cool(np.linspace(0, 1, len(local_x_values)))

# 绘制 local_x 和 local_y 的坐标点，使用渐变颜色表示方向
plt.figure(figsize=(10, 10))
plt.scatter(local_x_values, local_y_values, c=colors, cmap='cool', label='local_x vs local_y')
plt.xlabel('local_x')
plt.ylabel('local_y')
plt.title('local_x vs local_y with Gradient Color')
plt.legend()
plt.colorbar(label='Gradient from Blue to Green')

# 设置坐标轴等比例
plt.axis('equal')

# 绘制 local_x, local_y, task_status 和 local_angle 的变化曲线
plt.figure(figsize=(15, 10))

plt.subplot(3, 1, 1)
plt.plot(indexes, local_x_values, label='local_x')

plt.plot(indexes, local_y_values, label='local_y', color='orange')
plt.xlabel('Index')
plt.ylabel('distance')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(indexes, current_task_id_values, label='current_task_id', color='green')
plt.xlabel('Index')
plt.ylabel('task_status')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(indexes, local_angle_values, label='local_angle', color='red')
plt.xlabel('Index')
plt.ylabel('local_angle')
plt.legend()

plt.tight_layout()
plt.show()
