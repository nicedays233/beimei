import numpy as np
import cv2
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import seaborn as sns
import matplotlib.style as style
if __name__ == '__main__':
    X = []
    for i in range(10):
        for j in range(3000):
            digit = cv2.imread("E:/mnist_data/%d.%d.jpg"%(i,j))
            X.append(digit[:, :, 1])
    data = np.asarray(X)



    labels = np.array([j for j in range(0, 10)] * 3000)

    labels.sort()
    # 前两个是目标数据的训练集和测试集，label的训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(data , labels , test_size=0.2)

    X_train.shape = (24000, -1)
    X_test.shape = (6000, -1)
    # 建立模型
    knn = KNeighborsClassifier(n_neighbors=154)
    knn.fit(X_train, y_train)
    res_ = knn.predict(X_test)

    print(accuracy_score(y_test, res_))

    # dgt: None = cv2.imread("E:/mnist_data/1.1.jpg")
    # plt.imshow(dgt)
    # plt.show()
    # plt.imshow(dgt, cmap=plt.cm.gray)
    # img = cv2.cvtColor(dgt, code=cv2.COLOR_BGR2GRAY)

