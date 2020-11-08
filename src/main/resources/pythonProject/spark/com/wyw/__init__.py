from typing import List , Union

print(divmod(10 , 3))
count = 1

# for i in range(1, 5, 1):
#     for j in range(1, i, 1):
#         print('*', end='')
#     print()

for i in range(1 , 5 , 1):
    print(i * '*')


class MyNumber:
    def __iter__(self):
        self.a = 1
        return self

    def __next__(self):
        x = self.a
        self.a += 2
        return x


md = MyNumber()
myIter = iter(md)
print(next(myIter))
print(next(myIter))
print(next(myIter))
print(next(myIter))


def fibonacci():
    a , b = 0 , 1
    for i in range(1 , 11):
        # 每次保存当前a的所有值最后返回一个迭代器来遍历所有保存过的yield
        yield a
        print(a)
        # 用的是yield 摔回的a
        a , b = b , a + b


my = fibonacci()
# 拿到my迭代器，迭代所有保存过的a
for j in range(0 , 6):
    print(next(my))

list = ["1" , "2" , "3"]
del list[2]
list.append(1)
list += [2]
list += "63"
print(len(list))
print(list)

name = (i for i in range(1 , 10))
name1 = [i for i in range(1 , 10)]
print("hell".capitalize())
for j in name:
    print(j)

speak = "7"
mydist = {"1": 11 , "2": 33 , "3": 45}
for k in mydist:
    print(k)
for k in mydist.values():
    print(k)
for k in mydist.items():
    print(k)
# 空值 一切非0的值均为true
if 0:
    print("fffss")
if 1:
    print("fff")


def abce(e):
    return e + 2


r = map(abce , [1 , 2 , 4 , 5])
# print(list)

with open('e://ab.txt' , 'a+') as f:
    f.write("helllo")


def abc():
    return 123


kkk = abc
print(kkk())


def abc2(num):
    return num * 2


# print(list(map(abc2 , [1 , 2 , 3 , 4 , 5])))


# * 是元组
def func1(y , *x):
    value = x + y ** 2
    if value > 5:
        return value


# ** 是字典
# def func2(y , **x):
#     value = x + y ** 2
#     if value > 5:
#         return value


# func2(1 , a=1 , b=2)


# 装饰器
def myanno(user_func):
    # 传函数的参数
    def wrap(*args):
        print("烧饭")
        user_func(*args)
        print("刷碗")

    return wrap


@myanno
def add(x , y):
    print(x + '+' + y + '=')


add("zs", "北京")

# items = [0 , 1 , 2 , 3 , 4]
# list(filter(lambda x: x % 2 == 0 , items))


