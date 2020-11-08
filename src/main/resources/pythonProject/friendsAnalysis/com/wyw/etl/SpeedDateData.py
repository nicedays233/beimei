import pandas as pd
import numpy as np
import sklearn as sl
import matplotlib.pyplot as plt
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import *
from pyspark import SparkContext, SparkConf

spark = SparkSession.builder.master("local").appName("loaddata").getOrCreate()


# 使用SparkSession读取文件
def loadCsv(name):
    user = spark.read.format("csv").option("header", "true").load("E:/大数据/project/%s.csv" % name)
    # event = spark.read.format("csv").option("header","true").load("E:/大数据/project/events.csv/events.csv")
    return user


# users 处理清洗数据
def datePreProcessing(dateDF):
    dateCache = loadCsv(dateDF).cache()
    # dateCache.toPandas().isna().sum()
    dateCache.describe().show()


if __name__ == '__main__':
    datePreProcessing("speed_dating_train")
