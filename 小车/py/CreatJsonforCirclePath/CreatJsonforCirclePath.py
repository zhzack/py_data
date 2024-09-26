import json
import os
import math
from datetime import datetime


def generate_circular_trajectory_json(radius, arc_length=0.1):
    task_name = (
        "CirclePath_Rad" + str(radius) + "m"
    )  # _'+datetime.now().strftime("%Y-%m-%d-%H%M%S")
    center = (0, radius)  # 圆心位置
    # 计算圆的周长
    circumference = 2 * math.pi * radius
    # 计算节点数量
    num_nodes = int(circumference / arc_length)
    # 节点数组
    nodes = []
    # 小数保留位数
    PointNm = 3
    # 初始化下一个30度倍数的角度阈值
    next_special_angle = 30
    # 已添加节点的数量
    next_special_angle_id = 0
    # 停留时间，单位秒
    stay_time = 3

    # 任务点id，中途停顿时的taskid
    taskId_points = []
    # 计算并添加圆周上的节点和特殊节点
    for i in range(num_nodes + 2):  # 包括最后一个节点
        theta = arc_length / radius * i

        # 转换弧度到度数
        degrees = math.degrees(theta)
        # 检查是否超过了下一个30度的倍数阈值
        while degrees >= next_special_angle:
            # 计算30度的倍数点的坐标
            special_theta = math.radians(next_special_angle)
            special_x = round(center[0] + radius * math.sin(special_theta), PointNm)
            special_y = round(center[1] - radius * math.cos(special_theta), PointNm)
            taskId_points.append(i + 1 + next_special_angle_id)
            special_node = {
                "id": i + 1 + next_special_angle_id,
                "pos": {"x": special_x, "y": special_y},
                "task": {
                    "task_id": i + 1 + next_special_angle_id,
                    "is_pre_defined": False,
                    "defined_id": -1,
                    "repeat_count": 1,
                    "task_nodes": [
                        {
                            "arm_id": 1,
                            "stay_time": stay_time,
                            "arm_pose": {
                                "x": 0.04,
                                "y": 0.03,
                                "z": 0.49,
                                "roll": -89.96,
                                "pitch": -3.56,
                                "yaw": 88.89,
                                "joint1": -4.712,
                                "joint2": -2.870,
                                "joint3": 2.491,
                                "joint4": -2.727,
                                "joint5": 3.122,
                                "joint6": -0.026,
                            },
                        }
                    ],
                },
            }
            nodes.append(special_node)
            next_special_angle_id += 1
            # 增加下一个30度的倍数
            next_special_angle += 30
            continue
        if math.degrees(theta) < 360:
            x = round(center[0] + radius * math.sin(theta), PointNm)
            y = round(center[1] - radius * math.cos(theta), PointNm)
            node = {"id": i + 1 + next_special_angle_id, "pos": {"x": x, "y": y}}
            nodes.append(node)
    data = {"task_name": task_name, "nodes": nodes}

    return json.dumps(data, indent=4, ensure_ascii=False), taskId_points


def save_json_to_file(json_data, task_name):
    # 获取当前日期
    current_date = datetime.now().strftime("%Y-%m-%d")
    # 获取当前文件名（不含扩展名）
    current_file_name = os.path.splitext(os.path.basename(__file__))[0]

    # 组合文件夹名称
    folder_name = f"{current_file_name}_{current_date}"
    folder_name = f"{current_file_name}"

    # 创建保存文件的文件夹
    os.makedirs(folder_name, exist_ok=True)

    # 生成保存文件的路径
    file_path = os.path.join(folder_name, f"{task_name}.json")

    # 将JSON数据保存到文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json_data)


def list_to_str():
    dia_list = [2, 3, 5, 8, 10, 15]
    list = []
    for i in dia_list:
        _, taskId_points = generate_circular_trajectory_json(i)
        for j in taskId_points:
            list.append(j)
    # print(list)
    return list


if __name__ == "__main__":
    # 设置参数
    radius = 3  # 半径为10
    current_path = os.path.dirname(os.path.realpath(__file__))
    print(f"current_path:{current_path}")

    arc_length = 0.1  # 两节点之间的弧长约为0.1米
    task_name = (
        "CirclePath_Rad" + str(radius) + "m"
    )  # _'+datetime.now().strftime("%Y-%m-%d-%H%M%S")
    task_name = os.path.join(current_path, task_name)
    print(f"task_name:{task_name}")
    list_to_str()

    # 生成圆形轨迹的JSON
    json_output, taskId_points = generate_circular_trajectory_json(radius)

    save_json_to_file(json_output, task_name)
    print(f"taskId_points:{taskId_points}")

    _, sdd = generate_circular_trajectory_json(3)
    print(f"taskId_points:{sdd}")
