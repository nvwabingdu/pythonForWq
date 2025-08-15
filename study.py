#1.变量赋值的时候就声明了
x = 5
y = "Hello, World!"

#2.用缩进表示语法
if x > 2:
 print("Five is greater than two!")
else:
 print("s")

#3. # 或者三个引号表示多重注释
"""
This is a comment
written in 
more than just one line
"""

# 4.变量不需要使用任何特定类型声明，甚至可以在设置后更改其类型。字符串变量可以使用单引号或双引号进行声明：
x = "Bill"
# is the same as
x = 'Bill'

#5.变量名规则
"""
变量可以使用短名称（如 x 和 y）或更具描述性的名称（age、carname、total_volume）。

Python 变量命名规则：
变量名必须以字母或下划线字符开头
变量名称不能以数字开头
变量名只能包含字母数字字符和下划线（A-z、0-9 和 _）
变量名称区分大小写（age、Age 和 AGE 是三个不同的变量）
请记住，变量名称区分大小写
"""

# 6.赋值方式
x, y, z = "Orange", "Banana", "Cherry"
x = y = z = "Orange"

x = "Python is "
y = "awesome"
z =  x + y   #可以字符相加  数字相加 但是不能数字和字符
print(z)

# 7.变量范围   要在函数内部更改全局变量的值，请使用 global 关键字引用该变量：如果您用了 global 关键字，则该变量属于全局范围
x = "awesome"

def myfunc():
 x = "fantastic"
 print("Python is " + x)

 global y
 y = 0

myfunc()

print("Python is " + x)

# 8.数据类型
"""
文本类型：	str
数值类型：	int, float, complex
序列类型：	list, tuple, range
映射类型：	dict
集合类型：	set, frozenset
布尔类型：	bool
二进制类型：	bytes, bytearray, memoryview
"""


# 9. 各种类型查看
x = 10
print(type(x)) #您可以使用 type() 函数获取任何对象的数据类型

"""                                    
x = "Hello World"	                              str	
x = 29	                                          int	
x = 29.5	                                      float	  可带e  x = 27e4  y = 15E2 z = -49.8e100
x = 1j	                                          complex(复数)   x = 2+3j  y = 7j  z = -7j	
x = ["apple", "banana", "cherry"]	              list	
x = ("apple", "banana", "cherry")	              tuple	（Python 中，元组是一种不可变的数据类型，类似于列表，但一旦创建就不能修改）
x = range(6)	                                  range	
x = {"name" : "Bill", "age" : 63}	              dict	
x = {"apple", "banana", "cherry"}	              set	
x = frozenset({"apple", "banana", "cherry"})	  frozenset（不可变集合）	
x = True	                                      bool	
x = b"Hello"	                                  bytes	
x = bytearray(5)	                              bytearray	
x = memoryview(bytes(5))	                      memoryview（memoryview 在中文里通常被称为 内存视图，它是一个用于访问其他对象的内存，而无需复制数据的工具。它允许你对支持缓冲区协议的对象（如bytes 、bytearray 、array 等）进行操作，并以“只读”或“可读写”的方式访问其内部数据）	
"""

# 10 random
import random
print(random.randrange(1,10))

# 11 强转
"""
int() - 用整数字面量、浮点字面量构造整数（通过对数进行下舍入），或者用表示完整数字的字符串字面量
float() - 用整数字面量、浮点字面量，或字符串字面量构造浮点数（提供表示浮点数或整数的字符串）
str() - 用各种数据类型构造字符串，包括字符串，整数字面量和浮点字面量
"""

x = int(1)   # x 将是 1
y = int(2.5) # y 将是 2
z = int("3") # z 将是 3

x = float(1)     # x 将是 1.0
y = float(2.5)   # y 将是 2.5
z = float("3")   # z 将是 3.0
w = float("4.6")# w 将是 4.6

x = str("S2") # x 将是 'S2'
y = str(3)    # y 将是 '3'
z = str(4.0)  # z 将是 '4.0'

# 12 字符写法
c = "da"
d = '01234578'
a = """Python """
b = '''python '''
print(a+b+c+d)
print(d[0])         #  0   位置1
print(d[2:5])       #  234 位置2-5
print(d[-5:-2])     #  345 获取从位置 5 到位置 1 的字符，从字符串末尾开始计数：
print(len(d))       #获取长度
print(a.strip())    #strip() 方法删除开头和结尾的空白字符：
print(a.lower())    #大小写
print(a.upper())
print(a.replace("World", "Kitty"))
a = "Hello, World!"
print(a.split(",")) #拆分 returns ['Hello', ' World!']

txt = "China is a great country"
x = "ina" in txt
print(x)     #是否在内  in     不在内 not in


# 13 format 格式化写法
age = 63
txt = "My name is Bill, and I am {}"
print(txt.format(age))

a = 3
b = 567
c = 49.95
aaa = "I want {} pieces of item {} for {} dollars."
print(aaa.format(a, b, c))

a = 3
b = 567
c = 49.95
aaa = "I want to pay {2} dollars for {0} pieces of item {1}."
print(aaa.format(a, b, c))


# 14 字符串常见方法
"""
capitalize()	把首字符转换为大写。
casefold()	把字符串转换为小写。
center()	返回居中的字符串。
count()	返回指定值在字符串中出现的次数。
encode()	返回字符串的编码版本。
endswith()	如果字符串以指定值结尾，则返回 true。
expandtabs()	设置字符串的 tab 尺寸。
find()	在字符串中搜索指定的值并返回它被找到的位置。
format()	格式化字符串中的指定值。
format_map()	格式化字符串中的指定值。
index()	在字符串中搜索指定的值并返回它被找到的位置。
isalnum()	如果字符串中的所有字符都是字母数字，则返回 True。
isalpha()	如果字符串中的所有字符都在字母表中，则返回 True。
isdecimal()	如果字符串中的所有字符都是小数，则返回 True。
isdigit()	如果字符串中的所有字符都是数字，则返回 True。
isidentifier()	如果字符串是标识符，则返回 True。
islower()	如果字符串中的所有字符都是小写，则返回 True。
isnumeric()	如果字符串中的所有字符都是数，则返回 True。
isprintable()	如果字符串中的所有字符都是可打印的，则返回 True。
isspace()	如果字符串中的所有字符都是空白字符，则返回 True。
istitle()	如果字符串遵循标题规则，则返回 True。
isupper()	如果字符串中的所有字符都是大写，则返回 True。
join()	把可迭代对象的元素连接到字符串的末尾。
ljust()	返回字符串的左对齐版本。
lower()	把字符串转换为小写。
lstrip()	返回字符串的左修剪版本。
maketrans()	返回在转换中使用的转换表。
partition()	返回元组，其中的字符串被分为三部分。
replace()	返回字符串，其中指定的值被替换为指定的值。
rfind()	在字符串中搜索指定的值，并返回它被找到的最后位置。
rindex()	在字符串中搜索指定的值，并返回它被找到的最后位置。
rjust()	返回字符串的右对齐版本。
rpartition()	返回元组，其中字符串分为三部分。
rsplit()	在指定的分隔符处拆分字符串，并返回列表。
rstrip()	返回字符串的右边修剪版本。
split()	在指定的分隔符处拆分字符串，并返回列表。
splitlines()	在换行符处拆分字符串并返回列表。
startswith()	如果以指定值开头的字符串，则返回 true。
strip()	返回字符串的剪裁版本。
-----swapcase()	切换大小写，小写成为大写，反之亦然。
title()	把每个单词的首字符转换为大写。
translate()	返回被转换的字符串。
upper()	把字符串转换为大写。
zfill()	在字符串的开头填充指定数量的 0 值。
"""

# 15  bool 布尔类型
"""
如果有某种内容，则几乎所有值都将评估为 True。

除空字符串外，任何字符串均为 True。

除 0 外，任何数字均为 True。

除空列表外，任何列表、元组、集合和字典均为 True。
"""
x = "Hello"
y = 10

print(bool(x))
print(bool(y))

#true
bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])

#flase
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})

# 检测是否是该类型
x = 200
print(isinstance(x, int))

# 16  运算符
'''
+	加	x + y	试一试
-	减	x - y	试一试
*	乘	x * y	试一试
/	除	x / y	试一试
%	取模	x % y	试一试
**	幂	x ** y	试一试
//	地板除（取整除）	x // y	试一试


=	x = 5	x = 5	试一试
+=	x += 3	x = x + 3	试一试
-=	x -= 3	x = x - 3	试一试
*=	x *= 3	x = x * 3	试一试
/=	x /= 3	x = x / 3	试一试
%=	x %= 3	x = x % 3	试一试
//=	x //= 3	x = x // 3	试一试
**=	x **= 3	x = x ** 3	试一试
&=	x &= 3	x = x & 3	试一试
|=	x |= 3	x = x | 3	试一试
^=	x ^= 3	x = x ^ 3	试一试
>>=	x >>= 3	x = x >> 3	试一试
<<=	x <<= 3	x = x << 3	试一试

==	等于	x == y	试一试
!=	不等于	x != y	试一试
>	大于	x > y	试一试
<	小于	x < y	试一试
>=	大于或等于	x >= y	试一试
<=	小于或等于	x <= y	试一试


运算符	描述	实例	试一试
and	如果两个语句都为真，则返回 True。	x > 3 and x < 10	试一试
or	如果其中一个语句为真，则返回 True。	x > 3 or x < 4	试一试
not	反转结果，如果结果为 true，则返回 False	not(x > 3 and x < 10)	试一试

身份运算符用于比较对象，不是比较它们是否相等，但如果它们实际上是同一个对象，则具有相同的内存位置：
is	如果两个变量是同一个对象，则返回 true。	x is y	试一试
is not	如果两个变量不是同一个对象，则返回 true。	x is not y	试一试

位运算
&	AND	如果两个位均为 1，则将每个位设为 1。
|	OR	如果两位中的一位为 1，则将每个位设为 1。
^	XOR	如果两个位中只有一位为 1，则将每个位设为 1。
~	NOT	反转所有位。
<<	Zero fill left shift	通过从右侧推入零来向左移动，推掉最左边的位。
>>	Signed right shift	通过从左侧推入最左边的位的副本向右移动，推掉最右边的位。



'''


# 17 集合（数组）
"""
列表（List）是一种有序和可更改的集合。允许重复的成员。
元组（Tuple）是一种有序且不可更改的集合。允许重复的成员。 不用这个
集合（Set）是一个无序和无索引的集合。没有重复的成员。  因为无序 除非有集合相互比较的方法 否则也不常用 
词典（Dictionary）是一个无序，可变和有索引的集合。没有重复的成员。


"""
thislist = ["0", "1", "2","3", "4", "5", "6"]
print(thislist)
print(thislist[0])
print(thislist[-1])
print(thislist[2:5])
print(thislist[-4:-1])

thislist[1] = "mango"
print(thislist)

thislist = ["apple", "banana", "cherry"]
for x in thislist:
  print(x)

thislist = ["apple", "banana", "cherry"]
if "apple" in thislist:
  print("Yes, 'apple' is in the fruits list")

  print(len(thislist)) #打印长度

thislist.append("orange") #追加

thislist.insert(1, "orange") #修改

thislist.remove("banana") #删除

thislist = ["apple", "banana", "cherry"]
thislist.pop(0) #pop() 方法删除指定的索引（如果未指定索引，则删除最后一项）：
print(thislist)

thislist = ["apple", "banana", "cherry"]
del thislist[0]  #同样是删除
print(thislist)

print(len(thislist)==0)
del thislist   #完全删除
#print(len(thislist)==0)

thislist = ["apple", "banana", "cherry"]
thislist.clear()
print(thislist)   #还有一个空集合

# 复制列表 list2=list1       mylist = thislist.copy()       mylist = list(thislist)

# list3 = list1 + list2

# 追加
list1 = ["a", "b" , "c"]
list2 = [1, 2, 3]

for x in list2:
  list1.append(x)

print(list1)

# 一个个扩展
list1 = ["a", "b" , "c"]
list2 = [1, 2, 3]

list1.extend(list2)
print(list1)

#直接用构造函数
thislist = list(("apple", "banana", "cherry")) # 请注意双括号
print(thislist)

"""
集合操作方法
方法	描述
append()	在列表的末尾添加一个元素
clear()	删除列表中的所有元素
copy()	返回列表的副本
count()	返回具有指定值的元素数量。
extend()	将列表元素（或任何可迭代的元素）添加到当前列表的末尾
index()	返回具有指定值的第一个元素的索引
insert()	在指定位置添加元素
pop()	删除指定位置的元素
remove()	删除具有指定值的项目
reverse()	颠倒列表的顺序
sort()	对列表进行排序


set方法 
add()	向集合添加元素。
clear()	删除集合中的所有元素。
copy()	返回集合的副本。
difference()	返回包含两个或更多集合之间差异的集合。
difference_update()	删除此集合中也包含在另一个指定集合中的项目。
discard()	删除指定项目。
intersection()	返回为两个其他集合的交集的集合。
intersection_update()	删除此集合中不存在于其他指定集合中的项目。
isdisjoint()	返回两个集合是否有交集。
issubset()	返回另一个集合是否包含此集合。
issuperset()	返回此集合是否包含另一个集合。
pop()	从集合中删除一个元素。
remove()	删除指定元素。
symmetric_difference()	返回具有两组集合的对称差集的集合。
symmetric_difference_update()	插入此集合和另一个集合的对称差集。
union()	返回包含集合并集的集合。
update()	用此集合和其他集合的并集来更新集合。


"""

# 字典
thisdict =	{
  "brand": "Porsche",
  "model": "911",
  "year": 1963
}
print(thisdict)

x = thisdict["model"]
x = thisdict.get("model")
thisdict["year"] = 2019

for x in thisdict:
  print(x)

for x in thisdict:
   print(thisdict[x])  #返回值

for x in thisdict.values():  #返回值
  print(x)

for x, y in thisdict.items(): #返回键和值
  print(x, y)

# 嵌套字典
myfamily = {
  "child1" : {
    "name" : "Phoebe Adele",
    "year" : 2002
  },
  "child2" : {
    "name" : "Jennifer Katharine",
    "year" : 1996
  },
  "child3" : {
    "name" : "Rory John",
    "year" : 1999
  }
}

# 使用构造函数创建
thisdict = dict(brand="Porsche", model="911", year=1963)
# 请注意，关键字不是字符串字面量
# 请注意，使用了等号而不是冒号来赋值
print(thisdict)

"""
clear()	删除字典中的所有元素
copy()	返回字典的副本
fromkeys()	返回拥有指定键和值的字典
get()	返回指定键的值
items()	返回包含每个键值对的元组的列表
keys()	返回包含字典键的列表
pop()	删除拥有指定键的元素
popitem()	删除最后插入的键值对
setdefault()	返回指定键的值。如果该键不存在，则插入具有指定值的键。
update()	使用指定的键值对字典进行更新
values()	返回字典中所有值的列表
"""

# 18 判断语句
a = 66
b = 66
if b > a:
  print("b is greater than a")
elif a == b:  #之前不正确的判断
  print("a and b are equal")

if b > a:
   pass # 无意义用pass通过


i = 1
while i < 7:
  print(i)
  if i == 3:
    break
  i += 1


i = 0
while i < 7:
  i += 1
  if i == 3:
    continue   #继续
  print(i)


  i = 1
  while i < 6:
   print(i)
   i += 1
  else:  #不成立时再运行一次
   print("i is no longer less than 6")


for x in range(10):
  print(x)

  for x in range(10):
   print(x)

   for x in range(3, 10):
    print(x)

    for x in range(3, 50, 6):   #第三个值是步长
     print(x)

for x in [1,2,3]:  #这个写法好
 print(x)


 # 设置默认值的方式
 def my_function(country="China"):
     print("I am from " + country)

 my_function("Sweden")
 my_function("India")
 my_function()
 my_function("Brazil")

 # 多参数形势
 def my_function(*kids):
     print("The youngest child is " + kids[2])

 my_function("Phoebe", "Jennifer", "Rory")


#  递归   方法里面调用方法
def tri_recursion(k):
  if(k>0):
    result = k+tri_recursion(k-1)
    print(result)
  else:
    result = 0
  return result

print("\n\nRecursion Example Results")
tri_recursion(6)

# lambda 拉姆达表达式

x = lambda a : a + 10
print(x(5))

x = lambda a, b : a * b
print(x(5, 6))

x = lambda a, b, c : a + b + c
print(x(5, 6, 2))


def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)
mytripler = myfunc(3)

print(mydoubler(11))
print(mytripler(11))



