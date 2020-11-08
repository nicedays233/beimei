import pandas as pd
import numpy as np
import sklearn as sl
import matplotlib.pyplot as plt
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import *
from pyspark import SparkContext , SparkConf

spark = SparkSession.builder.master("local").appName("loaddata").getOrCreate()


# 使用SparkSession读取文件
def loadCsv(name):
    user = spark.read.format("csv").option("header" , "true").load("E:/大数据/project/%s.csv" % name)
    # event = spark.read.format("csv").option("header","true").load("E:/大数据/project/events.csv/events.csv")

    return user


# users 处理清洗数据
def userPreProcessing(userDF):

    uscache = loadCsv(userDF).cache() \
    # 一：查询非正常情况
    # 1.查询空值
    # print(uscache.toPandas().is
    # na().sum())

    # 2.user_id没有重复值
    # print(uscache.count())
    # print(uscache.select(col("user_id")).distinct().count())

    # 3.把birthyear的非正常情况查出 1494个脑瘫
    # uscache\
    #     .filter(~ col("birthyear").rlike("[0-9]{4}"))\
    #     .show()

    # 4.把joinedAt的非正常情况查出
    # uscache\
    #     .exceptAll(uscache.filter(col("joinedAt").rlike("[0-9]{4}-[0-1][0-9]-[0-3]{1,2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}Z")))

    # 二.填充或删除非正常情况
    # 5.寻找国家中最多的城市将空值填充
    hotCity = uscache \
        .filter(col("location").isNotNull() & (trim(col("location")) != '')) \
        .groupBy("locale", "location") \
        .agg(count("location").alias("people")) \
        .withColumnRenamed("location", "loct") \
        .select("locale", "loct",
                row_number().over(Window.partitionBy("locale").orderBy(desc('people'))).alias("rank")).filter("rank=1") \

    avgAge = uscache \
        .groupby(col("location")) \
        .agg(round(mean(col("birthyear"))).alias("avgage")) \
        .withColumnRenamed("location", "city")

    # 国家中最多的城市空值已填充
    # 城市平均生日进行填充空值
    # 空值随机填充男女
    tmp = uscache \
        .join(hotCity, ["locale"]) \
        .select(col("*"), when(col("location").isNull() | trim(col("location")).__eq__(""), col("loct")).otherwise(col("location")).alias("city"))\
        .drop("location", "loct", "joinedAt", "timezone") \
        .join(avgAge, ['city'])\
        .withColumn("ageyear", when(col("birthyear").rlike("[0-9]{4}"), col("birthyear")).otherwise(col("avgage")).alias("biryear")) \
        .drop("avgage", "birthyear") \
        .withColumn("gender", when(col("gender").__eq__("male") | col("gender").__eq__("female"), col("gender"))
                    .otherwise(when(rand() < 0.5, "male").otherwise("female")))

    return tmp


# 处理user_friend
def userFriendPreProcessing(userFndDF):

    ufcache = loadCsv(userFndDF).cache()
    # explode将一行变多行对应friends
    newFriend = ufcache.select("user", explode(split("friends"," ")).alias("friendId"))

    return newFriend


# 处理events
def eventPreProcessing(eventDF):
    eventCache = loadCsv(eventDF).cache()
    # print(eventCache.toPandas().isna().sum())
    # eventCache.filter(col("city").isNotNull()).show()
    tmp = eventCache.select("event_id", "user_id", "start_time")
    return tmp


# 处理event_attendees
def eventAttsPreProcessing(eventAttDF):

    eventAttsCache = loadCsv(eventAttDF).cache()









if __name__ == '__main__':
    # userPreProcessing("users")
    # userFriendProcessing("user_friends")
    # eventPreProcessing("events")
    eventAttsPreProcessing("events_attendees")
