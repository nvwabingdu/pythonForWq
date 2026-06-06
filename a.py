import os
import time
import threading
import win32clipboard
import win32con
from PIL import Image
import io
import pyautogui
import keyboard

# -------------------------- 基础配置 --------------------------
ROOT_FOLDER = r"C:\Users\MI\Desktop\京东产品"
IMAGE_EXT = (".jpg", ".jpeg", ".png", ".bmp", ".gif")
CLICK_POS1 = (595, 755)
CLICK_POS2 = (645, 898)
PASTE_DELAY = 0.3
pyautogui.FAILSAFE = True

# 全局控制
STOP_FLAG = False
CLIPBOARD_LOCK = threading.Lock()


# 空格监听强制停止
def check_space_stop():
    global STOP_FLAG
    while not STOP_FLAG:
        if keyboard.is_pressed('space'):
            STOP_FLAG = True
            print("\n🛑 已按下空格，程序强制中断！")
            break
        time.sleep(0.05)


# -------------------------- 剪贴板 --------------------------
def copy_image_to_clipboard_cf_dib(image_path):
    with CLIPBOARD_LOCK:
        img = Image.open(image_path).convert("RGB")
        output = io.BytesIO()
        img.save(output, format="BMP")
        data = output.getvalue()[14:]

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_DIB, data)
        win32clipboard.CloseClipboard()


# -------------------------- 自动化操作 --------------------------
def mouse_click(x, y):
    if STOP_FLAG: raise SystemExit
    pyautogui.moveTo(x, y, duration=0.1)
    pyautogui.click()
    time.sleep(PASTE_DELAY)


def mouse_double_click(x, y):
    if STOP_FLAG: raise SystemExit
    pyautogui.moveTo(x, y, duration=0.1)
    pyautogui.doubleClick()
    time.sleep(PASTE_DELAY)


def mouse_right_click(x, y):
    if STOP_FLAG: raise SystemExit
    pyautogui.moveTo(x, y, duration=0.1)
    pyautogui.rightClick()
    time.sleep(PASTE_DELAY)


def paste():
    if STOP_FLAG: raise SystemExit
    pyautogui.hotkey("ctrl", "v")
    time.sleep(PASTE_DELAY)


def select_all():
    if STOP_FLAG: raise SystemExit
    pyautogui.hotkey("ctrl", "a")
    time.sleep(PASTE_DELAY)


def copy():
    if STOP_FLAG: raise SystemExit
    pyautogui.hotkey("ctrl", "c")
    time.sleep(PASTE_DELAY)


def press_esc():
    if STOP_FLAG: raise SystemExit
    pyautogui.press("esc")
    time.sleep(PASTE_DELAY)


def press_backspace():
    if STOP_FLAG: raise SystemExit
    pyautogui.press("backspace")
    time.sleep(PASTE_DELAY)


# -------------------------- 读取剪贴板 --------------------------
def get_clipboard_text():
    with CLIPBOARD_LOCK:
        win32clipboard.OpenClipboard()
        try:
            text = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
        except:
            text = ""
        win32clipboard.CloseClipboard()
    return text


# -------------------------- 写入TXT --------------------------
def write_to_folder_txt(folder_path, content):
    folder_name = os.path.basename(folder_path)
    txt_path = os.path.join(folder_path, f"{folder_name}.txt")
    with open(txt_path, "a", encoding="utf-8") as f:
        f.write(content + "\n" + "-" * 50 + "\n")
    print(f"✅ 已写入：{txt_path}")


# -------------------------- 主流程：使用 os.walk 取图（和第一段代码完全一致） --------------------------
def process_all_subfolders():
    global STOP_FLAG

    if not os.path.exists(ROOT_FOLDER):
        print(f"❌ 根目录不存在：{ROOT_FOLDER}")
        return

    # 👇 这就是第一段代码的取图方式
    for root, dirs, files in os.walk(ROOT_FOLDER):
        if STOP_FLAG:
            break

        # 跳过根目录，只处理子文件夹
        if root == ROOT_FOLDER:
            continue

        print(f"\n======== 正在处理文件夹：{root} ========")
        # 筛选图片
        images = [f for f in files if f.lower().endswith(IMAGE_EXT)]

        if not images:
            print("⚠️  无图片，跳过")
            continue

        # 循环处理每一张图片
        for img in images:
            if STOP_FLAG:
                break

            img_path = os.path.join(root, img)
            print(f"\n🖼️  当前图片：{img}")

            try:
                copy_image_to_clipboard_cf_dib(img_path)
            except Exception as e:
                print(f"❌ 图片复制失败：{e}")
                continue

            # 点击粘贴
            x1, y1 = CLICK_POS1
            mouse_click(x1, y1)
            paste()
            mouse_double_click(x1, y1)
            time.sleep(2)
            mouse_right_click(x1, y1)
            time.sleep(0.5)

            # 点击第二个位置
            x2, y2 = CLICK_POS2
            mouse_click(x2, y2)
            time.sleep(0.8)

            # 提取文字
            select_all()
            copy()
            text = get_clipboard_text().strip()
            if not text:
                text = "未获取到文本"

            write_to_folder_txt(root, text)

            # 没文字按两次ESC
            if text == "未获取到文本":
                print("⚠️ 未提取到文字，执行两次ESC")
                press_esc()
                press_esc()
            else:
                press_esc()

            press_backspace()
            print(f"✅ 完成：{img}")
            time.sleep(0.5)

    print("\n🎉 程序已安全结束！")


# -------------------------- 启动 --------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("京东产品图片自动化工具（严格系统顺序版）")
    print("⚠️  强制终止：按【空格键】")
    print("=" * 60)

    # 启动空格监听线程
    stop_thread = threading.Thread(target=check_space_stop, daemon=True)
    stop_thread.start()

    time.sleep(3)
    process_all_subfolders()