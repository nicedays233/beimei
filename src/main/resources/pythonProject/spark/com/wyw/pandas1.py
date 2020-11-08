import pandas as pd
import numpy as np
# 一：Series是一种一维数组型对象 ,包含了值序列和索引序列
obj = pd.Series([4, 7, -5, 3])
print(obj)

# 创建索引序列
obj2 = pd.Series([4, 7, -5, 3], index=['d', 'b', 'a', 'c'])
print(obj2)

# 利用字典生成Series
sdata = {'oo': 3500, 'sdf': 125, 'ssd': 200}
obj3 = pd.Series(sdata)
# series有isnull，notnull，join等方法

# 二.dataFrame
data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada', 'Nevada'],
        'year': ['2000', '2001', '2002', '2001', '2002', '2003'],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]}
frame = pd.DataFrame(data)
print(frame)
# 1.选出头部5行
print(frame.head())

# 2.指定列名顺序
print(pd.DataFrame(data, columns=['year', 'state', 'pop']))
# 3.插新列
print(pd.DataFrame(data, columns=['year', 'state', 'pop', 'debt']))
# 4.创建表，输入参数列名和数据字典或者二维数组，数据参数必要，index索引可以不要，列名也可以不要
dates = pd.date_range('20200101',periods=6, freq='3D')
df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
print(pd.DataFrame(data, columns=['year', 'state', 'pop']))
print(pd.DataFrame(data))
print(pd.DataFrame(np.random.randn(6, 4)))

# 5.按列名排序，按行名排序
df.sort_index(axis=1, ascending=True)
df.sort_index(axis=0, ascending=True)
# 6.按列值排序
print(df.sort_values(by='B'))
print(df.sort_values(axis=0, by=['A', 'B']))
# 7.按列行拿值
value = df['A'][:'2020-01-16']
print(value)
# 8.按行列拿值
value1 = df.loc[['2020-01-16'], 'A']
# value2 = df.iloc['2020-01-16':'2020-01-20', 'A']
print(value1)

# 9.整表滤值 表值大于0.5的留下
df2 = df[df > 0.5]
print(df2)

# 10.新增列
df['debt'] = 0
print(df)
# 11.删除列
print(df.drop(columns='debt'))
del df['debt']

# 12.缺失值
# 删除所有缺失行
print(df[df > 0].dropna(how='any'))
# 填充所有缺失值
print(df['A'].mean())
# 按列填充空值，使用列的平均值
print(df[df > 0]['A'].fillna(value=df['A'].mean()))
# print(df.aggregate(df))





