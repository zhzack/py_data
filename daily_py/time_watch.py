import tkinter as tk
from datetime import datetime, timedelta

# 定义QLOCKTWO时间矩阵
time_matrix = [
    ["I", "T", "I", "S", " ", "A", "S", "A", "M", "P", "M"],
    ["A", "C", "Q", "U", "A", "R", "T", "E", "R", "D", "C"],
    ["T", "W", "E", "N", "T", "Y", "F", "I", "V", "E", " "],
    ["H", "A", "L", "F", "S", "T", "E", "N", "F", "T", "O"],
    ["P", "A", "S", "T", "E", "R", "U", "N", "I", "N", "E"],
    ["O", "N", "E", "T", "W", "O", "T", "H", "R", "E", "E"],
    ["F", "O", "U", "R", "F", "I", "V", "E", "S", "I", "X"],
    ["S", "E", "V", "E", "N", "E", "I", "G", "H", "T", "T"],
    ["E", "L", "E", "V", "E", "N", "T", "W", "E", "L", "V"],
    ["T", "E", "N", "S", "E", "O", "C", "L", "O", "C", "K"]
]

# 创建时间词语的字典
time_words = {
    "IT IS": [(0, 0), (0, 1), (0, 2), (0, 3)],
    "A M": [(0, 5), (0, 6), (0, 7), (0, 8)],
    "P M": [(0, 9), (0, 10)],
    "QUARTER": [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8)],
    "TWENTY": [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5)],
    "FIVE": [(2, 6), (2, 7), (2, 8), (2, 9)],
    "HALF": [(3, 0), (3, 1), (3, 2), (3, 3)],
    "TEN": [(3, 5), (3, 6), (3, 7)],
    "PAST": [(4, 0), (4, 1), (4, 2), (4, 3)],
    "TO": [(3, 9), (3, 10)],
    "ONE": [(5, 0), (5, 1), (5, 2)],
    "TWO": [(5, 3), (5, 4), (5, 5)],
    "THREE": [(5, 6), (5, 7), (5, 8), (5, 9), (5, 10)],
    "FOUR": [(6, 0), (6, 1), (6, 2), (6, 3)],
    "FIVE_HOUR": [(6, 4), (6, 5), (6, 6), (6, 7)],
    "SIX": [(6, 8), (6, 9), (6, 10)],
    "SEVEN": [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4)],
    "EIGHT": [(7, 5), (7, 6), (7, 7), (7, 8), (7, 9)],
    "NINE": [(4, 7), (4, 8), (4, 9), (4, 10)],
    "TEN_HOUR": [(9, 0), (9, 1), (9, 2)],
    "ELEVEN": [(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5)],
    "TWELVE": [(8, 6), (8, 7), (8, 8), (8, 9), (8, 10)],
    "O'CLOCK": [(9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10)]
}

# 模拟时间的变量
simulated_time = datetime(2023, 1, 1, 0, 0)  # 从凌晨0点开始

# 更新模拟时间
def increment_time():
    global simulated_time
    simulated_time += timedelta(minutes=1)
    if simulated_time.day != 1:  # 重置为当天
        simulated_time = simulated_time.replace(day=1)

# 将时间转换为词语列表
def time_to_words():
    hour = simulated_time.hour % 12 or 12
    minute = simulated_time.minute
    print(hour, minute)

    words = ["IT IS"]
    if simulated_time.hour < 12:
        words.append("A M")
    else:
        words.append("P M")

    if minute == 0:
        words.append("O'CLOCK")
    elif 0 < minute < 5:
        words.append("FIVE")
        words.append("PAST")
    elif 5 <= minute < 10:
        words.append("FIVE")
        words.append("PAST")
    elif 10 <= minute < 15:
        words.append("TEN")
        words.append("PAST")
    elif 15 <= minute < 20:
        words.append("QUARTER")
        words.append("PAST")
    elif 20 <= minute < 25:
        words.append("TWENTY")
        words.append("PAST")
    elif 25 <= minute < 30:
        words.append("TWENTY")
        words.append("FIVE")
        words.append("PAST")
    elif 30 <= minute < 35:
        words.append("HALF")
        words.append("PAST")
    elif 35 <= minute < 40:
        words.append("TWENTY")
        words.append("FIVE")
        words.append("TO")
        hour = (hour % 12) + 1
    elif 40 <= minute < 45:
        words.append("TWENTY")
        words.append("TO")
        hour = (hour % 12) + 1
    elif 45 <= minute < 50:
        words.append("QUARTER")
        words.append("TO")
        hour = (hour % 12) + 1
    elif 50 <= minute < 55:
        words.append("TEN")
        words.append("TO")
        hour = (hour % 12) + 1
    elif 55 <= minute < 60:
        words.append("FIVE")
        words.append("TO")
        hour = (hour % 12) + 1

    if hour == 1:
        words.append("ONE")
    elif hour == 2:
        words.append("TWO")
    elif hour == 3:
        words.append("THREE")
    elif hour == 4:
        words.append("FOUR")
    elif hour == 5:
        words.append("FIVE_HOUR")
    elif hour == 6:
        words.append("SIX")
    elif hour == 7:
        words.append("SEVEN")
    elif hour == 8:
        words.append("EIGHT")
    elif hour == 9:
        words.append("NINE")
    elif hour == 10:
        words.append("TEN_HOUR")
    elif hour == 11:
        words.append("ELEVEN")
    elif hour == 12:
        words.append("TWELVE")

    return words

# 更新显示时间
def update_time():
    words = time_to_words()
    for row in range(10):
        for col in range(11):
            labels[row][col].config(fg="white", bg="black")  # 默认颜色
    for word in words:
        if word in time_words:
            for pos in time_words[word]:
                labels[pos[0]][pos[1]].config(fg="black", bg="white")
    increment_time()
    root.after(1000, update_time)  # 每秒更新一次

# 创建Tkinter GUI
root = tk.Tk()
root.title("QLOCKTWO 手表样例")

labels = [[tk.Label(root, text=time_matrix[row][col], font=("Helvetica", 24), width=2, height=1, fg="white", bg="black") for col in range(11)] for row in range(10)]
for row in range(10):
    for col in range(11):
        labels[row][col].grid(row=row, column=col, padx=2, pady=2)

update_time()  # 初次调用以显示时间

root.mainloop()
