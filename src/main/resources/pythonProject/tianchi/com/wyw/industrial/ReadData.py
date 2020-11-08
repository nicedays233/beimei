import pandas as pd


# 导入文件
def readData():
    train_data_file = "../data/zhengqi_train.txt"
    test_data_file = "../data/zhengqi_test.txt"
    train_data = pd.read_csv(train_data_file, sep='\t', encoding='utf-8')
    test_data = pd.read_csv(test_data_file, sep='\t', encoding='utf-8')
    return train_data, test_data
