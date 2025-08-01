import os
from PIL import Image
import io
import win32clipboard

def copy_image_to_clipboard(image_path):
    # 检查路径是否有效
    if not os.path.isfile(image_path):
        print("文件路径无效")
        return

    # 打开图片
    image = Image.open(image_path)

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

# 示例路径
image_path = r"C:\Users\16616\Desktop\1.png"  # 修改为你的图片路径
copy_image_to_clipboard(image_path)