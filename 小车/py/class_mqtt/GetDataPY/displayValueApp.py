import tkinter as tk
from tkinter import font as tkfont

class DisplayValueApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()

    def setup_window(self):
        self.root.attributes('-fullscreen', True)
        self.root.configure(background='black')

        self.display_label = tk.Label(self.root, text='', fg='white', bg='black')
        self.display_label.pack(expand=True)

        self.update_font_size()

        # 绑定退出全屏和关闭窗口的快捷键
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.root.bind("<q>", self.close_window)

    def update_font_size(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        font_size = min(screen_width, screen_height) // 5

        custom_font = tkfont.Font(size=font_size)
        self.display_label.configure(font=custom_font)

    def update_value(self, value):
        self.display_label.config(text=value)

    def exit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)

    def close_window(self, event=None):
        self.root.quit()

class Controller:
    def __init__(self, display_app):
        self.display_app = display_app

    def set_value(self, value):
        self.display_app.update_value(value)

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.display_app = DisplayValueApp(self.root)
        self.controller = Controller(self.display_app)

    def run(self):
        # self.root.after(1000, self.update_display)  # 示例：1秒后更新显示内容
        self.root.mainloop()

    def update_display(self):
        self.controller.set_value("Hello, World!")
        self.root.after(2000, self.update_display_again)  # 示例：再过2秒后再次更新显示内容

    def update_display_again(self):
        self.controller.set_value("New Value")

if __name__ == "__main__":
    app = MainApp()
    app.run()
