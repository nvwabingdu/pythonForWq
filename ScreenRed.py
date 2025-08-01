import mss
import time
from PIL import Image
import os
from datetime import datetime
import numpy as np

# 获取用户桌面的路径
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# 定义要监控的区域 (left, top, width, height)
monitor_area = {
    "top": 0,  # 距离顶部的高度
    "left": 0,  # 距离左侧的宽度
    "width": 80,  # 区域的宽度
    "height": 200,  # 区域的高度
}

# 初始化之前的图像为None
previous_image = None


def has_red_pixel(image_array):
    """检查图像数组中是否有红色像素"""
    red_pixels = image_array[(image_array[:, :, 0] > 200) & (image_array[:, :, 1] < 100) & (image_array[:, :, 2] < 100)]
    return red_pixels.size > 0


with mss.mss() as sct:
    while True:
        # 捕捉屏幕截图
        img = sct.grab(monitor_area)

        # 将图像转换为PIL格式
        img_pil = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
        img_array = np.array(img_pil)

        # 生成唯一的文件名并保存到桌面
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        img_pil.save(os.path.join(desktop_path, filename))

        print(f"Screenshot saved to desktop as {filename}.")

        # 如果之前的图像存在，进行比较
        if previous_image is not None:
            # 检查是否有红色像素
            if has_red_pixel(img_array):
                print("出现了红色")
                # 在此处添加要执行的操作，例如发送警报或执行其他代码

        # 更新之前的图像
        previous_image = img_array

        # 暂停一段时间
        time.sleep(3)  # 每2秒捕捉一次