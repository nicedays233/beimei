import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
from sklearn import datasets
if __name__ == '__main__':

    train_data, labels_data = datasets.load_iris(True)
    # print(train_data.shape)
    knn = KNeighborsClassifier(n_neighbors=5)
    # # 需要训练集和标签集，函数自己会分测试集进行k折交叉验证计算
    score = cross_val_score(knn, train_data, labels_data, scoring='accuracy', cv=6)

    print(np.mean(score))
    # print(train_data.describe())
    # error = []
    # for i in range(1, 14):
    #     knn = KNeighborsClassifier(n_neighbors=i)
    #     score = cross_val_score(knn , train_data , labels_data , scoring='accuracy' , n_jobs=6).mean()
    #     error.append(1-score)
    #
    # plt.plot(np.arange(1, 14), error)
    # plt.show()

