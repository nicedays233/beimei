from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import *
import DistributeData as dbd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np


def train_model(model, param_grid=[], X=[], y=[], splits=5, repeats=5):
    rkFold = RepeatedKFold(n_splits=splits, n_repeats=repeats)
    gsearch = GridSearchCV(model, param_grid, cv=rkFold, scoring="neg_mean_squared_error", verbose=1, return_train_score=True, n_jobs=4)

    gsearch.fit(X, y)

    model = gsearch.best_estimator_
    best_idx = gsearch.best_index_
    print(model)
    print(gsearch.best_params_)
    print(gsearch.best_score_)

    # return model, best_idx


if __name__ == '__main__':
    train_data, test_data = dbd.featureDimReduce()
    model = ['GradientBoosting']
    opt_models = dict()
    forest = RandomForestRegressor()
    GBDT = GradientBoostingRegressor()
    GBDT2 = RandomForestRegressor(bootstrap=True , criterion='mse' , max_depth=5 ,
                          max_features='auto' , max_leaf_nodes=None ,
                          min_impurity_decrease=0.0 , min_impurity_split=None ,
                          min_samples_leaf=1 , min_samples_split=7 ,
                          min_weight_fraction_leaf=0.0 , n_estimators=250 ,
                          n_jobs=None , oob_score=False , random_state=None ,
                          verbose=0 , warm_start=False)
    GBDT2.fit(train_data.iloc[:, 0:-1], y=train_data.iloc[:, -1])
    res_ = GBDT2.predict(test_data)

    # print(res_)
    np.savetxt("E:/天池/工业蒸汽量预测/predictData.txt", res_)
    # with open("E:/天池/工业蒸汽量预测/predictData.txt", "w") as f:
    #     for i in res_:
    #         f.write(i.toString() + "\n")  # 这句话自带文件关闭功能，不需要再写f.close()


    score_models = pd.DataFrame(columns=['mean', 'std'])
    param_grid = {
        'n_estimators': [150, 250, 350, 450],
        'max_depth': [1, 2, 3, 4, 5],
        'min_samples_split': [5, 6, 7, 8]
    }

    train_model(
        forest,
        X=train_data.iloc[:, 0:-1],
        y=train_data.iloc[:, -1],
        param_grid=param_grid,
        repeats=1
    )
    #
    # cv_score.name = model
    # score_models = score_models.append(cv_score)
    # print(opt_models[model])
