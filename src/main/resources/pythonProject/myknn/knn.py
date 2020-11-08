from sklearn import *
import numpy as np
import pandas as pd
#
from sklearn.neighbors import KNeighborsClassifier

if __name__ == '__main__':
    # 获取数据
    trains_data = pd.read_excel("E:/大数据/train.xlsx", sheet_name=0)
    pred_data = pd.read_excel("E:/大数据/test.xlsx", sheet_name=0)

    # 将数据切片 ，训练集要和标签分开来
    train_data = trains_data.iloc[:,1:3]
    labels = trains_data.iloc[:, -1]

    # 准备模型 取5个离他最近的5个点
    knn = KNeighborsClassifier(n_neighbors=5)
    # 导入数据获取实际模型（获取方程组）
    knn.fit(train_data, labels)

    # 预测
    print()
    res_ = knn.predict(pred_data.iloc[:, 1:3])
    print(res_)

