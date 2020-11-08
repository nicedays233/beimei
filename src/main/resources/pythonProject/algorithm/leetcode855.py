import numpy as np


step = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13]
# 假设点在3，4
fill1 = np.ndarray(5 * 5)


def spiralMatrixIII(R: int, C: int, r0: int, c0: int):
    if R > C:
        fill = [0 for x in range(0, R * R)]
        s3 = np.ndarray(R * R)
    else:
        fill = [0 for x in range(0, R * R)]
        s3 = np.ndarray(C * C)
    for i in range(0, 10):
        fill[i] = i
    direction = 1  # 1右  2下  3左  4下 有限判断都可以用类似flag的形式做判断解决问题
    s1 = np.zeros([R, C])
    s2 = []

    xPos = r0
    yPos = c0
    stepCount = 0
    for num in range(0, R * R):
        num -= 1
        # 向右走
        if direction == 1:
            # 判断是否可以继续走
            if stepLeft(num, stepCount) == 0:
                direction = 2
                stepCount = 0
                continue
            # 判断是在边界内
            elif R > yPos >= 0 and C > xPos >= 0:
                s2 += [xPos, yPos]
                xPos += 1
                stepCount += 1
            else:
                xPos += 1
                stepCount += 1
        # 向下走
        if direction == 2:
            # 判断是否可以继续走
            if stepLeft(num, stepCount) == 0:
                direction = 3
                stepCount = 0
                continue
            # 判断是在边界内
            elif R > yPos >= 0 and C > xPos >= 0:
                s2 += [xPos, yPos]
                yPos += 1
                stepCount += 1
            else:
                yPos += 1
                stepCount += 1
        # 向左走
        if direction == 3:
            # 判断是否可以继续走
            if stepLeft(num, stepCount) == 0:
                direction = 4
                stepCount = 0
                continue
            # 判断是在边界内
            elif R > yPos >= 0 and C > xPos >= 0:
                s2 += [xPos, yPos]
                xPos -= 1
                stepCount += 1
            else:
                xPos -= 1
                stepCount += 1
        # 向上走
        if direction == 4:
            # 判断是否可以继续走
            if stepLeft(num, stepCount) == 0:
                direction = 1
                stepCount = 0
            # 判断是在边界内
            elif R > yPos >= 0 and C > xPos >= 0:
                s2 += [xPos, yPos]
                yPos -= 1
                stepCount += 1
            else:
                yPos -= 1
                stepCount += 1




    print(s2)


def stepLeft(num, stepCount):
    return step[num] - stepCount









if __name__ == '__main__':
    spiralMatrixIII(5, 5, 0, 0)

    # for i in range(0, 10):
    #     fill1[i] = i
    # print(fill1)


