import pandas as pd

# 1. 读取原始 CSV 文件
file_path = 'data_20240712_185445-5.csv'  # 替换成您的文件路径
df = pd.read_csv(file_path)

# 2. 筛选符合条件的数据
start_timestamp = 1720781094191
end_timestamp =   1720782030515
# start_time_stamp 
# end_time_stamp 1720783370027
# if time_stamp>1720778335400.00 and  time_stamp<1720780600485.00 :

filtered_df = df[(df['timestamp'] > start_timestamp) & (df['timestamp'] < end_timestamp)]

# 3. 将筛选后的数据保存到新的 CSV 文件
output_file_path = 'data_20240712_185445-5-n.csv'  # 替换成您希望保存的文件路径
filtered_df.to_csv(output_file_path, index=False)

print(f"Filtered data saved to {output_file_path}")
