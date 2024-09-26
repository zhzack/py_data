import tkinter as tk

class RealTimeDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("实时串口数据展示")
        self.root.attributes('-fullscreen', True)
        self.label_var = tk.StringVar()
        self.label = tk.Label(root, textvariable=self.label_var, font=("Helvetica", 32), bg='green', fg='red')
        self.label.pack(expand=True, fill='both')
        self.root.bind("<Configure>", self.update_font_size)

    def update_label(self, value):
        self.update_background_color(value)
        self.label_var.set(f"{value} ")
        

    def update_font_size(self, event=None):
        new_size = min(self.root.winfo_width() // 2, self.root.winfo_height() // 2)
        self.label.config(font=("Helvetica", new_size))

    def update_background_color(self, value):
        value = str(value).replace(' ', '')
        if value == ' 65535':
            self.label.configure(fg='blue',bg='red')
        else:
            self.label.configure(fg='red',bg='white')

    def start(self):
        self.root.mainloop()
