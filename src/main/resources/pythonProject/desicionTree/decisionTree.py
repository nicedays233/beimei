from math import log
import operator


#  度量数据集的无序程度（计算香农熵）
def calcShannonEnt(dataSet):  # calculate shannon entropy计算香农熵
    numEntries = len(dataSet)  # 得到数据集的长度，即矩阵行数，即数据组的个数entries词典的条目的数量，就是词条的数量
    labelCounts = {}  # 新建空字典
    for featVec in dataSet:  # 遍历数组
        currentLabel = featVec[-1]  # currentLabel 存储dataSet最后一列的数值，最后一列是最终判断的结果
        # 将最后一列的判断结果存入字典并记录数据集里判断结果出现的次数
        if currentLabel not in labelCounts.keys():  # 如果数值不在字典里
            labelCounts[currentLabel] = 0  # 如果判断不在字典里，扩展字典，将currentLabel的键值设为0
        labelCounts[currentLabel] += 1  # 将currentLabel的键值加1，记录当前，数据组的相同判断在字典里出现的次数
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries  # probablity 计算字典中的不同的判断结果在数据集中出现的概率
        shannonEnt += -prob * log(prob, 2)  # 香农熵的计算公式，其实就是算所以信息的期望值
    return shannonEnt


#  按照特征划分数据集
def splitDataSet(dataSet, axis, value):  # 输入带划分数据集，axis列的属性，value（划分数据集的特征），我们需要返回的特征的值
    retDataSet = []  # 创建新的list对象,为了不修改原始数据集
    for featVec in dataSet:
        if featVec[axis] == value:  # 找出每个数据组的axis轴的属性里的特征值，让它和value特征判断，相等去除掉value
            # 下面这个操作其实就是找每个数据组的axis列上是value的，我就删掉
            reducedFeatVec = featVec[:axis]  # 0-axis-1
            reducedFeatVec.extend(featVec[axis + 1:])  # axis+1到最后,两个合并起来
            retDataSet.append(reducedFeatVec)  # 变成[[reducedFeatVec1],[reducedFeatVec2]，[reducedFeatVec3]]
    return retDataSet  # 这里面存着所有被删过value的数据组，没有value的数据组没有放进去


def file2matrix(filename):
    fr = open(filename)
    lists = fr.readlines()
    listnum = []
    for k in lists:
        listnum.append(k.strip().split(','))
    return listnum


#  选择最好的数据集划分方式
'''
 dataSet = [[1,2,3],[4,2,6,7],[8,3,2,11]]
     for fc in dataSet:
         if fc[1] == 2:
             print(fc[:1],fc[2:],"!")
     for i in range(3):
         featlist = [example[i] for example in dataSet]
         print(featlist)
[1] [3] !
[4] [6, 7] !
[1, 4, 8]
[2, 2, 3]
[3, 6, 2]

'''


def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)  # 计算数据集的香农熵
    bestInfoGain = 0.0;
    bestFeature = -1
    for i in range(numFeatures):
        # 这个写法是遍历数据集中的每一行，把其中的第i个数据取出来组合成一个列表，每个i列表示一种属性
        featList = [example[i] for example in dataSet]  # 把属性i中相同类别的元素划在一个列表，再合起来组合成一个大列表
        uniqueVals = set(featList)  # set可以去掉重复元素
        newEntropy = 0.0
        # 找列表的第一个列表里遍历，在遍历列表里的第二个列表，以此类推
        for value in uniqueVals:  # 把所有类别的所有特征全部划分一次数据集
            subDataSet = splitDataSet(dataSet, i, value)  # 给出在属性i下不同的特征值获取每种不同划分方式的数据集
            # 对应到决策树的情况就是每次选判断条件（特征值），通过这个判断条件之后剩下来的数据集的信息熵是否减少
            prob = len(subDataSet) / float(len(dataSet))  # 计算i轴属性i下有value的数据组占整个数据组的概率
            newEntropy += prob * calcShannonEnt(subDataSet)  # 计算不同划分方式的信息熵
        infoGain = baseEntropy - newEntropy  # 计算所有的信息增益
        if infoGain > bestInfoGain:  # 选出最大的信息增益
            bestInfoGain = infoGain
            bestFeature = i  # 找到最好的划分方式特征并返回
        return bestFeature


# 针对所有特征都用完，但是最后一个特征中类别还是存在很大差异，
# 比如西瓜颜色为青绿的情况下同时存在好瓜和坏瓜，无法进行划分，此时选取该类别中最多的类
def majorityCnt(classlist):  # 作为划分的返回值，majorityCnt的作用就是找到类别最多的一个作为返回值
    classCount = {}
    for vote in classlist:  # 寻找classlist里的值将存入字典，并记录该值在classlist里出现的次数
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
        # 将classcount里的值进行排序，大的在前
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)

    return classCount[0][0]  # 返回最大值


#  创建树的代码
def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]  # 提取最后一列的判断结果，返回列表
    # 递归结束条件一：当发现到叶子结点，也就是所有的判断特征都用完了，判断结果都一致
    if classList.count(classList[0]) == len(classList):  # 检查是不是所有判断结果都是一样的，一样的那么决策树就只有一个根节点和一个子节点
        return classList[0]
    # 递归结束条件二：当发现到叶子结点，判断特征用完后，判断结果仍然有分歧，我们将判断结果较多的作为结果返回
    # 递归条件二要结合第一个条件判断，既然能到第二个条件，说明判断结果有不一样的
    # 而且再检查它还有几个属性，发现只剩下一个属性了，不能将判断结果划分了
    if len(dataSet[0]) == 1:  # 一般前面用不到，递归到最底层的叶子结点时执行
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)  # 返回最佳的属性划分方式
    bestFeatLabel = labels[bestFeat]  # 并得到该属性的字符串名
    # 由于{}设置为空，即键的值为空，所以下层字典树的创建在该{}里创建
    myTree = {bestFeatLabel: {}}  # 开始创建字典树，bestFeatLabel为根结点标签，下一层的标签放在后面的括号内
    del (labels[bestFeat])  # 删除改属性的字符串名
    featValues = [example[bestFeat] for example in dataSet]  # 把这个属性的所有特征拿出来
    uniqueVals = set(featValues)  # 删除重复的特征
    for value in uniqueVals:
        subLabels = labels[:]  # 创建新的子标签
        # split函数获取去除了属性bestFeat下value的子数据集并获得子标签，递归创建子树
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree



