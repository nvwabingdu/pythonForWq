# # 用于测试 打印屏幕坐标构成的图片
# import pyautogui
# import os
#
# # ===================== 你的屏幕坐标（直接用）=====================
# # 格式：(左上x, 左上y, 右下x, 右下y)
# COORD1 = (506, 666, 550, 712)
# COORD2 = (489, 341, 1144, 782)
# # =================================================================
#
# # 自动获取桌面路径
# desktop = os.path.join(os.path.expanduser("~"), "Desktop")
#
# # 工具函数：坐标转截图区域
# def coord_to_region(coord):
#     left, top, right, bottom = coord
#     width = right - left
#     height = bottom - top
#     return (left, top, width, height)
#
# # 截图并保存到桌面
# # 截图1
# region1 = coord_to_region(COORD1)
# pyautogui.screenshot(region=region1).save(os.path.join(desktop, "screen1.png"))
#
# # 截图2
# region2 = coord_to_region(COORD2)
# pyautogui.screenshot(region=region2).save(os.path.join(desktop, "screen2.png"))
#
# print("✅ 截图完成！两张图片已保存到桌面")
#

# ================================================
import pyautogui
# 截你头像区域（只截左上角一小块，看位置对不对）
pyautogui.screenshot(region=(506, 660, 553, 713)).save("test.png")

