# 元组中只包含一个元素时，需要在元素后面添加逗号，否则括号会被当作运算符使用：

tup1 = (50)
print(type(tup1))
# 不加逗号，类型为整型
tup1 = (50,)
print(type(tup1))
# 加上逗号，类型为元组

# 修改元组
tup1 = (12, 34.56)
tup2 = ('abc', 'xyz')

# 以下修改元组元素操作是非法的。
# tup1[0] = 100

# 创建一个新的元组
tup3 = tup1 + tup2
print(tup3)

# 删除元组

tup = ('Google', 'Runoob', 1997, 2000)

print(tup)
del tup
print("删除后的元组 tup : ")
try:
    print(tup)
except Exception:
    print(Exception)


# 创建一个迭代器
class MyNumbers:
    b = 1

    def __iter__(self):
        self.a = 1
        return self

    def __next__(self):
        x = self.a
        self.a += 1
        return x


myclass = MyNumbers()
print(myclass, "MyNumbers")
myiter = iter(myclass)

print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
