import numpy as np
import pandas as pd
import matplotlib.style as style
import matplotlib.pyplot as plt
import seaborn as sns
# # 读文件含表头
# df = pd.read_csv('E:\大数据\python\ex1.csv')
# print(df)
#
# df1 = pd.read_table('E:\大数据\python\ex1.csv' , sep=',')
# print(df1)
#
# # 读文件不含表头
# df2 = pd.read_csv('E:\大数据\python\ex2.csv' , header=None)
# print(df2)
#
# df3 = pd.read_csv('E:\大数据\python\ex2.csv' , names=['a' , 'b' , 'c' , 'd' , 'message'])
# print(df3)
#
# # 将指定列为索引
# df4 = pd.read_csv('E:\大数据\python\ex2.csv' , names=['a' , 'b' , 'c' , 'd' , 'message'] , index_col='message')
# print(df4)
#
# # 建立分层索引，就是两层行号
# df5 = pd.read_csv('E:\大数据\python\csv_mindex.csv' , index_col=['key1' , 'key2'])
# print(df5)
#
# 其他格式读取
df6 = pd.read_table('E:\大数据\python\ex3.txt', sep='\s+')
print(df6)

# # 跳过某行读取
# df7 = pd.read_csv('E:\大数据\python\csv_mindex.csv' , index_col=['key1' , 'key2'], skiprows=[1, 3])
# print(df7)
print(df6.corr())
style.use('fivethirtyeight')
sns.heatmap(df6)
plt.show()

