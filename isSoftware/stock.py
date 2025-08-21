import baostock as bs
import pandas as pd
import requests

#### 登陆系统 ####
lg = bs.login()

file_name_=fr"C:\Users\16616\Desktop\stock\stock.xlsx"
current_day = "2025-08-19"

# 显示登陆返回信息
# print('login respond error_code:' + lg.error_code)
# print('login respond  error_msg:' + lg.error_msg)
data_list = []

def get_stock(code,start_date_,end_date_):
    #### 获取沪深A股历史K线数据 ####
    # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
    # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
    # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
    # code sz.002067   sh.000001
    # start_date_   2025-08-14
    # end_date_ 2025-08-15
    rs = bs.query_history_k_data_plus(code,
                                      # "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                      "code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                      start_date=start_date_,
                                      end_date=end_date_,
                                      frequency="d",
                                      adjustflag="3")

    # print('query_history_k_data_plus respond error_code:' + rs.error_code)
    # print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

    #### 打印结果集 ####
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())

# 麦馨数据 用于获取所有股票列表   {'dm': '000001.SZ', 'mc': '平安银行', 'jys': 'SZ'},{'dm': '000001.SZ', 'mc': '平安银行', 'jys': 'SZ'}
url = "http://api.mairuiapi.com/hslt/list/LICENCE-66D8-9F96-0C7F0FBCD073"
response = requests.get(url)
data = response.json()

# 通过获取的列表重复请求数据
for i in range(len(data)):
    code=data[i]["jys"]+"."+data[i]["dm"][:6]  #sh002067
    print("code:"+code.lower())
    get_stock(code.lower(), current_day, current_day)

# 将集合内每个小集合第一个前面插入股票名称
new_data_list = [[data[i]["mc"]] + sublist for i, sublist in enumerate(data_list)]

# 结果转化为 DataFrame
result = pd.DataFrame(new_data_list,columns=[
    "股票名称",      # code
    "证券代码",      # code
    "开盘价",       # open
    "最高价",       # high
    "最低价",       # low
    "收盘价",       # close
    "前收盘价",     # preclose
    "成交量",       # volume
    "成交额",       # amount
    "复权状态",     # adjustflag
    "换手率",       # turn
    "交易状态",     # tradestatus
    "涨跌幅",       # pctChg
    "是否ST股"      # isST
     ])

# 使用 ExcelWriter 写入数据
with pd.ExcelWriter(file_name_, engine='openpyxl', mode='a') as writer:
    result.to_excel(writer, sheet_name=fr"{current_day}", index=False)

#### 登出系统 ####
bs.logout()
