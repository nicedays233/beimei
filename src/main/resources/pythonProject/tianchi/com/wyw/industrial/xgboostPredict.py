from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
import DataPreProcessing as dpp
import DistributeData as dbd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
import pandas as pd
import numpy as np


if __name__ == '__main__':
    if __name__ == '__main__':
        train_data , test_data = dpp.findOutlier()
        param_grid = {
            'n_estimators': [100, 200, 300, 400, 500],
            'max_depth': [1, 2, 3]
        }

        xgb = RandomForestRegressor()

        gcv = GridSearchCV(xgb, param_grid, scoring="accuracy", cv=6)
        gcv.fit(np.array(train_data.iloc[:, 0:-1]), y=np.array(train_data.iloc[:, -1]))
        print(gcv.best_params_)
        print(gcv.best_score_)
        print(gcv.best_estimator_)

        # xgb.fit(train_data.iloc[:, 0:-1], y=train_data.iloc[:, -1])
        # res_ = xgb.predict(test_data)

        # print(res_)
        # np.savetxt("E:/天池/工业蒸汽量预测/predictData.txt" , res_)




