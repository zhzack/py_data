import os
import pandas as pd
import re

# 指定包含 CSV 文件的文件夹路径
folder_path = 'E:/UWB_Share/py_data/Data/20240828'

# 初始化一个字典来存储分类后的结果
categorized_results = {}

# 文件名解析正则表达式
filename_pattern = re.compile(r"data_(\d{6})_dis_(\d+)_ad(\d{2}[LR])\.csv")

# 遍历文件夹中的所有 CSV 文件
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        
        # 解析文件名
        match = filename_pattern.match(filename)
        if not match:
            continue  # 跳过不符合命名规范的文件
        
        time_str, distance, position = match.groups()
        
        # 读取 CSV 文件
        df = pd.read_csv(file_path)
        
        # 计算 PdoaFirst、PdoaSecond、PdoaThird 的统计值
        pdoa_stats = {
            'filename': filename,
            'time': time_str,
            'distance': int(distance),
            'position': position,
            'Pdoa01_max': df['PdoaFirst'].max(),
            'Pdoa01_min': df['PdoaFirst'].min(),
            'Pdoa01_mean': df['PdoaFirst'].mean(),
            'Pdoa01_median': df['PdoaFirst'].median(),
            
            'Pdoa20_max': df['PdoaSecond'].max(),
            'Pdoa20_min': df['PdoaSecond'].min(),
            'Pdoa20_mean': df['PdoaSecond'].mean(),
            'Pdoa20_median': df['PdoaSecond'].median(),
            
            'Pdoa12_max': df['PdoaThird'].max(),
            'Pdoa12_min': df['PdoaThird'].min(),
            'Pdoa12_mean': df['PdoaThird'].mean(),
            'Pdoa12_median': df['PdoaThird'].median(),
        }
        
        # 按时间、距离和位置进行分类
        key = (time_str, distance, position)
        if key not in categorized_results:
            categorized_results[key] = []
        
        # 将结果添加到对应分类中
        categorized_results[key].append(pdoa_stats)

# 将结果转换为 DataFrame，并分类保存为不同的表格
for key, stats in categorized_results.items():
    df = pd.DataFrame(stats)
    time_str, distance, position = key
    output_filename = f"results_{time_str}_dis_{distance}_ad{position}.csv"
    
    # 保存每个分类的结果为独立的 CSV 文件
    # df.to_csv(output_filename, index=False)
    # print(f"Saved {output_filename}")

# 如果需要汇总所有结果，也可以生成一个总表
all_results_df = pd.concat([pd.DataFrame(stats) for stats in categorized_results.values()], ignore_index=True)
all_results_df.to_csv('all_results_summary.csv', index=False)
print("Saved all_results_summary.csv")
