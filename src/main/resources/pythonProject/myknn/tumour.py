import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split , cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

if __name__ == '__main__':
    datas,labels = datasets.load_breast_cancer(True)
    # 将小数点变成2位
    np.set_printoptions(suppress=True, precision=10, threshold=2000, linewidth=150)
    pd.set_option("display.float_format", lambda x: '%.2f'%x)



    # 随机获取数组中的条数，洗牌150个索引
    index = np.arange(569)
    np.random.shuffle(index)

    # 归一化参数 最大最小参数
    # print((X_train[: , :1] - X_train[: , :1].min()) / (X_train[: , :1].max() - X_train[: , :1].min()))
    # 将训练集数据归一化
    mms = MinMaxScaler()
    g_ = mms.fit_transform(datas)

    # # 前两个是目标数据的训练集和测试集，label的训练集和测试集
    X_train , X_test , y_train , y_test = train_test_split(g_ , labels , test_size=0.2)


    # 建造模型
    knn = KNeighborsClassifier()
    params = {'n_neighbors': [i for i in range(1, 26)],
              'weights': ['distance', 'uniform'],
              'p': [1, 2]
              }
    # 网格穷举搜索将所有的参数算一遍，并且会自动分验证集和训练集
    gcv = GridSearchCV(knn, params, scoring="accuracy", cv=6)
    gcv.fit(X_train, y_train)
    print(gcv.best_estimator_)
    print(gcv.best_index_)
    print(gcv.best_params_)

    print(gcv.best_score_)


    res_ = gcv.predict(X_test)

    matx = confusion_matrix(y_test, res_)
    plot_confusion_matrix(matx
                          , classes=
                          , title='Gender-Confusion matrix')

    print(accuracy_score(y_test, res_))

    # # 需要训练集和标签集，函数自己会分验证集进行k折交叉验证计算
    # score = cross_val_score(knn, X_train, y_train, scoring='accuracy' , cv=6)
def plot_confusion_matrix(cm, classes,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=0)
    plt.yticks(tick_marks, classes)

    thresh = cm.max() / 2.
    for i, j in np.itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')









