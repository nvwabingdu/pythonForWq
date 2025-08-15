import os
from datetime import datetime
import requests
import pandas as pd

# url = "http://api.mairuiapi.com/hslt/list/LICENCE-66D8-9F96-0C7F0FBCD073"
url="https://api.mairuiapi.com/hsstock/real/time/002068/LICENCE-66D8-9F96-0C7F0FBCD073"
response = requests.get(url)
data = response.json()

print(data[0])
# {'pe': 19.48, 'ud': -0.12, 'pc': -0.9836, 'zf': 2.377, 'tr': 0.01, 'pb_ratio': 0.54, 'p': 12.08, 'o': 12.23, 'h': 12.23, 'l': 11.94, 'yc': 12.2, 'cje': 2344073500, 'v': 1948503, 'pv': 194850295, 'tv': 7951, 't': '2025-08-15 15:00:00'}


def save_xls(content):
    # 将获取到的数据转换为 DataFrame  这里是list
    content = pd.DataFrame(data)
    # 获取桌面路径
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    folder_path = os.path.join(desktop_path, "文件夹1")
    # 创建文件夹（如果不存在的话）
    os.makedirs(folder_path, exist_ok=True)
    # 当前日期
    current_date = datetime.now().strftime('%Y-%m-%d')
    # 保存为 .xls 文件
    xls_file_path = os.path.join(folder_path, f"{current_date}.xlsx")
    content.to_excel(xls_file_path, index=False)

# save_xls(data)







# # =============================================== 将新数据写入工作薄的新表
# import pandas as pd
#
# # 创建一个示例 DataFrame
# data = {
#     'Column1': [1, 2, 3],
#     'Column2': ['A', 'B', 'C']
# }
# df = pd.DataFrame(data)
#
# # 指定文件名
# file_name = fr"C:\Users\16616\Desktop\stock\212.xlsx"
#
# # 使用 ExcelWriter 写入数据
# with pd.ExcelWriter(file_name, engine='openpyxl', mode='a') as writer:
#     df.to_excel(writer, sheet_name='NewSheet', index=False)
#
# print(f'DataFrame 已成功写入 {file_name} 的 NewSheet 工作表。')
