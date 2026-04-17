import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime
import os
import re

# 解析数据（支持多行地址）
def parse_data(text):
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]

    # 找到原因那一行（包含 =========》）
    reason_idx = None
    for i, line in enumerate(lines):
        if "=========》" in line:
            reason_idx = i
            break

    if reason_idx is None:
        return None, "未找到原因行：=========》"

    # 严格按顺序提取
    data = {
        "日期": datetime.now().strftime("%Y年%m月%d日"),
        "订单号": lines[1],
        # "付款时间": lines[2],

        # "SKU": lines[4],
        # 地址：从第5行 到 原因行的上一行，全部合并
        # "客户姓名": extract("".join(lines[5:reason_idx]))["姓名"],
        # "电话": extract("".join(lines[5:reason_idx]))["电话"],
        # "地址": extract("".join(lines[5:reason_idx]))["地址"],
         "客户姓名": "",
         "电话": extract("".join(lines[5:reason_idx]))["电话"],
         "地址": "".join(lines[5:reason_idx]),
        "商品": lines[3],
        "数量": "",
        "登记人": "",
        # 原因：去掉符号
        # "原因": lines[reason_idx].replace("=========》", "").strip()

    }
    return data, None


# 保存Excel（强制文本格式）
def save_to_excel(data):
    today = datetime.now().strftime("%Y%m%d")
    filename = f"{today}.xlsx"

    df_new = pd.DataFrame([data])
    # df_new['ID'] = df_new['ID'].astype(str)
    df_new['订单号'] = df_new['订单号'].astype(str)
    # df_new['SKU'] = df_new['SKU'].astype(str)

    if os.path.exists(filename):
        # df_old = pd.read_excel(filename, dtype={'ID': str, '订单号': str, 'SKU': str})
        df_old = pd.read_excel(filename, dtype={'订单号': str})
        df_final = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_final = df_new

    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df_final.to_excel(writer, index=False)

    return filename


# GUI功能
def on_paste():
    content = root.clipboard_get()
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, content)


def on_generate():
    content = text_box.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("提示", "请先粘贴数据")
        return

    data, err = parse_data(content)
    if err:
        messagebox.showerror("错误", err)
        return

    fn = save_to_excel(data)
    messagebox.showinfo("成功", f"已保存到：{fn}")
    text_box.delete("1.0", tk.END)

# 提取 文字内的 姓名 电话 地址
def clean(s):
    # 修复后的正则，无警告
    s = re.sub(r'[\s，。,；;：""\'()（）【\]]+', ' ', s)
    return s.strip()

def extract(text):
    text = clean(text)

    # 1. 提取电话
    phone = re.search(r'1[3-9]\d{9}', text)
    phone = phone.group() if phone else ''

    # 2. 去掉电话
    rest = text.replace(phone, '').strip()
    parts = [p for p in rest.split() if p]

    # 3. 识别地址
    address = ''
    name = ''
    addr_keywords = ('省','市','区','县','路','街','号','镇','乡','村','花园','苑','城')

    temp_parts = []
    for p in parts:
        if any(k in p for k in addr_keywords):
            address += p + ' '
        else:
            temp_parts.append(p)
    address = address.strip()

    # 4. 姓名
    name = ''.join(temp_parts).strip()
    if len(name) > 6:
        name = name[:4]

    return {
        "姓名": name,
        "电话": phone,
        "地址": address
    }

# 界面
root = tk.Tk()
root.title("订单转Excel工具")
root.geometry("400x450")

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill=tk.BOTH, expand=True)

text_box = tk.Text(main_frame, height=18, width=85, font=("微软雅黑", 10))
text_box.pack(fill=tk.BOTH, expand=True, pady=5)

btn_frame = ttk.Frame(root, padding=5)
btn_frame.pack(pady=5)

ttk.Button(btn_frame, text="📋 粘贴", command=on_paste, width=12).grid(row=0, column=0, padx=15)
ttk.Button(btn_frame, text="✅ 生成Excel", command=on_generate, width=15).grid(row=0, column=1, padx=15)

root.mainloop()