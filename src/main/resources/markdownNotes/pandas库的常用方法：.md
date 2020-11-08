## pandas库的常用方法：

### Pandas数据结构：

- **series**
  - `value`
  - `index`

- **dataframe**
  - 由多列Series组成

### Series常用方法：

| **方法**        | **说明**                                                     |
| --------------- | ------------------------------------------------------------ |
| iloc(start:end) | 通过index索引截取Series中的数据，不包括end                   |
| head(n)         | 截取Series中的钱n条数据                                      |
| []              | 根据[]中的条件截取Series中的数据                             |
| sort_values()   | 按照Series的值进行排序，默认是升序，设置降序：ascending=False |
| value_counts()  | 用来计算Series里面相同数据出现的频率，生成新的Series         |
| max() /min()    | 返回Series中的最大值和最小值                                 |
| mean()          | 求均值                                                       |
| median()        | 求中位数                                                     |
| std()           | 求标准差                                                     |
| isnull()        | 判断是否为空值                                               |

### DataFrame数据结构：

- 多列Series组成的数据结构
- 每列Series都有一个列名
- 所有列共享索引

### 创建DataFrame方法：

- 用**等长的列表的字典**创建DataFrame对象

```python
data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada', 'Nevada'],
        'year': ['2000', '2001', '2002', '2001', '2002', '2003'],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]}
frame = pd.DataFrame(data)
```



- 用由**字典组成的嵌套字典**创建DataFrame对象
  - 外部字典的键会成为列名
  - 内部嵌套字典的键会成为索引

```python
data = {'state': {'wyw': 'ohio', 'wyw2': 'sss'},
        'year': {'wyw': '2004', 'wyw2': '2003'},
        'pop': {'wyw': 2.4, 'wyw3':  3.2}
       }
frame = pd.DataFrame(data)
```



### 操作DataFrame的常用方法：

| **方法**                   | **说明**                                                     |
| -------------------------- | ------------------------------------------------------------ |
| reset_index()              | 将索引转换成DataFrame的一个列，并重新添加索引，也可用于将Series转化成DataFrame，把Series的索引转化成DataFrame的列 |
| df['col_name']             | 通过列名获取DataFrame中的一列，返回Series对象                |
| df[df['col_name']>n]       | 通过条件筛选符合条件的行，条件为col_name列的值大于n。  可以使用&（且），\|（或）进行复核条件筛选 |
| del df['col_name']         | 删除DataFrame中指定列名的列                                  |
| drop()                     | 删除数据，默认为根据索引删除行数据                           |
| iloc(start:end)            | 通过index索引解决DataFrame中指定区间的列                     |
| isnull()                   | 显示DataFrame中的空值状态，如果存在空值则为True              |
| sort_values(by='col_name') | 按照选择的列的数值进行排列                                   |

```python
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

```



### 使用Pandas加载数据：

- `mysql数据库`

**两种方式读取：**

```python
import pymysql
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
engine = create_engine('mysql+pymysql://root:123456@192.168.56.101:3306/mydemo')
sql = '''select * from full_access_logs; '''
df5 = pd.read_sql_query(sql, engine)

# print(df5)
# 按不同列，不同的聚合方式
print(df5.groupby("event_time").agg({"event_time": np.max,"action_client":np.sum}))

connect = pymysql.Connect(
                host='192.168.56.101',
                port=3306,
                user='root',
                passwd='123456',
                db='mydemo',
                charset='utf8'
                )
sql = pd.read_sql("select * from full_access_logs",connect)
print(sql)
```



- `csv格式文件`

```python
pd.read_csv(file_path)
```

```python
# 读文件含表头
df = pd.read_csv('E:\大数据\python\ex1.csv')
print(df)

df1 = pd.read_table('E:\大数据\python\ex1.csv' , sep=',')
print(df1)

# 读文件不含表头
df2 = pd.read_csv('E:\大数据\python\ex2.csv' , header=None)
print(df2)

df3 = pd.read_csv('E:\大数据\python\ex2.csv' , names=['a' , 'b' , 'c' , 'd' , 'message'])
print(df3)

# 将指定列为索引
df4 = pd.read_csv('E:\大数据\python\ex2.csv' , names=['a' , 'b' , 'c' , 'd' , 'message'] , index_col='message')
print(df4)

# 建立分层索引，就是两层行号
df5 = pd.read_csv('E:\大数据\python\csv_mindex.csv' , index_col=['key1' , 'key2'])
print(df5)

# 其他格式读取
df6 = pd.read_table('E:\大数据\python\ex3.txt', sep='\s+')
print(df6)

# 跳过某行读取
df7 = pd.read_csv('E:\大数据\python\csv_mindex.csv' , index_col=['key1' , 'key2'], skiprows=[1, 3])
print(df7)
```

- `json格式文件`

```python
pd.read_json(file_path)
```



### dataframe行列数

```python
df.shape[0] 行
df.shape[1] 列
```

