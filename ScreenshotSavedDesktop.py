import mss
import time
from PIL import Image
import os
from datetime import datetime

# 获取用户桌面的路径
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# 定义要监控的区域 (left, top, width, height)
monitor_area = {
    "top": 41,  # 距离顶部的高度
    "left": 39,  # 距离左侧的宽度
    "width": 397,  # 区域的宽度
    "height": 673,  # 区域的高度
}

with mss.mss() as sct:
    while True:
        # 捕捉屏幕截图
        img = sct.grab(monitor_area)

        # 将图像转换为PIL格式
        img_pil = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")

        # 生成唯一的文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"

        # 保存到桌面
        img_pil.save(os.path.join(desktop_path, filename))

        print(f"Screenshot saved to desktop as {filename}.")

        # 暂停一段时间
        time.sleep(10)  # 每2秒捕捉一次