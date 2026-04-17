import tkinter as tk
from datetime import datetime
import os

import pandas as pd


COLUMNS = [
    "登记时间",
    "订单号",
    "客户账号",
    "SKU",
    "补发原因",
    "姓名",
    "电话",
    "收货地址",
    "补发型号",
    "数量",
    "登记人",
]

REQUIRED_ORDER = ["订单号", "客户账号", "SKU", "补发原因", "姓名", "电话", "收货地址", "补发型号"]

DEFAULT_QUANTITY = "x"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("补发表登记工具")
        self.geometry("1200x430")
        self.minsize(980, 360)

        # 置顶：保持在桌面最前面（Windows/macOS 都尽量兼容）
        self.attributes("-topmost", True)

        self._cursor = 0
        self._last_clip = None
        self._is_updating_from_clip = False

        # 左侧按钮区
        left = tk.Frame(self, width=170)
        left.pack(side="left", fill="y")

        btn_generate = tk.Button(left, text="生成", command=self.on_generate)
        btn_generate.pack(pady=18)

        # 右侧表头+输入行
        right = tk.Frame(self)
        right.pack(side="right", fill="both", expand=True, padx=8, pady=6)

        # 紧凑：统一高度
        header_h = 28
        cell_h = 28

        # 表头
        header = tk.Frame(right)
        header.pack(fill="x")

        # 这些宽度决定“单元格长度一致”
        widths = {
            "登记时间": 150,
            "订单号": 120,
            "客户账号": 120,
            "SKU": 100,
            "补发原因": 140,
            "姓名": 80,
            "电话": 110,
            "收货地址": 260,
            "补发型号": 140,
            "数量": 70,
            "登记人": 90,
        }

        self.vars = {}
        self.entries = {}

        # 为了“显示省略但实际文本保持不变”：
        # Tkinter 的 Entry 本身只显示前 N 个字符；但内部 textvariable 保持全量。
        # 我们通过给 Entry 固定宽度，让它自然省略显示（不会截断变量内容）。
        # 这满足你“实际文本保持不变，显示省略一些，上下单元格长度一致”。
        font_name = ("Microsoft YaHei", 10)

        for col in COLUMNS:
            w = widths.get(col, 120)
            lbl = tk.Label(
                header,
                text=col,
                bd=1,
                relief="solid",
                width=max(6, int(w / 10)),
                anchor="center",
                font=font_name,
                height=1,
            )
            lbl.pack(side="left", padx=1, pady=1)

        # 输入行
        inp = tk.Frame(right)
        inp.pack(fill="x", pady=(6, 0))

        # 生成登记时间/数量/登记人输入框
        self.reg_time_var = tk.StringVar(value=self.get_today_cn_date())
        self.qty_var = tk.StringVar(value=DEFAULT_QUANTITY)
        self.user_var = tk.StringVar(value="")

        # 订单号~补发型号：由剪贴板依次填
        for col in COLUMNS:
            w = widths.get(col, 120)
            ent_width = max(6, int(w / 10))

            if col == "登记时间":
                v = self.reg_time_var
                ent = tk.Entry(inp, textvariable=v, bd=1, relief="solid",
                               font=font_name, width=ent_width, justify="center",
                               state="readonly")
            elif col == "数量":
                v = self.qty_var
                ent = tk.Entry(inp, textvariable=v, bd=1, relief="solid",
                               font=font_name, width=ent_width, justify="center",
                               state="readonly")
            elif col == "登记人":
                v = self.user_var
                ent = tk.Entry(inp, textvariable=v, bd=1, relief="solid",
                               font=font_name, width=ent_width, justify="center")
            else:
                v = tk.StringVar(value="")
                ent = tk.Entry(inp, textvariable=v, bd=1, relief="solid",
                               font=font_name, width=ent_width, justify="center")

                self.vars[col] = v

            ent.pack(side="left", padx=1, pady=1, fill="y")

            # readonly 在 Tk 上没法直接禁编辑也能显示；这里就够用
            self.entries[col] = ent

        # 开始轮询剪贴板变化：复制一次就自动填当前列
        self.after(200, self.poll_clipboard)

    def get_today_cn_date(self):
        return datetime.now().strftime("%Y年%m月%d日")

    def set_current_column(self, text):
        # 根据 cursor 填到下一个字段
        if self._cursor >= len(REQUIRED_ORDER):
            # 已经填完，不再填（你可以选择循环，这里先不做）
            return

        col = REQUIRED_ORDER[self._cursor]
        if col in self.vars:
            self.vars[col].set(text)
        self._cursor += 1

    def poll_clipboard(self):
        # 读取剪贴板，如果变化且非空，就写入当前列
        # 注意：复制可能触发多次轮询变化，这里用 last_clip 做去重
        try:
            clip = self.clipboard_get().strip()
        except tk.TclError:
            clip = ""

        if clip and clip != self._last_clip:
            # 防止写入过程中触发二次变化（一般不会，但做个保险）
            self._last_clip = clip
            self.set_current_column(clip)

        self.after(150, self.poll_clipboard)

    def on_generate(self):
        # 校验：至少必填字段（订单号~补发型号）都填了
        missing = []
        for col in REQUIRED_ORDER:
            if not str(self.vars[col].get()).strip():
                missing.append(col)

        if missing:
            # 你说“不需要提示文本”，这里仍需要避免写入错误。
            # 但不弹窗“提示文本”。我用最小化弹窗确认。
            tk.messagebox.showwarning("信息不完整", f"还缺少：{', '.join(missing)}")
            return

        record = {
            "登记时间": self.reg_time_var.get(),
            "订单号": self.vars["订单号"].get().strip(),
            "客户账号": self.vars["客户账号"].get().strip(),
            "SKU": self.vars["SKU"].get().strip(),
            "补发原因": self.vars["补发原因"].get().strip(),
            "姓名": self.vars["姓名"].get().strip(),
            "电话": self.vars["电话"].get().strip(),
            "收货地址": self.vars["收货地址"].get().strip(),
            "补发型号": self.vars["补发型号"].get().strip(),
            "数量": self.qty_var.get().strip(),
            "登记人": self.user_var.get().strip(),
        }

        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        file_name = f"{datetime.now().strftime('%Y-%m-%d')}_登记记录补发表.xlsx"
        file_path = os.path.join(desktop, file_name)

        df_new = pd.DataFrame([record], columns=COLUMNS)

        if not os.path.exists(file_path):
            df_new.to_excel(file_path, index=False)
        else:
            df_old = pd.read_excel(file_path)
            df_all = pd.concat([df_old, df_new], ignore_index=True)
            df_all.to_excel(file_path, index=False)

        # 生成后清空并等待下一条
        self.reset_for_next()

    def reset_for_next(self):
        self._cursor = 0
        self._last_clip = None

        self.reg_time_var.set(self.get_today_cn_date())
        self.qty_var.set(DEFAULT_QUANTITY)
        self.user_var.set("")

        for col in REQUIRED_ORDER:
            self.vars[col].set("")

        # 继续置顶（生成后有时会失焦）
        self.attributes("-topmost", True)


if __name__ == "__main__":
    # Tk messagebox 需要显式导入
    import tkinter.messagebox  # noqa: F401
    app = App()
    app.mainloop()