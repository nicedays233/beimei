> **写在前面：** 我是`「nicedays」`，一枚喜爱**做特效，听音乐，分享技术**的`大数据开发猿`。这名字是来自**world order**乐队的一首`HAVE A NICE DAY`。如今，走到现在很多坎坷和不顺，如今终于明白**nice day**是需要自己赋予的。
> **白驹过隙，时光荏苒，珍惜当下**~~
> 写博客一方面是对自己学习的一点点`总结及记录`，另一方面则是希望能够帮助更多对大数据感兴趣的朋友。如果你也对 `大数据与机器学习 `感兴趣，可以关注我的**动态** `https://blog.csdn.net/qq_35050438`，让我们一起挖掘数据与人工智能的价值~




## Spark-RDD--DataSet--DataFrame：

### 一：RDD

> Spark核心，主要数据抽象，数据项拆分为多个分区（多行数据的集合）的集合的描述

>用于数据转换的接口，指向了存储在HDFS，Cassandra，HBase等，或在故障或缓存收回时重新计算其他RDD分区中的数据。

### 二：RDD是弹性分布式数据集（resilient distributed datasets）

- `分布式数据集`
  - RDD是只读的，分区记录的集合，每个分区**分布在集群的不同节点上**，指针指向对应节点的分区
  - RDD并不存储真正的数据，**只是对数据的操作的描述**
- `弹性`
  - RDD默认存放在内存中，当内存不足，spark自动将RDD写入磁盘
- `容错性`
  - 根据数据血统，可以自动从节点失败中恢复分区

### 三：RDD与DAG：

- 两者为Spark提供的核心抽象
- DAG反映了RDD之间的依赖关系

### 四：RDD的五大特性：

- 一系列的**分区**信息，每个任务处理一个分区
- 每个分区上都有**compute函数**，计算该分区中的数据
- RDD之间有**一系列的依赖**
- **分区器**决定数据（key-value），分配至哪个分区
- **优先位置列表**，将计算任务分派到其所在处理数据块的存储位置

### 五：RDD创建：

#### （1）：从DataFrame，DataSet中转RDD：

> DataFrame或DataSet类型调用rdd方法即可

#### （2）：从本地集合创建RDD：

> makeRDD方式：底层调用了parallelize方法,并重载了另一个方法：多提供了数据位置信息

```js
val conf = new SparkConf().setAppName("test").setMaster("local[2]")
val sc = SparkContext.getOrCreate(conf)
val value1: RDD[Int] = sc.makeRDD(List(1,3,6),3)
```

> parallelize方式

```js
val spark = SparkSession.builder.appName("xxx").master("local[2]").getOrCreate
val words = spark.sparkContext.parallelize(List(1,2,3,4),5)
```

> makeRDD函数比parallelize函数多提供了数据的位置信息。

#### （3）：从数据源创建：

```js
val spark = SparkSession.builder.appName("xxx").master("local[2]").getOrCreate
spark.sparkContext.textFile("/xx/xxx")
```

> 当文件属于半结构化，结构化数据时，由于RDD属于底层API，没有之后的DataFrameAPI方便，所以读取数据处理数据最好的方式时DataFrameAPI，RDD适合读取图像流，文本流之类。

### 六：相互转换

#### RDD转DataSet和DataFrame

- 导入隐式转换包

```js
import spark.implicit._
```

这个类里有toDF和toDS方法

```js
package org.apache.spark.sql
@org.apache.spark.annotation.InterfaceStability.Stable
case class DatasetHolder[T] private[sql] (private val ds : org.apache.spark.sql.Dataset[T]) extends scala.AnyRef with scala.Product with scala.Serializable {
  def toDS() : org.apache.spark.sql.Dataset[T] = { /* compiled code */ }
  def toDF() : org.apache.spark.sql.DataFrame = { /* compiled code */ }
  def toDF(colNames : scala.Predef.String*) : org.apache.spark.sql.DataFrame = { /* compiled code */ }
}
```

导包之后直接使用方法

```js
rdd.toDF()
rdd.toDS()
```



#### Dataset和DataFrame转RDD

```js
dataframe.rdd
dataset.rdd
```



### 七：何时使用RDD？
> Spark开源作者对此有自己的解释：
> https://databricks.com/blog/2016/07/14/a-tale-of-three-apache-spark-apis-rdds-dataframes-and-datasets.html
#### When to use RDDs?

Consider these scenarios or common use cases for using RDDs when:

- you want low-level transformation and actions and control on your dataset;
- your data is unstructured, such as media streams or streams of text;
- you want to manipulate your data with functional programming constructs than domain specific expressions;
- you don’t care about imposing a schema, such as columnar format, while processing or accessing data attributes by name or column; and
- you can forgo some optimization and performance benefits available with DataFrames and Datasets for structured and semi-structured data.

>翻译：
- 您希望对数据集进行**低级转换，操作和控制**；
- 您的数据是**非结构化的，例如媒体流或文本流**；
- 您想使用功能性编程构造而非特定于域的表达式来操纵数据；
- 您不关心在按名称或**列处理或访问数据属性**时强加诸如列格式之类的模式
- 您可以放弃针对结构化和半结构化数据的DataFrame和Dataset提供的一些优化和性能优势。