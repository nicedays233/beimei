import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import ReadData as rd


def findOutlier():
    train_data, test_data = rd.readData()
    plt.figure(figsize=(18, 10))
    plt.boxplot(x=train_data.values, labels=train_data.columns)
    plt.hlines([-7.5, 7.5], 0, 40, colors='r')
    plt.show()
    train_data = train_data[train_data['V9'] > -7.5]
    test_data = test_data[test_data['V9'] > -7.5]
    # train_data.describe()
    # test_data.describe()
    return train_data, test_data



