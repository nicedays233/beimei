from pyspark import SparkContext
from pyspark.sql import SparkSession
if __name__ == '__main__':
    spark = SparkSession.builder.appName("test").master("local[*]").getOrCreate()
    df = spark.read.format("csv").option("header",  "true").load("E:\大数据\project\events.csv")
    df.show(5)
    df1 = spark.read.format("jdbc").options(
        url="jdbc:mysql://192.168.56.101:3306/mydemo?user=root&password=123456",
        dbtable="userinfos"
    ).load()
    df1.show()
