from numpy.core._multiarray_umath import ndarray

arr1 = ["hello world" , "hello python"]
import numpy as np

print(map(lambda line: line.split(" ") , arr1))
# 1.显式转换数组的数据类型 , 转换新的数据类型会产生新的数组
arr = np.array([1 , 2 , 3 , 4 , 5])
print(arr.dtype)
float_arr = arr.astype(np.float64)
print(float_arr.dtype)

# 2.数组算术
print(arr * arr)
print(arr - arr)
print(1 / arr)
print(arr ** 0.5)
# 得到数组维度
print(arr.ndim)

# 3.基础索引与切片0-2全部替换
arr[:3] = 12
print(arr)
# 当我改变arr_slice，变化也会体现在原数组上
arr_slice = arr[:3]
arr_slice[1] = 12345
print(arr)
# 如果你需要拷贝切片的话，显式定义
arr[:3].copy()

# 对多维数组的切片
arr2d = np.array([
    [1 , 2 , 3] ,
    [4 , 5 , 6] ,
    [7 , 8 , 9]
])
print(arr2d[:2])
print(arr2d[:3 , 1:])

# 4.布尔索引
# 7行4列的随机数组
data = np.random.randn(7 , 4)

# 5.数组转置和换轴：
# 重新将数组转换成对应多少行多少列
arr3 = np.arange(15).reshape(3 , 5)
print(arr3)
print(arr3.T)

# 6.数组内积
print(np.dot(arr3.T , arr3))

# 7.重新组成形状多维多维数字相乘的array的size
arr4 = np.arange(16).reshape((2 , 2 , 4))
# 展平数组
print(arr4.reshape(-1))
# 原来顺序是0，1，2，将x[0][1]的元素 换成 x[1][0]得元素  第一个括号为0轴，第二个括号为1轴
arr4.transpose((1 , 0 , 2))
print(arr4)

# 8.数组进行面向数组编程
points = np.arange(-5 , 5 , 0.01)
# 将两个一维数组的所有（x,y）对形成二维矩阵
xs , ys = np.meshgrid(points , points)

import matplotlib.pyplot as plt

z = np.sqrt(xs ** 2 + ys ** 2)
plt.imshow(z , cmap=plt.cm.gray)
plt.colorbar()
plt.title("image plot of $\sqrt{x^2 + y^2}$ for a grid of values")

# 9.将条件逻辑作为数组操作
xarr = np.array([1.1 , 1.2 , 1.3 , 1.4 , 1.5])
yarr = np.array([2.1 , 2.2 , 2.3 , 2.4 , 2.5])
cond = np.array([True , False , True , True , False])
# cond数组里为true的用xarr对应值替换，false用yarr对应值替换
result = np.where(cond , xarr , yarr)
print(result)

# 同时标量也可以
arr5 = np.random.randn(4 , 4)
print(np.where(arr5 > 0 , 2 , -2))

# 10。数学和统计方法
# 正态分布的随机数
arr7 = np.random.randn(5 , 4)
# 对二维数组的列求平均
arr7.mean(1)
# 对二维数组的行求平均
arr7.mean(0)
# 对二维数组进行累加axis=0为对列
# 对二维数组进行累乘axis=0为对列
arr7.cumsum(0)
arr7.cumprod(0)
# std,var 标准差和方差
# argmin，argmax最大，最小值的位置

# 11.唯一值与其他集合逻辑
names = np.array(['Bob', 'Job', 'Will', 'Bob', 'Joe', 'Joe'])
np.unique(names)

x = np.array([1, 2, 3, 4, 5, 6])
y = np.array([1, 5, 2, 4, 5, 1])
# 12.计算x和y交集，并排序
print(np.intersect1d(x, y))
# 13.计算x和y并集，并排序
print(np.union1d(x, y))
# 14.计算x中的元素是否包含在y中，返回一个布尔值数组
print(np.in1d(x, y))
# 15.差集，在x中但不在y中的x的元素
print(np.setdiff1d(x, y))
# 16.异或集，在x或y中，但不属于x，y交集得元素
print(np.setdiff1d(x, y))

x1 = np.array([[1., 2., 3.],
               [4., 5., 6.]])
y1 = np.array([[6., 23.],
               [-1, 7],
               [8, 9]])
# 17. 2x3 3x2 矩阵相乘
x1.dot(y1)

arr8: ndarray = np.array([[('a', 1), ('b', 2)], [('c', 3), ('d', 4)]])
arr8.astype(object)
print(arr8.reshape(-1))

# 18.矩阵运算
import numpy.linalg as la

X = np.random.randn(5, 5)
mat = X.T.dot(X)
# 计算矩阵的逆矩阵
print(la.inv(mat))
# 计算QR分解
q , r = la.qr(mat)
print(q)
print(r)
# 计算奇异值分解
print(la.svd(mat))
# 计算对角元素和
print(mat.trace())
# 计算方阵的特征值和特征向量
print(la.eig(mat))
# 计算矩阵的行列式
print(la.det(mat))
# 求解x的线性系统Ax = b，其中A是方阵
print(la.solve(mat, mat))

va = [[1],
      [1, 2],
      [1, 2, 3],
      [1, 2, 3, 4],
      [1, 2, 3, 4, 5],
      [3, 4, 5],
      [2, 3, 4, 5]]
# 现在需要将矩阵中bai所有的列表长度对du齐到最长的列表的长zhi度5，末尾全部dao用0填充
max_len = max(len(l) for l in va)
new_matrix = list(map(lambda l: l + [0] * (max_len - len(l)), va))
print(new_matrix)
# new_matrix = list(map(lambda l:l + [0]*(max_len - len(l)), va))
# print(new_matrix)

# 19.伪随机数生成
# 20.删除
m = [i for i in range(1, 10)]
m.remove(2, 3, 4)
print(m)
# m.pop(3)
# del m[2]
