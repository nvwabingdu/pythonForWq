# 将一个文件夹中的图片  每三张竖向拼合成一张图片并输出
import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def merge_images_vertical(images, save_path):
    """将多张图片竖向拼接成一张"""
    imgs = [Image.open(img) for img in images]

    # 统一宽度为最小宽度
    min_width = min(img.width for img in imgs)
    resized_imgs = [
        img.resize((min_width, int(img.height * min_width / img.width)))
        for img in imgs
    ]

    total_height = sum(img.height for img in resized_imgs)

    merged_img = Image.new("RGB", (min_width, total_height), (255, 255, 255))

    y_offset = 0
    for img in resized_imgs:
        merged_img.paste(img, (0, y_offset))
        y_offset += img.height

    merged_img.save(save_path)


def batch_merge(folder_path, output_folder, group_size=3):
    """批量处理文件夹中的图片，每 group_size 张拼成一张"""
    exts = (".jpg", ".jpeg", ".png", ".bmp")
    images = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(exts)
    ]
    images.sort()

    if not images:
        return False, "文件夹中没有找到图片"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    group = []
    index = 1

    for img in images:
        group.append(img)

        if len(group) == group_size:
            save_path = os.path.join(output_folder, f"merged_{index:03d}.jpg")
            merge_images_vertical(group, save_path)
            group = []
            index += 1

    # 不足 group_size 的剩余图片
    if group:
        save_path = os.path.join(output_folder, f"merged_{index:03d}.jpg")
        merge_images_vertical(group, save_path)

    return True, "拼接完成"


# ---------------- GUI 软件 ----------------

class MergeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片竖向拼接工具（每 3 张）")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        self.folder_path = ""
        self.output_path = ""

        tk.Label(root, text="图片竖向拼接工具", font=("微软雅黑", 16, "bold")).pack(pady=10)

        frame = ttk.Frame(root)
        frame.pack(pady=10)

        # 选择图片文件夹
        ttk.Button(frame, text="选择图片文件夹", command=self.select_folder).grid(row=0, column=0, padx=5)
        self.folder_label = ttk.Label(frame, text="未选择", width=40)
        self.folder_label.grid(row=0, column=1)

        # 选择输出文件夹
        ttk.Button(frame, text="选择输出文件夹", command=self.select_output).grid(row=1, column=0, padx=5, pady=10)
        self.output_label = ttk.Label(frame, text="未选择", width=40)
        self.output_label.grid(row=1, column=1)

        # 开始按钮
        ttk.Button(root, text="开始拼接", command=self.start_merge).pack(pady=20)

        self.status_label = ttk.Label(root, text="", foreground="green")
        self.status_label.pack()

    def select_folder(self):
        path = filedialog.askdirectory(title="选择图片文件夹")
        if path:
            self.folder_path = path
            self.folder_label.config(text=path)

    def select_output(self):
        path = filedialog.askdirectory(title="选择输出文件夹")
        if path:
            self.output_path = path
            self.output_label.config(text=path)

    def start_merge(self):
        if not self.folder_path or not self.output_path:
            messagebox.showerror("错误", "请先选择文件夹")
            return

        success, msg = batch_merge(self.folder_path, self.output_path)

        if success:
            messagebox.showinfo("完成", msg)
            self.status_label.config(text=msg)
            os.startfile(self.output_path)
        else:
            messagebox.showerror("失败", msg)
            self.status_label.config(text=msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = MergeApp(root)
    root.mainloop()
