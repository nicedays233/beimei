import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# data = np.arange(10)
# plt.plot(data)
# # plt.show()
# from mpl_toolkits import mplot3d
#
# ax = plt.axes(projection='3d')
# # 三维线数据
# zline = np.linspace(0 , 15 , 1000)
# xline = np.sin(zline)
# yline = np.cos(zline)
# ax.plot3D(xline , yline , zline , 'gray')
#
# # 三维散点的数据
# zdata = 15 * np.random.random(100)
# xdata = np.sin(zdata) + 0.1 * np.random.randn(100)
# ydata = np.cos(zdata) + 0.1 * np.random.randn(100)
# ax.scatter3D(xdata , ydata , zdata , c=zdata , cmap='Greens')
# plt.show()

### 1.创建图形和坐标轴
fig = plt.figure()  # 容纳坐标轴图形文字的容器
ax = plt.axes()  # 带有刻度和标签的矩形
ax.plot()

### 2.绘制正弦函数
x = np.linspace(0 , 10 , 1000)  # 0-10 1000个点
ax.plot(x , np.sin(x))
plt.show()
#### 也可以用pylab接口
plt.plot(x , np.sin(x))
#### 重复画线
plt.plot(x , np.cos(x))
plt.show()

### 3.调整图形，线条的颜色与风格
plt.plot(x , np.sin(x - 0) , color='blue')  # 标准颜色名称
plt.plot(x , np.sin(x - 1) , color='g')  # 缩写颜色代码
plt.plot(x , np.sin(x - 2) , color='0.75')  # 范围0-1的灰度值
plt.plot(x , np.sin(x - 3) , color='#FFDD44')  # 十六进制
plt.plot(x , np.sin(x - 4) , color='chartreuse')  # RGB元组 范围在0-1
plt.plot(x , np.sin(x - 5) , color=(1.0 , 0.2 , 0.3))  # HTML 颜色名称
plt.show()

### 4.调整线条的风格
plt.plot(x , x + 0 , linestyle='solid')
plt.plot(x , x + 1 , linestyle='dashed')
plt.plot(x , x + 2 , linestyle='dashdot')
plt.plot(x , x + 3 , linestyle='dotted')

#### 简写形式
plt.plot(x , x + 4 , linestyle='-')  # 实线
plt.plot(x , x + 5 , linestyle='--')  # 虚线
plt.plot(x , x + 6 , linestyle='-.')  # 点划线
plt.plot(x , x + 7 , linestyle=':')  # 实点线
plt.show()

#### 带颜色简写
plt.plot(x , x + 4 , '-g')  # 实线
plt.plot(x , x + 5 , '--c')  # 虚线
plt.plot(x , x + 6 , '-.k')  # 点划线
plt.plot(x , x + 7 , ':r')  # 实点线
plt.show()

### 5.调整图形：坐标轴x,y 轴上下限
plt.plot(x , np.sin(x))
plt.xlim(-1 , 11)
plt.ylim(-1.5 , 1.5)
plt.show()

#### 逆序显示坐标轴
plt.plot(x , np.sin(x))
plt.xlim(10 , 0)
plt.ylim(1.2 , -1.2)
plt.show()

#### axis简写设置x，y轴上下限
plt.plot(x , np.sin(x))
plt.axis([-1 , 11 , -1.5 , 1.5])

#### axis还可以自动收紧坐标轴
plt.axis('tight')

#### 图形分辨率为1：1
plt.axis('equal')
plt.show()

### 6.设置图形标签
plt.plot(x , np.sin(x))
plt.title("A Sine Curve")
plt.xlabel("x")
plt.ylabel("sin(x)")
plt.show()

#### 多条线给每条线设置图例
plt.plot(x , np.sin(x) , '-g' , label='sin(x)')
plt.plot(x , np.cos(x) , ':b' , label='cos(x)')
plt.axis('equal')

plt.legend()
plt.show()

### 7.风格转换 plt是matlab风格，ax是面向对象画法
ax = plt.axes()
ax.plot(x, np.sin(x))
ax.set(xlim=(0, 10))



