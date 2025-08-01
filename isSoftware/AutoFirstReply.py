import pyautogui
import time
import tkinter as tk
from tkinter import messagebox

def auto_reply(reply_count, interval):
    for _ in range(reply_count):
        pyautogui.hotkey('alt', 'w')
        time.sleep(interval)
        pyautogui.press('/')
        time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.1)
        pyautogui.press('enter')

    messagebox.showinfo("完成", "所有回复已发送！")

def start_reply():
    try:
        reply_count = int(entry_count.get())
        if reply_count <= 0:
            raise ValueError
        interval = float(entry_interval.get())
        if interval <= 0:
            raise ValueError
        auto_reply(reply_count, interval)
    except ValueError:
        messagebox.showerror("错误", "请输入有效的正整数和正浮点数！")

def increase_interval():
    current_value = float(entry_interval.get())
    entry_interval.delete(0, tk.END)
    entry_interval.insert(0, str(current_value + 1))

def decrease_interval():
    current_value = float(entry_interval.get())
    if current_value > 1:  # Prevent it from going below 1
        entry_interval.delete(0, tk.END)
        entry_interval.insert(0, str(current_value - 1))

# 创建主窗口
root = tk.Tk()
root.title("自动回复设置")

# 输入框和标签
label_count = tk.Label(root, text="请输入回复次数:")
label_count.grid(row=0, column=0, pady=10)

entry_count = tk.Entry(root)
entry_count.grid(row=0, column=1, pady=5)

label_interval = tk.Label(root, text="修改间隔秒数:")
label_interval.grid(row=1, column=0, pady=10)

# Create a frame for the interval entry and buttons
frame_interval = tk.Frame(root)
frame_interval.grid(row=1, column=1)

button_decrease = tk.Button(frame_interval, text="-", command=decrease_interval)
button_decrease.grid(row=0, column=0)

entry_interval = tk.Entry(frame_interval, width=5, justify='center')
entry_interval.insert(0, "3")  # Default interval isModule 3 seconds
entry_interval.grid(row=0, column=1)

button_increase = tk.Button(frame_interval, text="+", command=increase_interval)
button_increase.grid(row=0, column=2)

# 开始按钮
start_button = tk.Button(root, text="开始回复", command=start_reply)
start_button.grid(row=2, columnspan=2, pady=20)

# 运行主循环
root.mainloop()