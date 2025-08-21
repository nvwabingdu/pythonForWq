import pyautogui

# 在坐标处执行复制命令
def paste_at_coordinates(x, y):
    # 获取屏幕的宽度和高度
    screen_width, screen_height = pyautogui.size()
    # 确保坐标在屏幕范围内
    if 0 <= x < screen_width and 0 <= y < screen_height:
        # 移动鼠标到指定坐标
        pyautogui.moveTo(x, y)
        # 点击以激活输入框或目标位置
        pyautogui.click()
        # # 执行粘贴命令
        pyautogui.hotkey('ctrl', 'v')  # Windows/Linux
        # # pyautogui.hotkey('command', 'v')  # macOS
    else:
        print("坐标超出屏幕范围！")
# 示例调用
paste_at_coordinates(586, 514)  # 替换为你想要的位置坐标
