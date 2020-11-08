import NormalizeData as nd
import matplotlib.pyplot as plt
import seaborn as sns
import ReadData as rd
import numpy as np
from sklearn.decomposition import PCA
import pandas as pd


# 查询KDE分布
# def showDataDistribution():
#     train_data, test_data = rd.readData()
#     dist_cols = 6
#     dist_rows = len(test_data.columns)
#     print(dist_rows)
#     plt.figure(figsize=(4 * dist_cols, 4 * dist_rows))
#     i = 1
#     for col in test_data.columns:
#         ax = plt.subplot(dist_rows, dist_cols, i)
#         ax = sns.kdeplot(train_data[col], color="Red", shade=True)
#         ax = sns.kdeplot(test_data[col], color="Blue", shade=True)
#         ax.set_xlabel(col)
#         ax.set_ylabel("Frequency")
#         ax = ax.legend(["train", "test"])
#     # plt.show()
#         i += 1
#     plt.show()


# 加载数据
train_data_scaler, test_data_scaler = rd.readData()


# 根据kde分布找到6列分布不均的列展示一下
def showDataDistribution():
    drop_col = 6
    drop_row = 1
    plt.figure(figsize=(5 * drop_col, 5 * drop_row))

    for i, col in enumerate(["V5", "V9", "V11", "V17", "V22", "V28"]):
        ax = plt.subplot(drop_row, drop_col, i + 1)
        ax = sns.kdeplot(train_data_scaler[col], color="Red", shade=True)
        ax = sns.kdeplot(test_data_scaler[col], color="Blue", shade=True)
        ax.set_xlabel(col)
        ax.set_ylabel("Frequency")
        ax = ax.legend(["train", "test"])
    plt.show()


# 查看特征相关性
def showDataCorr():
    plt.figure(figsize=(20, 16))
    column = train_data_scaler.columns.tolist()
    mcorr = train_data_scaler[column].corr(method="spearman")
    mask = np.zeros_like(mcorr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    g = sns.heatmap(mcorr, mask=mask, cmap=cmap, square=True, annot=True, fmt='0.2f')
    # plt.show()
    mcorr = mcorr.abs()
    numerical_corr = mcorr[mcorr['target'] > 0.1]['target']
    return numerical_corr


# 特征降维
def featureDimReduce():
    # numerical_corr = showDataCorr()
    pca = PCA(n_components=16)
    new_train_pca_90 = pca.fit_transform(train_data_scaler.iloc[:, 0:-1])
    new_test_pca_90 = pca.transform(test_data_scaler)

    new_train_pca_90 = pd.DataFrame(new_train_pca_90)
    new_test_pca_90 = pd.DataFrame(new_test_pca_90)

    new_train_pca_90['target'] = train_data_scaler['target']

    # print(new_train_pca_90.describe())
    return new_train_pca_90, new_test_pca_90






if __name__ == '__main__':
    featureDimReduce()
   # showDataCorr()
