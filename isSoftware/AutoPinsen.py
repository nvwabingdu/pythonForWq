#目前用的客服回复工具，已经使用中
import tkinter as tk
from tkinter import scrolledtext
import pandas as pd
import pyperclip
import os
from PIL import Image
import io
import win32clipboard


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("客服辅助简化工具_wq")

        # 将窗口固定在最前面
        self.root.attributes('-topmost', True)

        # 自动查找文件路径
        self.file_path = os.path.join(os.path.expanduser("~"), "Desktop", "tool", "ps.xls")
        # 自动查找图片路径
        self.file_path_img = os.path.join(os.path.expanduser("~"), "Desktop", "tool", "photoInfo")

        # 创建按钮
        self.button = tk.Button(root, text="点击加载SKU", command=self.load_data)
        self.button.pack(pady=10)

        # 显示粘贴的文本
        self.pasted_text_label = tk.Label(root, text="", wraplength=300)
        self.pasted_text_label.pack(pady=5)

        # 创建瀑布流区域
        self.flow_frame = tk.Frame(root)
        self.flow_frame.pack(pady=10)

        # 创建文本显示框
        self.text_box = scrolledtext.ScrolledText(root, width=40, height=10)
        self.text_box.pack(pady=10)

        self.waterfall_labels = []  # 存储瀑布流标签的列表

    def create_waterfall(self):
        # 清除现有的瀑布流
        self.remove_waterfall()

        # 检查文件路径是否有效
        if not os.path.isfile(self.file_path):
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, "文件路径无效，请检查。")
            return

        data = pd.read_excel(self.file_path, header=None)

        # 获取剪贴板的内容
        clipboard_content = "_" + pyperclip.paste()
        self.pasted_text_label.config(text="当前sku是：" +clipboard_content)  # 显示粘贴的文本

        mIndex = -1
        # 遍历第一列的数据
        for index, value in enumerate(data.iloc[:, 0]):
            if value == clipboard_content:
                mIndex = index
                break

        if mIndex == -1:
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, "没有找到匹配内容。")
            return

        first_row = data.iloc[mIndex]

        # 处理数据，仅保留每个项中 '$' 前面的部分
        def get_before_colon(item):
            return item.split('$')[0] if isinstance(item, str) else item

        # 处理数据，仅保留每个项中 '$' 后面的部分
        def get_after_colon(item):
            return item.split('$')[1] if isinstance(item, str) and '$' in item else ''

        # '$' 后面的部分的点击事件
        def copy_image_to_clipboard(image_path):
            # 检查路径是否有效
            if not os.path.isfile(self.file_path_img+image_path):
                pyperclip.copy(image_path)
            # 打开图片
            else:
                image = Image.open(self.file_path_img+image_path)

                # 将图片转换为 RGBA 格式
                if image.mode != 'RGBA':
                 image = image.convert('RGBA')

                 # 创建一个字节流
                output = io.BytesIO()
                image.save(output, format='BMP')  # 以 BMP 格式保存
                data = output.getvalue()[14:]  # 跳过 BMP 头部

                # 复制到剪贴板
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                win32clipboard.CloseClipboard()

                print(f"已复制图片到剪贴板: {image_path}")
            self.text_box.delete(1.0, tk.END)  # 清除原本的文字
            self.text_box.insert(tk.END, f"{text}")
        # 模拟瀑布流组件
        columns = 3  # 每行显示的列数
        for index in range(1, len(first_row)):  # 从第二个数据开始
            item = first_row[index]
            before_colon = get_before_colon(item)
            after_colon = get_after_colon(item)

            # 跳过 NaN 值
            if pd.isna(before_colon):
                continue

            # 计算行和列
            row = (index - 1) // columns  # 减去 1 以适应从第二个数据开始
            column = (index - 1) % columns

            label = tk.Label(self.flow_frame, text=before_colon, borderwidth=1, relief="solid", padx=10, pady=5)
            label.grid(row=row, column=column, padx=5, pady=5)

            # 绑定鼠标事件
            label.bind("<Enter>", lambda e, text=after_colon: self.show_info(text))
            label.bind("<Leave>", lambda e: self.clear_info())
            label.bind("<Button-1>", lambda e, text=after_colon: copy_image_to_clipboard(text))

            # 存储标签以便后续删除
            self.waterfall_labels.append(label)

    def show_info(self, text):
        self.text_box.delete(1.0, tk.END)  # 清除原本的文字
        self.text_box.insert(tk.END, text)  # 显示提示文本

    def clear_info(self):
        self.text_box.delete(1.0, tk.END)  # 清空文本框

    def remove_waterfall(self):
        # 删除现有的瀑布流标签
        for label in self.waterfall_labels:
            label.destroy()
        self.waterfall_labels.clear()  # 清空存储的标签列表

    def load_data(self):
        # 加载数据并更新文本框
        self.create_waterfall()


# 创建主窗口
root = tk.Tk()
app = App(root)

# 启动主循环
root.mainloop()