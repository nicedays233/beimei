from typing import Any, Tuple

import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

#  定义两种结点类型
decisionNode = dict(boxstyle="sawtooth", fc="0.8",pad=0.3)
#  boxstyle为文本框的类型，sawtooth是锯齿形，ec是边框线颜色，edgecolor,ew为edgewidth
leafNode = dict(boxstyle="round4", fc="0.8",pad=0.3,)
#  定义叶节点，round4是方框椭圆型
arrow_args = dict(arrowstyle="<-")
#  定义箭头方向 与常规的方向相反
#  Advanced Raster Graphics System高级光栅图形系统

# 声明绘制一个节点的函数
'''
annotate是关于一个数据点的文本 相当于注释的作用 
nodeTxt:即为文本框或锯齿形里面的文本内容
nodeType：是判断节点还是叶子节点
bbox给标题增加外框
nodeTxt为要显示的文本
centerPt为文本的中心点，箭头所在的点
parentPt为指向文本的点  pt为point

'''


def plotNode(nodeTxt, centerPt, parentPt, nodeType):  # 输入4个参数：结点文字,终点，起点，结点的类型
    createPlot.ax1.annotate(nodeTxt,fontsize=5, xy=parentPt, xycoords='axes fraction', xytext=centerPt, textcoords='axes fraction',
                            va="center", ha="center", bbox=nodeType,
                            arrowprops=arrow_args)


#  annotate给这个结点上注释文字（）里定义
#  xycoords为x轴y轴的coordinates坐标，选用轴分数
#  arrowprops 箭头性质arrowproperties
'''
def createPlot():
    fig = plt.figure(1, facecolor='white')  # facecolor背景颜色
    fig.clf()  # figure图像clf:clearfigure 清除当前图像
    createPlot.ax1 = plt.subplot(111, frameon=False)  # frameon是否绘制图像边缘，绘制1*1网格的第一子图
    plotNode('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode)  # 调用下面定义的画结点的函数
    plotNode('a leaf node', (0.8, 0.1), (0.3, 0.8), leafNode)
    plt.show()
'''

#  获取字典树的叶子结点个数
def getNumLeafs(myTree):
    numLeafs = 0  # 定义记录叶节点的数目的变量
    firstside = list(myTree.keys())  # 我们获取当前输入的树的所有键，并将其转换成列表
    firstStr = firstside[0]  # 并把当前列表第一个结点（当前树的根节点）的键获取
    secondDict = myTree[firstStr]  # 去输入的字典树里找这个键对应的值，存入另一个空字典
    for key in secondDict.keys():  # 查找存入这个字典的值它是不是字典类型；是说明下面还有分支，不是说明是叶子结点
        if type(secondDict[key]) == dict:
            numLeafs += getNumLeafs(secondDict[key])  # 是字典类型就递归找子节点是不是叶子结点
        else:
            numLeafs += 1  # 不是字典类型说明是叶子结点，数量加一，并返回上一层
    return numLeafs

#  获取字典树的深度
def getTreeDepth(myTree):
    maxDepth = 0
    firstside = list(myTree.keys())   # 我们获取当前输入的树的所有键，并将其转换成列表
    firstStr = firstside[0]  # 并把当前列表第一个结点（当前树的根节点）的键获取
    secondDict = myTree[firstStr]  # 去输入的字典树里找这个键对应的值，存入另一个空字典
    for key in secondDict.keys():  # 查找存入这个字典的值它是不是字典类型；是说明下面还有分支，不是说明下面没有深度可寻
        if type(secondDict[key]) == dict:
            thisDepth = 1 + getTreeDepth(secondDict[key])  # 是字典类型，继续寻找下面分支的深度，并将当前深度记录加一
        else:
            thisDepth = 1  # 如果刚开始就只有根节点就返回深度一，如果后面递归到这里，发现不是字典类型，返回的1值没有用，意义是使下面比较时保持返回的maxdepth不变，
        if thisDepth > maxDepth: maxDepth = thisDepth  # 每层都比较更新一下树的最大深度，并返回上层
    return maxDepth

#  在父子结点的箭头的中间处填充文本
def plotMidText(cntrPt, parentPt, txtString):  # 分别输入终点，起点，和文本内容
    # 找到输入文本的位置，即终点和起点连线的中点处
    xMid = (parentPt[0] + cntrPt[0]) / 2.0
    yMid = (parentPt[1] + cntrPt[1]) / 2.0
    createPlot.ax1.text(xMid, yMid, txtString,fontsize=5)  # 在（xMid,yMid）位置填充txtString文本

#  所以结点的绘制过程是根左右深度遍历到最左边的叶子结点，确认是根直接绘制，。
#  然后把最左边最小的根节点的叶子结点绘制完往上递归绘制根节点，再绘制根节点的兄弟姐妹，再往上回退，再绘制。
def plotTree(myTree, parentPt, nodeTxt):  # 输入当前的字典树，父节点，结点填充文本
    numLeafs = getNumLeafs(myTree)  # 得到当前的根节点树下的叶子结点个数
    depth = getTreeDepth(myTree)  # 得到当前根节点树下的最大深度
    firstside = list(myTree.keys())  # 获取了当前树的所有键
    firstStr = firstside[0]  # 得到当前节点的键，键值如果是字典，那么键里存的就是根节点文本，
    # 计算子节点的坐标，一开始最初始的树的子节点算出来和根节点的坐标是一样的，所以画不出指向根结点箭头
    # 详细解释一下中点公式怎么算的，首先最开始是因为xOff定义在脱出画面的半个结点长度
    # 因此需要给它加上（当前根的叶子节点数+1）/2个的长度为1/totalW的距离才能到达当前子节点中点的位置，所以下列公式即可算出
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs)) /2.0 / plotTree.totalW, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)  # 填充当前的父子结点之间的文本信息
    plotNode(firstStr, cntrPt, parentPt, decisionNode)  # 绘制当前根结点和指向根结点箭头
    secondDict = myTree[firstStr]  # 获取当前根节点下面的子树
    plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD  # 纵坐标到下一层，将减少1/totalD的权重长度
    for key in secondDict.keys():  # 遍历字典的值，找值类型是否是字典，即找根结点所有的分支，找叶子节点
        if type(secondDict[key]) == dict:
            # 这里有个很重要的结论是：如果当前键的键值是字典，说明有子树
            # 而且键存着是子树的根节点文本
            # 当前键的键值不是字典类型，那么说明键存着父子结点填充文本，键值为叶子结点文本
            # 这里三个参数分别是当前字典的值(也就是分支树），下一层的根节点坐标，和下一层根节点要填充的文本
            plotTree(secondDict[key], cntrPt, str(key))  # 是字典类型，继续递归绘制下一层的根节点
        else:
            # 不是字典类型，说明已经到了叶子结点，接下来绘制叶子结点
            plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW  # 一旦发现叶子节点，从左往右不断绘制叶子结点，体现在每次给叶子节点横坐标加1/totalW的长度
            # 绘制当前的叶子节点和指向叶节点的箭头，和父子结点之间的填充文本
            # 起点是cntrPt,此时的cntrPt其实是父节点的坐标值，(plotTree.xOff, plotTree.yOff)点是子节点的坐标值
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD  # 返回上层函数的时候要将y坐标恢复成上层的函数坐标值


#  更新版的绘制字典树
def createPlot(inTree):  # 这个参数是输入初始树
    fig = plt.figure(1, facecolor='white')  # facecolor背景颜色

    fig.clf()  # figure图像clf:clearfigure 清除当前图像

    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)  # frameon是否绘制图像边缘，绘制1*1网格的第一子图 ,**axprops定义为2维坐标轴
    plotTree.totalW = float(getNumLeafs(inTree))  # 获取初始树的所有叶子节点个数
    plotTree.totalD = float(getTreeDepth(inTree))  # 获取初始树的最大深度
    # totalW是叶子结点个数，而整张图的横纵长度为1，所以1/totalW，1/totalD为一个结点的长度
    plotTree.xOff = -0.5 / plotTree.totalW  # 在图的零点再向左偏移半个结点长度，以此之后获取结点中点的位置
    plotTree.yOff = 1.0
    # 这里初始值之所以这样输入是因为，其实整棵树画出来，初始树的根节点上面还有一个虚拟的根节点
    # 不过这个虚拟根节点的坐标和初始树的根节点坐标一致，结点文本为空，所以和初始树根节点重合，导致看不出来
    plotTree(inTree, (0.5, 1.0), '')  # 输入初始树，和根节点坐标，和空的字符串

    plt.show()


def retrieveTree(i):
    listOfTrees = [{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                   {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}]
    return listOfTrees[i]

import decisionTree
lenses = decisionTree.file2matrix('E:/machinelearingdatas/machinelearninginaction-master/Ch03'
          '/car.data')
lensesLabels = ['buying', 'maint', 'doors','persons','lug_boot','safety']
lensesTree = decisionTree.createTree(lenses,lensesLabels)

print(createPlot(lensesTree))




