#文件说明
#1.全屏化，通过鼠标拉框的方式，将拉动的框的位置打印出来
import tkinter as tk

class FloatingBox:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # 去掉边框
        self.root.attributes("-topmost", True)  # 置于所有窗口之上
        self.root.attributes("-alpha", 0.5)  # 设置窗口透明度

        # 设置窗口为全屏
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")

        self.root.bind("<ButtonPress-1>", self.on_button_press)
        self.root.bind("<B1-Motion>", self.on_mouse_drag)
        self.root.bind("<ButtonRelease-1>", self.on_button_release)

        self.canvas = tk.Canvas(root, bg='lightgray', width=self.screen_width, height=self.screen_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.rect = None
        self.start_x = None
        self.start_y = None

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red',
                                                 width=2)

    def on_mouse_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        end_x, end_y = event.x, event.y
        box_position = (self.start_x, self.start_y, end_x, end_y)
        print("选定区域位置:", box_position)  # 打印框的位置

        # 清除框并关闭应用
        self.canvas.delete(self.rect)
        self.root.destroy()  # 关闭应用

if __name__ == "__main__":
    root = tk.Tk()
    app = FloatingBox(root)
    root.mainloop()