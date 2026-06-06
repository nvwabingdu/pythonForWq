import cv2
import numpy as np
import pyautogui
import time
import os
import threading
import keyboard
from pathlib import Path
import tkinter as tk
from tkinter import ttk, font
import pyperclip

# ========== 全局控制开关 ==========
is_running = False
stop_flag = False

# ========== 配置区域坐标 ==========
MONITOR_RED_ROI = (14, 113, 86, 192)    # 红色监控区
CLICK_POS = (586, 1028)                 # 输入框点击坐标
WAIT_AFTER_ALT_W = 1.5

AVATAR_ROI = (510, 347, 548, 771)
DIALOG_ROI = (490, 279, 1140, 770)

def coord_to_region(coord):
    left, top, right, bottom = coord
    width = right - left
    height = bottom - top
    return (left, top, width, height)

AVATAR_REGION = coord_to_region(AVATAR_ROI)
DIALOG_REGION = coord_to_region(DIALOG_ROI)

# ========== 参数 ==========
DOWN_1CM = 38
HOVER_WAIT = 0.7
MIN_AVATAR_AREA = 180
MAX_AVATAR_AREA = 5500
SLIDE_STEP = 6

# ========== 关键词自动回复字典 ==========
reply_dict = {
    "彩虹": "是我",
    "人工": "现在已经是人工了，请问有什么需要咨询的呢？",
    "快递": "是京东发货的呢，暂时没有信息呢",
    "质保": "质保是一年的了"
}

# ========== GUI状态控制 ==========
def update_indicator(color):
    canvas.itemconfig(led_oval, fill=color)

def update_button_text(text):
    start_btn.config(text=text)

def update_status_text(text):
    status_label.config(text=text)

def set_status_running():
    update_indicator("#2ecc71")
    update_button_text("点击暂停")
    update_status_text("✅ 正常运行中……")

def set_status_paused(reason="已暂停"):
    global is_running
    is_running = False
    update_indicator("#e74c3c")
    update_button_text("点击开始")
    update_status_text(f"❌ {reason}")

# ========== 双击空格暂停 ==========
last_space_time = 0
def on_space_press(event):
    global last_space_time, is_running
    if not is_running:
        return
    now = time.time()
    if now - last_space_time <= 0.3:
        set_status_paused("双空格强制暂停")
    last_space_time = now

# ========== 检测区域红色 ==========
def check_red_in_region(region_roi):
    left, top, right, bottom = region_roi
    region = (left, top, right-left, bottom-top)
    screenshot = pyautogui.screenshot(region=region)
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2
    red_pixels = cv2.countNonZero(mask)
    return red_pixels > 20

# ========== 头像定位 ==========
def find_avatar_bottom():
    try:
        screenshot = pyautogui.screenshot(region=AVATAR_REGION)
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        binary = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,15,3)
        kernel = np.ones((2,2), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        avatars = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if MIN_AVATAR_AREA < area < MAX_AVATAR_AREA:
                x,y,w,h = cv2.boundingRect(cnt)
                avatars.append((x+w//2, y+h, x,y,w,h))
        if not avatars:
            return None,None,None
        avatars.sort(key=lambda p:p[1], reverse=True)
        cx,by,x,y,w,h = avatars[0]
        return AVATAR_ROI[0]+cx, AVATAR_ROI[1]+by, (AVATAR_ROI[0]+x, AVATAR_ROI[1]+y, w,h)
    except:
        return None,None,None

# ========== 复制按钮检测 + 关键词自动回复（复制粘贴版） ==========
def check_copy_btn():
    try:
        template = cv2.imread("copy_btn.png")
        if template is None:
            return False
        screen = pyautogui.screenshot(region=DIALOG_REGION)
        img = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.7)
        if len(loc[0])>0:
            px = DIALOG_ROI[0]+loc[1][0]+8
            py = DIALOG_ROI[1]+loc[0][0]+8
            pyautogui.click(px,py)
            pyautogui.hotkey("ctrl","c")
            time.sleep(0.2)
            text = pyperclip.paste().strip()
            if not text:
                set_status_paused("复制内容为空，暂停运行")
                return False

            # 匹配关键词 → 复制粘贴发送（无模拟打字）
            for keyword, reply_txt in reply_dict.items():
                if keyword in text:
                    # 1. 点击输入框
                    pyautogui.moveTo(CLICK_POS[0], CLICK_POS[1], duration=0.15)
                    pyautogui.click()
                    time.sleep(0.2)

                    # 2. 复制回复内容到剪贴板
                    pyperclip.copy(reply_txt)

                    # 3. 粘贴 Ctrl+V
                    pyautogui.hotkey("ctrl", "v")
                    time.sleep(0.2)

                    # 4. 回车发送
                    pyautogui.press("enter")

                    update_status_text(f"✅ 命中【{keyword}】已粘贴发送")
                    return True
            return True
    except Exception as e:
        print("异常:", e)
    return False

def run_once():
    cx,cy,roi = find_avatar_bottom()
    if not cx:
        set_status_paused("未找到头像，暂停运行")
        return False
    pyautogui.moveTo(cx,cy,duration=0.2)
    total = 0
    while total < DOWN_1CM:
        if not is_running:
            return False
        if check_copy_btn():
            return True
        pyautogui.moveRel(0,SLIDE_STEP,duration=0.08)
        total += SLIDE_STEP
        time.sleep(HOVER_WAIT)
    set_status_paused("滑动完毕未找到复制按钮")
    return False

def main_loop():
    global is_running
    while True:
        if not is_running:
            time.sleep(0.1)
            continue
        try:
            if check_red_in_region(MONITOR_RED_ROI):
                pyautogui.moveTo(CLICK_POS[0], CLICK_POS[1], duration=0.2)
                pyautogui.click()
                time.sleep(0.3)
                pyautogui.hotkey("alt","w")
                time.sleep(WAIT_AFTER_ALT_W)
                run_once()
        except Exception as e:
            set_status_paused(f"异常：{str(e)}")
        time.sleep(0.2)

# ========== 启停按钮 ==========
def toggle_start():
    global is_running
    if not is_running:
        is_running = True
        set_status_running()
    else:
        is_running = False
        set_status_paused("手动暂停")

# ========== 置顶小界面 ==========
root = tk.Tk()
root.title("监控工具")
root.geometry("320x130")
root.resizable(False, False)
root.attributes("-topmost", True) # 窗口置顶

# 指示灯
canvas = tk.Canvas(root, width=50, height=50, bg="#f0f0f0", highlightthickness=0)
canvas.place(x=20, y=40)
led_oval = canvas.create_oval(5,5,45,45, fill="#95a5a6", outline="#bdc3c7", width=2)

# 状态文字
status_font = font.Font(size=11, weight="bold")
status_label = tk.Label(root, text="⏸️ 等待启动", font=status_font, fg="#34495e")
status_label.place(x=85, y=50)

# 按钮
btn_font = font.Font(size=10, weight="bold")
start_btn = ttk.Button(root, text="点击开始", command=toggle_start, width=10)
start_btn.place(x=210, y=45)

# 底部提示
tip_label = tk.Label(root, text="按两次空格强制暂停", fg="#7f8c8d")
tip_label.place(x=20, y=100)

keyboard.on_press_key("space", on_space_press)
threading.Thread(target=main_loop, daemon=True).start()

root.mainloop()