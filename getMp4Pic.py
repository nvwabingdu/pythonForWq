import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# 按时间间隔抽取帧：每 N 秒保存一张
def extract_frame_by_second(video_path, save_folder, per_second, progress_bar, root):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return False, "无法打开视频文件，请检查视频是否损坏"

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    # 每多少帧抽一张
    step_frame = int(fps * per_second)

    save_count = 0
    last_progress = -1

    for frame_idx in range(0, total_frames, step_frame):
        # 跳到目标帧（极大提升速度）
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            break

        save_path = os.path.join(save_folder, f"pic_{save_count:03d}.jpg")
        cv2.imwrite(save_path, frame)
        save_count += 1

        # 更新进度（只在变化时更新）
        progress = int((frame_idx / total_frames) * 100)
        if progress != last_progress:
            progress_bar["value"] = progress
            root.update()
            last_progress = progress

    progress_bar["value"] = 100
    cap.release()
    return True, f"提取完成！每 {per_second} 秒一张，共保存 {save_count} 张"


# 图形界面
class VideoFrameExtractApp:
    def __init__(self, root):
        self.root = root
        self.root.title("视频按秒抽帧工具（带进度条）")
        self.root.geometry("620x380")
        self.root.resizable(False, False)

        self.video_path = ""
        self.save_folder = ""

        # 标题
        tk.Label(root, text="视频按秒自动抽帧工具", font=("微软雅黑", 16, "bold")).pack(pady=10)

        frame = ttk.Frame(root)
        frame.pack(pady=10, padx=20, fill="x")

        # 选择视频
        ttk.Button(frame, text="选择视频", command=self.select_video).grid(row=0, column=0, padx=5)
        self.video_label = ttk.Label(frame, text="未选择视频", width=45)
        self.video_label.grid(row=0, column=1)

        # 保存目录
        ttk.Button(frame, text="保存位置", command=self.select_save_folder).grid(row=1, column=0, padx=5, pady=10)
        self.save_label = ttk.Label(frame, text="未选择保存目录", width=45)
        self.save_label.grid(row=1, column=1)

        # 设置多少秒抽一张
        ttk.Label(frame, text="每多少秒抽一张：").grid(row=2, column=0, padx=5)
        self.second_var = tk.StringVar(value="5")
        ttk.Entry(frame, textvariable=self.second_var, width=12).grid(row=2, column=1, sticky="w")

        # 进度条
        ttk.Label(root, text="提取进度：").pack(pady=(15,5))
        self.progress_bar = ttk.Progressbar(root, length=500, mode="determinate")
        self.progress_bar.pack()

        # 开始按钮
        self.start_btn = ttk.Button(root, text="开始提取", command=self.start_extract, state="disabled")
        self.start_btn.pack(pady=15)

        # 状态文字
        self.status_label = ttk.Label(root, text="", foreground="green")
        self.status_label.pack()

    def select_video(self):
        path = filedialog.askopenfilename(
            title="选择视频文件",
            filetypes=[("视频文件", "*.mp4 *.mov *.avi *.flv *.mkv *.wmv"), ("所有文件", "*.*")]
        )
        if path:
            self.video_path = path
            self.video_label.config(text=os.path.basename(path))
            self.check_ready()

    def select_save_folder(self):
        path = filedialog.askdirectory(title="选择图片保存文件夹")
        if path:
            self.save_folder = path
            self.save_label.config(text=path)
            self.check_ready()

    def check_ready(self):
        if self.video_path and self.save_folder:
            self.start_btn.config(state="normal")

    def start_extract(self):
        # 校验输入
        try:
            sec = float(self.second_var.get())
            if sec <= 0:
                messagebox.showerror("错误", "秒数必须大于0")
                return
        except:
            messagebox.showerror("错误", "请输入合法数字，例如 1、3、5、0.5")
            return

        # 重置进度条
        self.progress_bar["value"] = 0
        self.start_btn.config(state="disabled", text="提取中...")
        self.status_label.config(text="正在处理视频，请稍等...")
        self.root.update()

        # 开始抽帧并传进度条进去
        success, msg = extract_frame_by_second(
            self.video_path,
            self.save_folder,
            sec,
            self.progress_bar,
            self.root
        )

        if success:
            messagebox.showinfo("完成", msg)
            os.startfile(self.save_folder)
        else:
            messagebox.showerror("失败", msg)

        self.start_btn.config(state="normal", text="开始提取")
        self.status_label.config(text=msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoFrameExtractApp(root)
    root.mainloop()