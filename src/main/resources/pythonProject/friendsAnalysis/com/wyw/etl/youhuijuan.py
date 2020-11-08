import pandas as pd
import numpy as np
import sklearn as sl
import matplotlib.pyplot as plt
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import *
from pyspark import SparkContext , SparkConf

spark = SparkSession.Builder\
    .appName("wyw")\
    .master("local[*]")\
    .getOrCreate()
onlineTrain = spark.read.format("csv").option("header", "true").load("E:/天池/新人优惠卷/ccf_online_stage1_train.csv")
