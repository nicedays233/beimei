import numpy as np
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql import functions
from pyspark.sql.functions import *
import matplotlib.pyplot as plt
ss = SparkSession.builder.appName("master").master("local[*]").getOrCreate()
pandas_df = pd.read_csv("E:/QQData/741454344/FileRecv/products.csv",  header=None, usecols=[1, 2, 5])
print(pandas_df.head())
spark_df = ss.createDataFrame(pandas_df)
df = spark_df.withColumnRenamed("1", "id")\
    .withColumnRenamed("2", "name")\
    .withColumnRenamed("5", "remark")
rdd = df.select(col("id")).rdd.map(lambda x: x[0])
# 把数据平均分配10个区间【（max-min）/10】
(countries, bins) = rdd.histogram(10)
plt.hist(rdd.collect(), 10)
plt.xlabel("xx")
plt.ylabel("yy")
plt.title("ss")
plt.show()
df.show()
