## Python函数与对象：

### 函数参数：

>  *以元组方式传入       ** 以字典方式传入

```python
# *以元组方式传入 **以字典方式传入
def name(arg1,*arg2,**arg3):
    print(arg1)
    print(arg2)
    print(arg3)

name(1,3,2,3,2,(321,23),2,3,e=2,f=3)
# 1 	
# (3, 2, 3, 2, (321, 23), 2, 3) 	
# {'e': 2, 'f': 3} 	
```



### 装饰器：

```python
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

```

### 全局变量：

- 定义在模块中的变量

  - 全局变量在整个模块中可见

  - globals（）函数

    > 返回所有定义在改模块中的全局变量

  - 修改全局变量时，使用global关键字申明变量

```python
msg = 'created in module'
def outer():
    def inner():
        global msg
        msg = 'changed'
    inner()
outer()

print(msg) # 会打印changed，不加global不会改变

```

### 自由变量：

> nonlocal关键字用来在函数或其他作用域中使用外层(非全局)变量

```python
def outer_1():
    msg = 'create in outer'
    def inner():
        nonlocal msg
        msg = "changed"
    inner()
    print(msg)
outer_1()
# 打印changed
```

![image-20200825100142467](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200825100142467.png)

### LEGB规则：

![image-20200825100655934](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200825100655934.png)

- 使用LEGB的顺序来查找一个符号对应的对象
  - local -> Enclosed -> Global -> Built-in
    - `Local：`一个函数或者类方法内部
    - `Enclosed：`嵌套函数内
    - `Global：`模块层级
    - `Built-in：`python内置符号
- 举例：

```python
type=4
def f1():
    type=3
    def f2():
        type=2
        def f3():
            type=1
            print("finaltype=",type)
        f3()
    f2()
    
f1()

# 打印出来finaltype=1
```



### 函数返回值：



### 生成器表达式：

```python
(x**3 for x in range(1, 10))
```

### lambda表达式：

- 是一种匿名函数
- 只包含一条语句，并自动返回这条语句的结果

```python
f = lambda x: x*x
```

- 常用方式：流处理

```python
# 生成n*n的随机字母矩阵
# 对map的第二个参数的列表或者数组每个元素进行遍历
initArr = np.array(list(map(lambda x: chr(x), np.random.randint(65 , 91 , size=n * n)))).reshape((n , n))
```

### 偏函数：

> import functools

简单总结`functools.partial`的作用就是，把一个函数的某些参数给固定住（也就是设置默认值），返回一个新的函数，调用这个新函数会更简单

```python
int('12345', base=2)
int2 = functools.partial(int, base=2)
# 可以将参数默认固定住，int2('12345')
```



### 正则表达式：

- **正则模块**
  - `re模块`
- **常用方法**
  - `compile()`：编译正则表达式，生成Pattern对象
  - `match()`：查看字符串开头是否符合匹配模式
  - `search()`：扫描字符串，返回**第一个**成功的
  - `findall()`：所有成功匹配得子串，作为列表返回，没有返回空列表
  - `sub()`：替换正则的匹配项







![image-20200825114905242](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200825114905242.png)

```python
str = "hello world 22,hello flink,helle hadoop 123 222 33"
```

#### match（）：

```python

if re.match('hes', str):
    print("find!!!")
else:
    print("not found")
    
    
# not found
```

#### findall（）：

```python
print(re.findall('[0-9]+', str))
# ['22', '123', '222', '33']
```

#### search（）：

```python
print(re.search('[0-9]+', str).group(0))
# 22

str1 = "1998-5-6 123456 {action:1, type:10}"
print(re.search("(\\d{4}-\\d+-\\d+).*{\\w+:(\\d+).*:(\\d+)}", str1).group(1))
# 1998-5-6
```

#### sub（）：

```python
str2 = "ababa"
print(re.sub('','-', str2))
# -a-b-a-b-a-
```

### 定义类：

```python
class Shape:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
    def move(self, deltaX, deltaY):
        self.x += deltaX
        self.y += deltaY
shape = Shape(1, 2)
shape2 = Shape()
shape2.ui = "UI" # 动态定义实例变量
shape.ui会报错 # 上面定义单独那个实例的实例变量
```

