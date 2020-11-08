import DataPreProcessing as dpp
from sklearn import  preprocessing
import pandas as pd
import ReadData as rd


# 归一化
def normalizationData():
    # 导入异常值排除的数据
    train_data, test_data = dpp.findOutlier()
    # 对除了target列的特征做归一化
    features_columns = [col for col in train_data.columns if col not in ['target']]
    min_max_scaler = preprocessing.MinMaxScaler()
    min_max_scaler_model = min_max_scaler.fit(train_data[features_columns])
    train_data_scaler = min_max_scaler_model.transform(train_data[features_columns])
    test_data_scaler = min_max_scaler_model.transform(test_data[features_columns])

    # 完善列名和补充target
    train_data_scaler = pd.DataFrame(train_data_scaler)
    train_data_scaler.columns = features_columns
    test_data_scaler = pd.DataFrame(test_data_scaler)
    test_data_scaler.columns = features_columns
    train_data_scaler['target'] = rd.readData()[0]['target']
    # print(train_data_scaler.describe())
    # print(test_data_scaler.describe())
    return train_data_scaler, test_data_scaler


if __name__ == '__main__':
    normalizationData()
