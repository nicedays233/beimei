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
df5.join()
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
