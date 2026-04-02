#!/usr/bin/env python3
"""
最终版：Windows 屏幕 + 音频 录制（中文界面，自动选择系统声音或麦克风）
说明：
 - 依赖：pip install mss pillow imageio-ffmpeg
 - 运行：python screen_recorder_auto_audio_cn.py
 - 输出：output_with_audio.mp4（保存在脚本运行目录）
"""

import subprocess
import shlex
import threading
import time
import os
import re
from tkinter import Tk, Canvas, Toplevel, Label, Button, Entry, messagebox
from mss import mss

# 尝试使用 imageio-ffmpeg 提供的 ffmpeg 二进制，否则使用系统 ffmpeg（需在 PATH）
FFMPEG_EXE = None
try:
    import imageio_ffmpeg as _iioff
    FFMPEG_EXE = _iioff.get_ffmpeg_exe()
except Exception:
    FFMPEG_EXE = "ffmpeg"

def ffmpeg_available(ffmpeg_exe=FFMPEG_EXE):
    try:
        proc = subprocess.Popen([ffmpeg_exe, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.communicate(timeout=3)
        # returncode may be 0 normally
        return proc.returncode == 0 or proc.returncode is None
    except Exception:
        return False

def list_dshow_devices(ffmpeg_exe=FFMPEG_EXE, timeout=5.0):
    """
    列出 DirectShow 设备（Windows）。返回 (video_devices, audio_devices)。
    若 ffmpeg 不可用会抛出 FileNotFoundError。
    """
    video_devices, audio_devices = [], []
    if not ffmpeg_available(ffmpeg_exe):
        raise FileNotFoundError(f"ffmpeg 未找到: {ffmpeg_exe}")
    try:
        cmd = [ffmpeg_exe, "-list_devices", "true", "-f", "dshow", "-i", "dummy"]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            outs, errs = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()
        text = (errs or b"").decode("utf-8", errors="ignore") + (outs or b"").decode("utf-8", errors="ignore")
        # 尝试解析双引号里的设备名并根据上下文判断是 audio 还是 video
        lines = text.splitlines()
        for i, line in enumerate(lines):
            q = re.findall(r'\"([^\"]+)\"', line)
            if not q:
                continue
            name = q[0]
            low = line.lower()
            if "audio" in low:
                audio_devices.append(name)
            elif "video" in low:
                video_devices.append(name)
            else:
                lname = name.lower()
                if any(k in lname for k in ("microphone", "mic", "stereo", "stereo mix", "立体声", "麦克风")):
                    audio_devices.append(name)
                else:
                    # fallback: put into video list (safer default)
                    video_devices.append(name)
        # 去重并返回
        def uniq(seq):
            seen = set(); res=[]
            for s in seq:
                if s not in seen:
                    seen.add(s); res.append(s)
            return res
        return uniq(video_devices), uniq(audio_devices)
    except Exception as e:
        raise

def choose_audio_device_auto():
    """
    自动选择音频设备：
     - 优先 Stereo Mix / 立体声（系统声音）
     - 否则选择第一个麦克风设备
     - 返回 (device_name or None, description)
    """
    try:
        _, audio_devices = list_dshow_devices()
    except FileNotFoundError:
        return None, "未找到 ffmpeg（将仅录制视频）"
    except Exception:
        return None, "列举设备失败（将仅录制视频）"
    if not audio_devices:
        return None, "未检测到音频设备（仅录视频）"
    lowered = [d.lower() for d in audio_devices]
    for idx, name in enumerate(lowered):
        if "stereo" in name or "立体声" in name or "stereo mix" in name or "立体声混音" in name:
            return audio_devices[idx], "自动选择：系统声音（Stereo Mix）"
    for idx, name in enumerate(lowered):
        if "microphone" in name or "mic" in name or "麦克风" in name or "micro" in name:
            return audio_devices[idx], "自动选择：麦克风（Microphone）"
    # fallback
    return audio_devices[0], "自动选择：第一个音频设备"

def build_ffmpeg_command(ffmpeg_exe, region, audio_device, fps=15, out_file="output_with_audio.mp4"):
    left, top, width, height = region
    video_input = f'-f gdigrab -framerate {fps} -offset_x {left} -offset_y {top} -video_size {width}x{height} -i desktop'
    if audio_device:
        audio_escaped = audio_device.replace('"', '\\"')
        audio_input = f'-f dshow -i audio="{audio_escaped}"'
        cmd = f'{ffmpeg_exe} {video_input} {audio_input} -c:v libx264 -preset veryfast -crf 23 -r {fps} -pix_fmt yuv420p -y "{out_file}"'
    else:
        cmd = f'{ffmpeg_exe} {video_input} -c:v libx264 -preset veryfast -crf 23 -r {fps} -pix_fmt yuv420p -y "{out_file}"'
    return cmd

def select_region_with_tk():
    """
    弹出全屏半透明窗口，支持鼠标拖动选择区域；返回 (left, top, width, height) 或 None。
    """
    root = Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.25)
    root.title("请拖动选择录制区域，按 Esc 取消")
    canvas = Canvas(root, cursor="cross", bg="black")
    canvas.pack(fill="both", expand=True)

    start_x = start_y = cur_rect = None
    region = {"left": 0, "top": 0, "width": 0, "height": 0}
    cancelled = {"v": False}

    def on_button_press(event):
        nonlocal start_x, start_y, cur_rect
        start_x, start_y = event.x, event.y
        cur_rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="red", width=2)

    def on_move(event):
        nonlocal cur_rect
        if cur_rect:
            canvas.coords(cur_rect, start_x, start_y, event.x, event.y)

    def _finish_selection():
        try:
            if root.winfo_exists():
                root.destroy()
        except Exception:
            pass

    def on_button_release(event):
        nonlocal region
        if start_x is None:
            return
        x1, y1 = start_x, start_y
        x2, y2 = event.x, event.y
        left = min(x1, x2)
        top = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        region.update({"left": left, "top": top, "width": width, "height": height})
        root.after(100, _finish_selection)

    def on_escape(event=None):
        cancelled["v"] = True
        try:
            if root.winfo_exists():
                root.destroy()
        except Exception:
            pass

    root.bind("<Escape>", on_escape)
    canvas.bind("<ButtonPress-1>", on_button_press)
    canvas.bind("<B1-Motion>", on_move)
    canvas.bind("<ButtonRelease-1>", on_button_release)

    instr = Toplevel(root)
    instr.overrideredirect(True)
    instr.attributes("-topmost", True)
    l = Label(instr, text="拖动选择录制区域，按 Esc 取消。", bg="yellow", fg="black")
    l.pack()
    instr.update_idletasks()
    instr.geometry("+10+10")

    try:
        root.mainloop()
    except Exception:
        pass

    try:
        if instr.winfo_exists():
            instr.destroy()
    except Exception:
        pass

    if cancelled["v"]:
        return None
    if region["width"] < 5 or region["height"] < 5:
        return None
    return (int(region["left"]), int(region["top"]), int(region["width"]), int(region["height"]))

class RecorderApp:
    def __init__(self):
        self.region = None
        self.proc = None
        self.running = False
        self.fps = 15
        self.out_file = "output_with_audio.mp4"
        self.audio_device = None
        self.audio_reason = ""

    def start(self):
        sel = select_region_with_tk()
        if not sel:
            print("已取消选择。")
            return
        self.region = sel
        dev, reason = choose_audio_device_auto()
        self.audio_device = dev
        self.audio_reason = reason
        self.show_control_window()

    def show_control_window(self):
        self.win = Tk()
        self.win.title("屏幕录制（控制面板）")
        self.win.geometry("540x280")
        self.win.resizable(False, False)

        Label(self.win, text=f"已选区域：{self.region[2]} x {self.region[3]}，位置 ({self.region[0]},{self.region[1]})").pack(pady=6)
        Label(self.win, text=f"音频检测：{self.audio_reason} {self.audio_device or ''}").pack()
        Label(self.win, text="目标帧率（建议 10-30）：").pack()
        fps_entry = Entry(self.win)
        fps_entry.insert(0, str(self.fps))
        fps_entry.pack()

        Label(self.win, text="（通常无需修改设备名，若想自定义可在此输入）").pack(pady=(6, 0))
        # 始终创建并赋值给实例属性，避免 AttributeError
        self.audio_entry = Entry(self.win, width=70)
        if self.audio_device:
            self.audio_entry.insert(0, self.audio_device)
        self.audio_entry.pack()

        start_btn = Button(self.win, text="开始录制", width=20, command=lambda: self.start_recording(fps_entry.get()))
        start_btn.pack(pady=(12, 6))
        stop_btn = Button(self.win, text="停止并保存", width=20, command=self.stop_recording)
        stop_btn.pack()

        def on_close():
            if self.running:
                if messagebox.askyesno("提示", "当前正在录制，是否停止并退出？"):
                    self.stop_recording()
                else:
                    return
            try:
                if self.win.winfo_exists():
                    self.win.destroy()
            except Exception:
                pass

        self.win.protocol("WM_DELETE_WINDOW", on_close)
        self.win.mainloop()

    def start_recording(self, fps_value):
        if self.running:
            return
        try:
            fps = int(fps_value)
            if fps <= 0 or fps > 60:
                raise ValueError
            self.fps = fps
        except Exception:
            messagebox.showerror("错误", "请输入有效的帧率整数（1-60）。")
            return

        # 检查 ffmpeg 是否可用
        if not ffmpeg_available(FFMPEG_EXE):
            # 提示并询问是否仅录视频
            if not messagebox.askyesno("未找到 ffmpeg", "未检测到 ffmpeg 可执行程序（或 imageio-ffmpeg 未安装）。\n安装 imageio-ffmpeg 或系统 ffmpeg 后可录音。\n是否仅录视频（不含音频）？"):
                return
            audio_dev = None
        else:
            # 若用户在文本框改了设备名，以文本框为准；否则使用自动检测到的设备（可能为 None）
            audio_dev_text = ""
            if hasattr(self, "audio_entry") and self.audio_entry is not None:
                audio_dev_text = self.audio_entry.get().strip()
            audio_dev = audio_dev_text if audio_dev_text else self.audio_device

        cmd = build_ffmpeg_command(FFMPEG_EXE, self.region, audio_dev if audio_dev else None, fps=self.fps, out_file=self.out_file)
        print("执行 ffmpeg 命令：")
        print(cmd)
        try:
            # 在 Windows 上使用 shell=True 让命令字符串按预期解析
            if os.name == "nt":
                self.proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                parts = shlex.split(cmd)
                self.proc = subprocess.Popen(parts, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            messagebox.showerror("错误", f"启动 ffmpeg 失败：{e}")
            return

        self.running = True
        threading.Thread(target=self._read_ffmpeg_stderr, daemon=True).start()
        messagebox.showinfo("开始", f"录制已开始，文件：{self.out_file}")

    def _read_ffmpeg_stderr(self):
        if not self.proc:
            return
        try:
            for line in self.proc.stderr:
                try:
                    decoded = line.decode("utf-8", errors="ignore").rstrip()
                    print(decoded)
                except Exception:
                    pass
        except Exception:
            pass

    def stop_recording(self):
        if not self.running or not self.proc:
            messagebox.showinfo("提示", "当前未在录制。")
            return
        try:
            # 尝试优雅停止：向 ffmpeg stdin 发送 'q'
            if self.proc.stdin:
                try:
                    self.proc.stdin.write(b"q")
                    self.proc.stdin.flush()
                except Exception:
                    pass
            # 等待进程退出
            timeout = 5.0
            t0 = time.time()
            while time.time() - t0 < timeout:
                if self.proc.poll() is not None:
                    break
                time.sleep(0.1)
            if self.proc.poll() is None:
                # 仍在运行，尝试 terminate -> kill
                self.proc.terminate()
                time.sleep(0.5)
                if self.proc.poll() is None:
                    self.proc.kill()
        except Exception as e:
            print("停止 ffmpeg 时出错：", e)
        finally:
            self.running = False
            messagebox.showinfo("完成", f"录制已停止，文件已保存为：{self.out_file}")

if __name__ == "__main__":
    app = RecorderApp()
    app.start()