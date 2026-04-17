# 固定删除等差数列
# # 读取你的字幕文件
# with open("字幕.txt", "r", encoding="utf-8") as f:
#     lines = f.readlines()
#
# # 保留：不是 4、9、14、19……行
# new_lines = []
# for idx, line in enumerate(lines, start=1):
#     # 删除规则：行号 %5 ==4 → 4、9、14、19...
#     if idx % 5 != 4:
#         new_lines.append(line)
#
# # 保存到新文件
# with open("字幕_已删除.txt", "w", encoding="utf-8") as f:
#     f.writelines(new_lines)
#
# print("✅ 删除完成！已生成：字幕_已删除.txt")

# 删除日文行字幕  有逻辑bug
# import re
#
# input_file = "字幕.txt"
# output_file = "字幕output.txt"
#
# # 只匹配平假名、片假名，不匹配汉字
# kana_pattern = re.compile(r'[ぁ-んァ-ヶ]')
#
# with open(input_file, "r", encoding="utf-8") as f_in, \
#      open(output_file, "w", encoding="utf-8") as f_out:
#
#     for line in f_in:
#         # 只删除包含假名的行
#         if not kana_pattern.search(line):
#             f_out.write(line)
#
# print("处理完成！只删除含日文假名的行，中文正常保留")



# 删除--> 下面第二行
input_file = "字幕.txt"
output_file = "字幕output.txt"

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

result = []
i = 0
total = len(lines)

while i < total:
    line = lines[i]
    # 判断是否是时间轴行：包含 --> 且格式像时间戳
    if '-->' in line and line.strip()[:2].isdigit():
        # 先保留这行时间轴
        result.append(line)
        i += 1

        # 下面第1行保留
        if i < total:
            result.append(lines[i])
            i += 1

        # 下面第2行直接跳过（删除）
        i += 1
    else:
        # 普通行正常保留
        result.append(line)
        i += 1

with open(output_file, 'w', encoding='utf-8') as f:
    f.writelines(result)

print("处理完成：已删除所有时间轴行下面的第2行")