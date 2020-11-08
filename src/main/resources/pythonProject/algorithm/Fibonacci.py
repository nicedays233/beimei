import numpy as np
import pandas as pd
#n 矩阵维度n*n
def makeSnake(n):
    snakeArr = np.zeros((n, n))
    # 制作一个point 和 方向控制变量 direction
    xPos = yPos = 0
    direction = 1 # 1右  2下  3左  4下 有限判断都可以用类似flag的形式做判断解决问题
    # 获取斐波那契数列
    fib = fibonacci(n*n)
    # 循环填充数据
    for num in fib:
        snakeArr[xPos][yPos] = num
        # 寻找下一个点
        if direction == 1:
            if yPos + 1 < n and snakeArr[xPos][yPos + 1] == 0:
                yPos += 1
            else:
                direction = 2
                xPos += 1
        elif direction == 2:
            if xPos + 1 < n and snakeArr[xPos + 1][yPos] == 0:
                xPos += 1
            else:
                direction = 3
                yPos -= 1
        elif direction == 3:
            if yPos - 1 >= 0 and snakeArr[xPos][yPos - 1] == 0:
                yPos -= 1
            else:
                direction = 4
                xPos -= 1
        else:
            if xPos - 1 >= 0 and snakeArr[xPos - 1][yPos] == 0:
                xPos -= 1
            else:
                direction = 1
                yPos += 1
    print(snakeArr)




# num 整个数列的长度
def fibonacci(num):
    fibArr = [1, 1]
    one=two=1
    three=0
    for rn in range(num - 2):
        three = one + two
        fibArr.append(three)
        # 往前移位
        one,two=two,three
    fibArr.reverse()
    return fibArr


if __name__ == '__main__':
    # print(fibonacci(10))
    print(makeSnake(4))

