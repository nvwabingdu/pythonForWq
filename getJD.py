import os
import time
import pyperclip
import pyautogui
import tkinter as tk
from pathlib import Path

# =====================【自行配置参数区】=====================
# SKU集合，逗号分隔自定义
SKU_SET = {
    "100347940234",
    "100347872254",
    "100261415515",
    "100326493286",
    "100244678325",
    "100244764593",
    "100113479424",
    "100348199986",
    "100326629284",
    "100348225916"
}
# SKU_SET = {"100049080427", "100200224975"}
# 浏览器地址栏点击坐标
ADDR_X, ADDR_Y = 454, 87
# 商品详情点击坐标
DETAIL_X, DETAIL_Y = 328, 1056

# 【主截图区域】：商品大图区域（不变）
CAP_LEFT = 148
CAP_TOP = 186
CAP_RIGHT = 1138
CAP_BOTTOM = 1124

# 【判定区域】：你指定的小区域 (x1, y1, x2, y2)
CHECK_X1 = 291
CHECK_Y1 = 146
CHECK_X2 = 372
CHECK_Y2 = 177

# 单次滚轮下滑数值(负数向下) → 一屏高度
SCROLL_DOWN = -750
# 页面加载等待秒数
WAIT_LOAD = 6
# 滑动后等待静止时间
WAIT_AFTER_SCROLL = 1
# ==========================================================

DESKTOP = str(Path.home() / "Desktop")

class SkuTool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("京东SKU自动截图｜每页保存一张")
        self.geometry("560x320")
        self.resizable(False, False)

        tk.Label(self, text=f"待处理SKU总数：{len(SKU_SET)}", font=("微软雅黑",12)).pack(pady=4)
        tk.Label(self, text=str(SKU_SET), font=("微软雅黑",9), wraplength=530).pack(pady=4)

        tk.Button(self, text="开始批量处理", command=self.start_task, width=18, height=2).pack(pady=8)

        self.log_box = tk.Text(self, width=65, height=9, font=("微软雅黑",9))
        self.log_box.pack(pady=3)

    def log(self, msg):
        self.log_box.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.log_box.see("end")
        self.update()

    def start_task(self):
        for sku in SKU_SET:
            self.log(f"\n======== 当前SKU：{sku} ========")
            self.process_single(sku)
        self.log("✅ 全部SKU处理完毕！")

    def process_single(self, sku):
        # 1.SKU写入剪贴板
        pyperclip.copy(sku)
        time.sleep(0.3)

        # 2.选中地址栏、替换链接并回车
        pyautogui.click(ADDR_X, ADDR_Y)
        time.sleep(0.5)
        pyautogui.hotkey("ctrl", "a")
        url = f"https://item.jd.com/{sku}.html"
        pyperclip.copy(url)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.press("enter")
        self.log(f"跳转网页：{url}")

        # 等待页面加载
        time.sleep(WAIT_LOAD)

        # 3.点击商品详情
        pyautogui.click(DETAIL_X, DETAIL_Y)
        self.log("点击商品详情标签，等待页面刷新")
        time.sleep(1.2)

        # 4.循环滚动+单张保存截图，触底停止
        self.scroll_capture_save(sku)

    def scroll_capture_save(self, sku):
        # 创建保存目录
        save_folder = os.path.join(DESKTOP, "京东产品", sku)
        os.makedirs(save_folder, exist_ok=True)

        # 主截图区域
        main_width = CAP_RIGHT - CAP_LEFT
        main_height = CAP_BOTTOM - CAP_TOP
        main_region = (CAP_LEFT, CAP_TOP, main_width, main_height)

        # 判定小区域
        check_width = CHECK_X2 - CHECK_X1
        check_height = CHECK_Y2 - CHECK_Y1
        check_region = (CHECK_X1, CHECK_Y1, check_width, check_height)

        # 先截第一张判定图
        last_check_img = pyautogui.screenshot(region=check_region)
        pic_index = 1

        self.log("开始逐屏截图，每张独立保存...")
        while True:
            # 截取并保存主图
            cur_main = pyautogui.screenshot(region=main_region)
            img_path = os.path.join(save_folder, f"{sku}_{pic_index}.png")
            cur_main.save(img_path)
            self.log(f"已保存：第{pic_index}屏")
            pic_index += 1

            # 下滑
            pyautogui.scroll(SCROLL_DOWN)
            time.sleep(WAIT_AFTER_SCROLL)

            # 截取新的判定图
            new_check_img = pyautogui.screenshot(region=check_region)

            # 对比：不一致 = 到底了，停止
            if new_check_img.tobytes() != last_check_img.tobytes():
                self.log("判定区域画面已变化 → 已滑到底部，停止截图")
                break

            # 更新上一张判定图
            last_check_img = new_check_img

        self.log(f"✅ 当前SKU截图完成，共保存 {pic_index-1} 张")

if __name__ == "__main__":
    app = SkuTool()
    app.mainloop()