import pymysql
from sqlalchemy import create_engine
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql import functions
from pyspark.sql.functions import *
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# ss = SparkSession.builder.appName("master").master("local[*]").getOrCreate()
engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/label')
sql = '''select * from ip_segment; '''
pds = pd.read_sql_query(sql, engine)
pds["address"] = pds["endbigint"] - pds["startbigint"]
plt.figure(figsize=(10, 10), dpi=150)
# ax = sns.kdeplot(pds["address"], color="Red", shade=True)
pdss = pds[pds["address"] == 0]
print(pdss)
# ax = sns.distplot(pds["address"])
# plt.show()
# print(pds["address"])
# df = ss.createDataFrame(pds)
# df.show(20)

# print(df5)
# 按不同列，不同的聚合方式
# print(df5.groupby("event_time").agg({"event_time": np.max,"action_client":np.sum}))

# print(df5.select("startbigint" - "endbigint"))
# connect = pymysql.Connect(
#                 host='',
#                 port=3306,
#                 user='root',
#                 passwd='123456',
#                 db='mydemo',
#                 charset='utf8'
#                 )
# sql = pd.read_sql("select * from full_access_logs",connect)
# print(sql)
