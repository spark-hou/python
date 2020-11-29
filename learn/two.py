import copy

# 运算符
# Python位运算符
#  按位运算符是把数字看作二进制来进行计算的。Python中的按位运算法则如下：
a = 60  # 60 = 0011 1100
b = 13  # 13 = 0000 1101
c = 0

c = a & b  # 12 = 0000 1100
print("1 - c 的值为：", c)
c = a | b  # 61 = 0011 1101
print("2 - c 的值为：", c)

# Python逻辑运算符
a = 10
b = 20


def comparison(a, b):
    if (a and b):
        print("1 - 变量 a 和 b 都为 true")
    else:
        print("1 - 变量 a 和 b 有一个不为 true")

    if (a or b):
        print("2 - 变量 a 和 b 都为 true，或其中一个变量为 true")
    else:
        print("2 - 变量 a 和 b 都不为 true")


comparison(a, b)

a = 0
comparison(a, b)

# Python成员运算符

a = 10
b = 20
arr = [1, 2, 3, 20, 5]

if (a in arr):
    print("1 - 变量 a 在给定的列表中 list 中")
else:
    print("1 - 变量 a 不在给定的列表中 list 中")

if (b not in arr):
    print("2 - 变量 b 不在给定的列表中 list 中")
else:
    print("2 - 变量 b 在给定的列表中 list 中")

# Python身份运算符
a = 20
b = 20

if (a is b):
    print("1 - a 和 b 有相同的标识")
else:
    print("1 - a 和 b 没有相同的标识")

if (id(a) == id(b)):
    print("2 - a 和 b 有相同的标识")
else:
    print("2 - a 和 b 没有相同的标识")

# 修改变量 b 的值
b = 30
if (a is b):
    print("3 - a 和 b 有相同的标识")
else:
    print("3 - a 和 b 没有相同的标识")

if (a is not b):
    print("4 - a 和 b 没有相同的标识")
else:
    print("4 - a 和 b 有相同的标识")

# is 与 == 区别：
# is 用于判断两个变量引用对象是否为同一个， == 用于判断引用变量的值是否相等。
a = [1, 2, 3]
b = a
print(b == a)
print(b is a)
# b = a[:]
b = copy.deepcopy(a)
print(b == a, b)
print(b is a)
