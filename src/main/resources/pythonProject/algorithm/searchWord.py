import numpy as np
import pandas as pd


# 找寻单词的每个字母在矩阵中的位置并返回字母坐标
def findChrPostition(marritx , word):
    chrPos = []
    for wd in word:
        # 该字符所有所有位置
        xyArr = np.where(marritx == wd)
        chrPos.append(list(zip(xyArr[0] , xyArr[1])))
    return chrPos


# 检查两点是否有关联性
def checkPointRelation(point1 , point2):
    if point1[0] == point2[0] and abs(point1[1] - point2[1] == 1) or (
            point1[1] == point2[1] and abs(point1[0] - point2[0]) == 1):
        return True
    else:
        return False


# b数组维数 word你要找的单词
def findWord(n , word):
    initArr = np.array(list(map(lambda x: chr(x), np.random.randint(65 , 91 , size=n * n)))).reshape((n , n))
    # 找寻单词的每个字母在矩阵中的位置并返回字母坐标
    # [a[(0,1),(0,2), (4,8), (5,7)], h[(1,1), (4,9), (6,7), (8,10), (12, 16)],i[(),()]]
    wordPos = findChrPostition(initArr , word)

    paths = [[] for i in range(len(word) - 1)]  # [[[(0,1),(1,1)],[(4,8),(4,9)]],[]]
    for r in range(len(word) - 1):
        if r == 0:
            for p1 in wordPos[0]:
                for p2 in wordPos[1]:
                    if checkPointRelation(p1, p2):
                        paths[r].append([p1, p2])
        else:

            # r=1path就找[[(0,1),(1,1)],[(4,8),(4,9)]] , r + 1就是找第三个点 ，r=2就找后面的让第四个点与path第二个来匹
            # path 永远比 wordPos少一个 ，r为当前所找位置，path是当前位置的前一个存储，
            for o1 in paths[r - 1]:
                for p3 in wordPos[r + 1]:
                    if checkPointRelation(o1[-1], p3):
                        o1.append(p3)
                        paths[r].append(o1)
    print(paths[-1])




if __name__ == '__main__':
    findWord(500 , 'CHINA')
