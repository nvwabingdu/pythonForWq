from chard import chard

# 测试各种乱七八糟的地址文本
test_data = [
    "张三 13812345678 北京市朝阳区建国路88号",
    "上海市浦东新区张江路123号 李四 13998765432",
    " 王五：13700001111，广东省深圳市南山区科技园 ",
    "收货人 赵六 13611112222 浙江省杭州市西湖区100号",
]

# 自动解析
for text in test_data:
    result = chard.parse(text)

    print("原始文本：", text)
    print("姓名：", result.get("name"))
    print("电话：", result.get("phone"))
    print("地址：", result.get("address"))
    print("-" * 40)