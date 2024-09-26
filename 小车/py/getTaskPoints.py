import json
import matplotlib.pyplot as plt
from datetime import datetime
import csv
import os
import numpy as np
from CreatJsonforCirclePath.CreatJsonforCirclePath import generate_circular_trajectory_json
from CreatJsonforCirclePath.CreatJsonforCirclePath import list_to_str

def to_thirteen_digit_timestamp(datetime_str):
    """
    将日期时间字符串转换为十三位时间戳。
    
    参数:
        datetime_str (str): 日期时间字符串。
    
    返回:
        int: 十三位时间戳。
    """
    dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S:%f')
    timestamp = int(dt.timestamp() * 1000)  # 转换为毫秒
    return timestamp

def read_json(file_path, task_id_list,lastId,currentId):
    """
    读取JSON文件并提取特定任务ID的数据。
    
    参数:
        file_path (str): JSON文件路径。
        task_id_list (list): 任务ID列表。
    
    返回:
        list: 提取的消息列表。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading JSON file: {e}")
        return []

    msg_list = []
    
    start_time_stamp = 0
    end_time_stamp = 0
    for task in data:
        for msg in task['messages']:
            payload = json.loads(msg['payload'])
            current_task_id = payload['current_task_id']
            time_stamp = to_thirteen_digit_timestamp(msg['createAt'])
            if current_task_id == lastId:
                start_time_stamp=time_stamp
            if current_task_id == currentId or current_task_id in task_id_list:
                end_time_stamp=time_stamp
    print("start_time_stamp",start_time_stamp)
    print("end_time_stamp",end_time_stamp)

    for task in data:
        for msg in task['messages']:
            payload = json.loads(msg['payload'])
            pose = payload['pose']

            task_status = payload['task_status']
            current_task_id = payload['current_task_id']
            time_stamp = to_thirteen_digit_timestamp(msg['createAt'])
            
            if task_status == 2 :
                if time_stamp>start_time_stamp and time_stamp<end_time_stamp:
                    msg_object = {
                        'local_angle': pose['local_angle'],
                        'local_x': pose['local_x'],
                        'local_y': pose['local_y'],
                        'current_task_id': current_task_id,
                        'latitude': pose['latitude'],
                        'longitude': pose['longitude'],
                        'altitude': pose['altitude'],
                        'time': msg['createAt'],
                        'timestamp': time_stamp
                    }
                    msg_list.append(msg_object)


    return msg_list

def save_to_csv_with_headers(data, filename):
    """
    将数据保存到CSV文件中。
    
    参数:
        data (list): 要保存的数据列表。
        filename (str): CSV文件名。
    """
    # 获取目录路径
    directory = os.path.dirname(filename)

    # 创建目录
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    fieldnames = ['time', 'timestamp', 'local_x', 'local_y', 'local_angle', 'current_task_id', 'latitude', 'longitude', 'altitude']

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except IOError as e:
        print(f"Error writing to CSV file: {e}")
def find_subarray(source_array, target_array):
    len_source = len(source_array)
    len_target = len(target_array)

    # 遍历源数组中的每一个可能的起始位置
    for i in range(len_source - len_target + 1):
        # 检查从当前起始位置开始的子数组是否与目标数组匹配
        if np.array_equal(source_array[i:i+len_target], target_array):
            return i
    return -1  # 如果没有找到匹配的子数组，返回 -1

def main():
    dis_list=[2,3,5,8,10,15]
    
    for radius in dis_list:
        _, taskId_points = generate_circular_trajectory_json(radius)
        list=list_to_str()
        print(list)
        temp=find_subarray(list,taskId_points)
        
        print(temp)
        
        msg_list = read_json('car_json/15m.json', taskId_points,list[temp-1],taskId_points[-1])
        
        # save_to_csv_with_headers(msg_list, f'car1PathData/{radius}m.csv')

if __name__ == '__main__':
    main()