import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn import datasets


if __name__ == '__main__':
    # 获取鸢尾花数据
    datas,labels = datasets.load_iris(True)

    print(datas, labels)

    # 随机获取数组中的条数，洗牌150个索引
    index = np.arange(150)
    np.random.shuffle(index)

    # 拿到训练数据集，和目标标签一共100个
    train_data, labels_data = datas[index[:100]], labels[index[:100]]
    # 拿到测试数据集，和测试的目标标签50个
    test_data, test_labels_data = datas[index[100:]], labels[index[100:]]
    # 先把数组切成5段


    # 建造模型
    knn = KNeighborsClassifier(n_neighbors=12)
    knn.fit(train_data, labels_data)

    res_ = knn.predict(test_data)

    print("---------预测效果-----------")
    print(res_)
    print("---------预测效果-----------")
    print(test_labels_data)
    print("---------模型命中-----------")
    print((res_ == test_labels_data).sum() / len(test_data))

