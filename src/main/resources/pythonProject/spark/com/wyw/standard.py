from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
# fit_transform里需要dataframe
z_score = scaler.fit_transform(xx[['xxx']])
z_score.mean()
z_score.std()


from sklearn.preprocessing import MinMaxScaler
import pandas as pd
pd.DataFrame()
min_max = MinMaxScaler()
# fit_transform里需要dataframe
pre_min_maxed = scaler.fit_transform(xx[['xxx']])
