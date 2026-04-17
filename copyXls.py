import tkinter as tk
from datetime import datetime
import os

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
        self.title("补发登记")
        self.attributes("-topmost", True)

        self._cursor = 0
        self._last_clip = None  # 保留，但初始不读取

        # 零边距
        right = tk.Frame(self)
        right.pack(fill="both", expand=True, padx=0, pady=0)

        widths = {
            "登记时间": 140,
            "订单号": 110,
            "客户账号": 110,
            "SKU": 90,
            "补发原因": 130,
            "姓名": 75,
            "电话": 105,
            "收货地址": 240,
            "补发型号": 130,
            "数量": 65,
            "登记人": 85,
        }

        self.vars = {}
        font = ("Microsoft YaHei", 9)

        # ========== 表头行 ==========
        header = tk.Frame(right)
        header.pack(fill="x")
        for col in COLUMNS:
            w = widths.get(col, 100)
            lbl = tk.Label(header, text=col, bd=1, relief="solid", font=font,
                           width=max(6, int(w/10)), anchor="center")
            lbl.pack(side="left", padx=1, pady=0)

        # ========== 输入行 ==========
        inp = tk.Frame(right)
        inp.pack(fill="x", pady=0)

        self.reg_time_var = tk.StringVar(value=self.get_today_cn_date())
        self.qty_var = tk.StringVar(value=DEFAULT_QUANTITY)
        self.user_var = tk.StringVar()

        for col in COLUMNS:
            w = widths.get(col, 100)
            if col == "登记时间":
                v = self.reg_time_var
                e = tk.Entry(inp, textvariable=v, font=font, width=max(6, int(w/10)),
                             bd=1, relief="solid", justify="center", state="readonly")
            elif col == "数量":
                v = self.qty_var
                e = tk.Entry(inp, textvariable=v, font=font, width=max(6, int(w/10)),
                             bd=1, relief="solid", justify="center")
            elif col == "登记人":
                v = self.user_var
                e = tk.Entry(inp, textvariable=v, font=font, width=max(6, int(w/10)),
                             bd=1, relief="solid", justify="center")
            else:
                v = tk.StringVar()
                e = tk.Entry(inp, textvariable=v, font=font, width=max(6, int(w/10)),
                             bd=1, relief="solid", justify="center")
                self.vars[col] = v
            e.pack(side="left", padx=1, pady=0)

        # ========== 绿色生成按钮 ==========
        btn_gen = tk.Button(inp, text="生成", command=self.on_generate,
                            font=font, width=6,
                            bg="#28a845", fg="white",
                            bd=1, relief="solid")
        btn_gen.pack(side="left", padx=1, pady=0)
        # 🔥 关键修改：初始不监听
        self.start_listening = False  # 新增
        self.after(200, self.poll_clipboard)

        # ==============================================
        # 🔥 核心：让窗口自动贴合内容大小（自适应）
        # ==============================================
        self.update()
        self.geometry(f"{self.winfo_width()}x{self.winfo_height()}")
        self.resizable(False, False)  # 锁定不可拉伸


    def get_today_cn_date(self):
        return datetime.now().strftime("%Y年%m月%d日")

    def set_current_column(self, text):
        if self._cursor >= len(REQUIRED_ORDER):
            return
        col = REQUIRED_ORDER[self._cursor]
        self.vars[col].set(text)
        self._cursor += 1

    def poll_clipboard(self):
        try:
            clip = self.clipboard_get().strip()
        except tk.TclError:
            clip = ""

        # 🔥 关键修改：第一次不自动填充
        if clip and clip != self._last_clip:
            if not self.start_listening:
                self.start_listening = True
                self._last_clip = clip
            else:
                self._last_clip = clip
                self.set_current_column(clip)

        self.after(150, self.poll_clipboard)

    def on_generate(self):
        import pandas as pd
        import tkinter.messagebox

        missing = [c for c in REQUIRED_ORDER if not self.vars[c].get().strip()]
        if missing:
            tkinter.messagebox.showwarning("提示", f"缺少：{', '.join(missing)}")
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
        file = os.path.join(desktop, f"{datetime.now():%Y-%m-%d}_补发登记.xlsx")

        df_new = pd.DataFrame([record], columns=COLUMNS)
        if os.path.exists(file):
            df_old = pd.read_excel(file)
            df_new = pd.concat([df_old, df_new], ignore_index=True)
        df_new.to_excel(file, index=False)

        # 重置
        self._cursor = 0
        self._last_clip = None
        self.start_listening = False  # 重置后再次忽略第一次
        self.user_var.set("")
        for c in REQUIRED_ORDER:
            self.vars[c].set("")

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
