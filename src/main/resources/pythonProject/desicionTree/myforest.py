import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier,ExtraTreesClassifier
from sklearn.ensemble import  GradientBoostingClassifier

if __name__ == '__main__':

    datas, labels = datasets.load_wine(True)

    # print(datas)
    #
    # lensesLabels = ['alcohol', 'malic_acid', 'ash', 'alcalinity_of_ash', 'magnesium', 'total_phenols', 'flavanoids', 'nonflavanoid_phenols', 'proanthocyanins', 'color_intensity', 'hue', 'od280/od315_of_diluted_wines', 'proline']
    #
    # dt.createTree(datas, lensesLabels)
    #
    # print(tp.createPlot(datas + labels, lensesLabels))

    X_train,X_test,y_train,y_test = train_test_split(datas, labels, random_state=1024)
    dtc = DecisionTreeClassifier(criterion="entropy")

    dtc.fit(X_train, y_train)

    y_ = dtc.predict(X_test)

    # print(accuracy_score(y_test, y_))
    # 评估的是训练集的6种模型取平均
    print(cross_val_score(dtc, datas, labels, scoring="accuracy", cv=6).mean())

    rfc = RandomForestClassifier(criterion="entropy")
    print(cross_val_score(rfc, datas, labels,scoring="accuracy", cv=6).mean())

    efc = ExtraTreesClassifier(criterion="entropy")
    print(cross_val_score(efc, datas, labels,scoring="accuracy", cv=6).mean())

    gbdt = GradientBoostingClassifier(learning_rate=0.5)
    print(cross_val_score(gbdt, datas, labels, scoring="accuracy", cv=6).mean())
