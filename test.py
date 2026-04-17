import re

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


# 测试
if __name__ == '__main__':
    tests = [
        "张三 13812345678 北京市朝阳区建国路88号",
        "上海市浦东新区张江路123号 李四 13998765432",
    ]

    for t in tests:
        res = extract(t)
        print("原始：", t)
        print("姓名：", res["姓名"])
        print("电话：", res["电话"])
        print("地址：", res["地址"])
        print("-" * 50)