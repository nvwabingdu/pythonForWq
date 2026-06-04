import os
import time
import win32clipboard
import win32con
from PIL import Image
import io
import pyautogui

# -------------------------- 基础配置 --------------------------
ROOT_FOLDER = r"C:\Users\MI\Desktop\京东产品"
IMAGE_EXT = (".jpg", ".jpeg", ".png", ".bmp", ".gif")  # 支持的图片格式
CLICK_POS1 = (595, 755)      # 第一次点击粘贴位置
CLICK_POS2 = (645, 898)      # 第二次点击位置
PASTE_DELAY = 0.3            # 操作间隔（秒）
pyautogui.FAILSAFE = True    # 鼠标移到左上角可强制终止

# -------------------------- CF_DIB 标准剪贴板（核心） --------------------------
def copy_image_to_clipboard_cf_dib(image_path):
    """
    严格按照 CF_DIB 标准格式复制图片到剪贴板
    无临时文件，纯内存，适配所有Windows程序粘贴
    """
    img = Image.open(image_path).convert("RGB")
    output = io.BytesIO()
    img.save(output, format="BMP")
    data = output.getvalue()[14:]  # BMP文件头跳过14字节 = CF_DIB标准

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_DIB, data)
    win32clipboard.CloseClipboard()

# -------------------------- 鼠标/键盘自动化 --------------------------
def mouse_click(x, y):
    pyautogui.moveTo(x, y, duration=0.1)
    pyautogui.click()
    time.sleep(PASTE_DELAY)

def mouse_double_click(x, y):
    pyautogui.moveTo(x, y, duration=0.1)
    pyautogui.doubleClick()
    time.sleep(PASTE_DELAY)

def mouse_right_click(x, y):
    pyautogui.moveTo(x, y, duration=0.1)
    pyautogui.rightClick()
    time.sleep(PASTE_DELAY)

def paste():
    pyautogui.hotkey("ctrl", "v")
    time.sleep(PASTE_DELAY)

def select_all():
    pyautogui.hotkey("ctrl", "a")
    time.sleep(PASTE_DELAY)

def copy():
    pyautogui.hotkey("ctrl", "c")
    time.sleep(PASTE_DELAY)

def press_esc():
    pyautogui.press("esc")
    time.sleep(PASTE_DELAY)

def press_backspace():
    pyautogui.press("backspace")
    time.sleep(PASTE_DELAY)

# -------------------------- 读取剪贴板文本 --------------------------
def get_clipboard_text():
    win32clipboard.OpenClipboard()
    try:
        text = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
    except:
        text = ""
    win32clipboard.CloseClipboard()
    return text

# -------------------------- 写入TXT（追加/自动创建） --------------------------
def write_to_folder_txt(folder_path, content):
    folder_name = os.path.basename(folder_path)
    txt_path = os.path.join(folder_path, f"{folder_name}.txt")
    with open(txt_path, "a", encoding="utf-8") as f:
        f.write(content + "\n" + "-" * 50 + "\n")
    print(f"✅ 已写入：{txt_path}")

# -------------------------- 遍历所有子文件夹 + 第一张图 --------------------------
def process_all_subfolders():
    if not os.path.exists(ROOT_FOLDER):
        print(f"❌ 根目录不存在：{ROOT_FOLDER}")
        return

    for root, dirs, files in os.walk(ROOT_FOLDER):
        # 只处理子文件夹，不处理根目录
        if root == ROOT_FOLDER:
            continue

        print(f"\n======== 正在处理文件夹：{root} ========")
        images = [f for f in files if f.lower().endswith(IMAGE_EXT)]
        if not images:
            print("⚠️  无图片，跳过")
            continue

        # 循环处理每一张图片
        for img in images:
            img_path = os.path.join(root, img)
            print(f"\n🖼️  当前图片：{img}")

            # 1. CF_DIB 复制图片到剪贴板
            try:
                copy_image_to_clipboard_cf_dib(img_path)
            except Exception as e:
                print(f"❌ 图片复制失败：{e}")
                continue

            # 2. 鼠标点击 → 粘贴 → 双击 → 右键
            x1, y1 = CLICK_POS1
            mouse_click(x1, y1)
            paste()
            mouse_double_click(x1, y1)
            time.sleep(2)
            mouse_right_click(x1, y1)
            time.sleep(0.5)

            # 3. 滑动到第二个位置点击
            x2, y2 = CLICK_POS2
            mouse_click(x2, y2)
            time.sleep(0.8)

            # 4. 全选 → 复制 → 获取文本
            select_all()
            copy()
            text = get_clipboard_text().strip()
            if not text:
                text = "未获取到文本"

            # 5. 写入当前子文件夹的同名TXT（追加）
            write_to_folder_txt(root, text)

            # 6. ESC关闭窗口 → 退格删除图片
            press_esc()
            press_backspace()

            print(f"✅ 完成：{img}")
            time.sleep(0.5)

    print("\n🎉 所有文件夹、所有图片全部处理完成！")

# -------------------------- 启动 --------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("京东产品图片自动化粘贴工具（CF_DIB纯剪贴板版）")
    print("⚠️  运行期间不要操作鼠标键盘！")
    print("⚠️  强制终止：鼠标移到屏幕左上角")
    print("=" * 60)
    time.sleep(3)  # 3秒切换到目标窗口
    process_all_subfolders()