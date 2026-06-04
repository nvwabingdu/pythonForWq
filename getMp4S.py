import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import imageio.v2 as imageio

# 支持的视频格式
VIDEO_EXTS = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".m4v", ".webm", ".mpeg", ".mpg"}

def is_video_file(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() in VIDEO_EXTS

def save_frame_png(out_file: Path, frame_bgr):
    frame_rgb = frame_bgr[:, :, ::-1]
    imageio.imwrite(str(out_file), frame_rgb)

def extract_frames(video_path: Path, out_dir: Path, interval_seconds: float = 1.0):
    out_dir.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return False, "无法打开视频"

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 25.0
    interval_frames = max(int(round(fps * interval_seconds)), 1)

    ok_read, test_frame = cap.read()
    if not ok_read or test_frame is None:
        cap.release()
        return False, "视频损坏或编码不支持"

    try:
        test_path = out_dir / "test_write.png"
        save_frame_png(test_path, test_frame)
        test_path.unlink(missing_ok=True)
    except:
        cap.release()
        return False, "图片写入失败"

    cap.release()
    cap = cv2.VideoCapture(str(video_path))
    frame_idx = 0
    saved = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame is None:
            frame_idx += 1
            continue

        if frame_idx % interval_frames == 0:
            out_file = out_dir / f"frame_{saved:04d}.png"
            try:
                save_frame_png(out_file, frame)
                saved += 1
            except:
                pass

        frame_idx += 1

    cap.release()
    return True, f"成功提取 {saved} 张"

# GUI界面
class VideoFrameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("视频批量抽帧工具（稳定版）")
        self.root.geometry("550x360")
        self.root.resizable(False, False)

        self.folder_path = ""
        self.interval_val = tk.StringVar(value="1")

        # 标题
        tk.Label(root, text="视频批量抽帧工具", font=("微软雅黑", 16, "bold")).pack(pady=12)

        frame = ttk.Frame(root)
        frame.pack(pady=10, padx=30, fill="x")

        # 选择文件夹
        ttk.Button(frame, text="选择视频文件夹", command=self.select_folder).grid(row=0, column=0, padx=5)
        self.folder_label = ttk.Label(frame, text="未选择文件夹", width=35)
        self.folder_label.grid(row=0, column=1)

        # 抽帧间隔
        ttk.Label(frame, text="抽帧间隔(秒)：").grid(row=1, column=0, padx=5, pady=12)
        ttk.Entry(frame, textvariable=self.interval_val, width=15).grid(row=1, column=1, sticky="w")

        # 进度条
        ttk.Label(root, text="总进度：").pack(pady=(10,0))
        self.total_progress = ttk.Progressbar(root, length=450)
        self.total_progress.pack(pady=(0,10))

        ttk.Label(root, text="当前视频：").pack()
        self.current_label = ttk.Label(root, text="等待开始...")
        self.current_label.pack(pady=2)

        # 按钮
        self.start_btn = ttk.Button(root, text="开始抽帧", command=self.start_process, state="disabled")
        self.start_btn.pack(pady=15)

        # 状态
        self.status_label = ttk.Label(root, text="", foreground="green")
        self.status_label.pack()

    def select_folder(self):
        path = filedialog.askdirectory(title="选择视频文件夹")
        if path:
            self.folder_path = path
            self.folder_label.config(text=Path(path).name)
            self.start_btn.config(state="normal")

    def start_process(self):
        try:
            interval = float(self.interval_val.get())
            if interval <= 0:
                messagebox.showerror("错误", "请输入大于0的数字")
                return
        except:
            messagebox.showerror("错误", "请输入有效数字")
            return

        folder = Path(self.folder_path)
        videos = [p for p in folder.rglob("*") if is_video_file(p)]

        if not videos:
            messagebox.showwarning("提示", "未找到视频文件")
            return

        self.start_btn.config(state="disabled", text="处理中...")
        total = len(videos)
        success = 0

        for i, video in enumerate(videos, 1):
            self.current_label.config(text=video.name)
            self.total_progress["value"] = (i / total) * 100
            self.root.update()

            out_dir = video.parent / video.stem
            ok, msg = extract_frames(video, out_dir, interval)
            if ok:
                success += 1

        self.total_progress["value"] = 100
        self.current_label.config(text="处理完成")
        messagebox.showinfo("完成", f"全部处理完毕！\n成功：{success}/{total}")
        self.start_btn.config(state="normal", text="开始抽帧")
        self.status_label.config(text=f"✅ 全部完成，共成功处理 {success} 个视频")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoFrameGUI(root)
    root.mainloop()