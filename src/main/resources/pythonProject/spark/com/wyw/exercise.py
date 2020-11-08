msg = 123


def abc():
    msg = 456

    def cde():
        print(msg)

    cde()


print(msg)
abc()

msg2 = 123

kkk = lambda x: x + 10


def abc2():
    msg2 = 456

    def cde2():
        global msg2
        print(msg2)
        print(kkk(20))

    cde2()


print(msg2)
abc2()

A = [i for i in range(2, 102, 2)]
print( A)


def my_decorator(some_func):
    def wrapper(*args):
        print("china!")
        some_func(*args)
        print("called")
    return wrapper

# 装饰器增加功能
# add这个函数会传给装饰器的参数，这里的add就i是some_func
# add的两个参数会传给wrapper的参数列表里
@my_decorator
def add(x, y):
    print(x,"+",y, "=", x+y)
add(5, 6)


msg = 'created in module'
def outer():
    def inner():
        global msg
        msg = 'changed'
    inner()
outer()

print(msg)
