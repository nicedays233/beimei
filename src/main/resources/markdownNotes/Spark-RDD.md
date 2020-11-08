## Spark-RDD--DataSet--DataFrame：

### 一：RDD

> Spark核心，主要数据抽象，数据项拆分为多个分区（多行数据的集合）的集合的描述

>用于数据转换的接口，指向了存储在HDFS，Cassandra，HBase等，或在故障或缓存收回时重新计算其他RDD分区中的数据。

### 二：RDD是弹性分布式数据集（resilient distributed datasets）

- 分布式数据集
  - RDD是只读的，分区记录的集合，每个分区**分布在集群的不同节点上**，指针指向对应节点的分区
  - RDD并不存储真正的数据，**只是对数据的操作的描述**
- 弹性
  - RDD默认存放在内存中，当内存不足，spark自动将RDD写入磁盘
- 容错性
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

### 六：何时使用RDD？

在以下情况下，请考虑以下使用RDD的方案或常见用例：

- 您希望对数据集进行**低级转换，操作和控制**；
- 您的数据是**非结构化的，例如媒体流或文本流**；
- 您想使用功能性编程构造而非特定于域的表达式来操纵数据；
- 您不关心在按名称或列处理或访问数据属性时强加诸如列格式之类的模式
- 您可以放弃针对结构化和半结构化数据的DataFrame和Dataset提供的一些优化和性能优势。



