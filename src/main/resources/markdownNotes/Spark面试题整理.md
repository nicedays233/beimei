### RDD是什么？

> 弹性分布式数据集

#### 弹性：

- **自动进行存储方式的切换，**RDD优先存储内存中，内存不足将自动写入磁盘

- **基于**Linage**的高效容错机制，**在任何时候都能进行重算，根据数据血统，可以自动从节点失败中恢复分区，各个分片之间的数据互不影响

- **Stage**失败自动重试 / Task**失败自动重试**

- **Checkpoint**和**Persist**，checkpoint持久化到文件系统

#### 分布式：

- 由于数据分布在不同节点，数据计算的工作多节点协同完成

#### 数据集：

- RDD不存储真正的数据，存储对数据的操作
- RDD是只读，还存储分区记录的集合



### RDD有哪些特性？

- 一系列的**分区**信息，每个任务处理一个分区
- 每个分区上都有**compute函数**，计算该分区中的数据
- RDD之间有**一系列的依赖**
- **分区器**决定数据（key-value），分配至哪个分区
- **优先位置列表**，将计算任务分派到其所在处理数据块的存储位置

### 创建RDD有哪些方式？

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

### 何时使用RDD?

在以下情况下，请考虑以下使用RDD的方案或常见用例：

- 您希望对数据集进行**低级转换，操作和控制**；
- 您的数据是**非结构化的，例如媒体流或文本流**；
- 您想使用功能性编程构造而非特定于域的表达式来操纵数据；
- 您不关心在按名称或列处理或访问数据属性时强加诸如列格式之类的模式
- 您可以放弃针对结构化和半结构化数据的DataFrame和Dataset提供的一些优化和性能优势。

### Spark架构核心组件有哪些，分别有什么作用？

|       **术语**       |                          **说  明**                          |
| :------------------: | :----------------------------------------------------------: |
|   **Application**    | **建立在**Spark上的用户程序，包括Driver代码和运行在集群各节点Executor中的代码 |
| **Driver  program**  |   **驱动程序。**Application中的main函数并创建SparkContext    |
| **Cluster  Manager** |  **在集群（**Standalone、Mesos、YARN）上获取资源的外部服务   |
|   **Worker  Node**   |         **集群中任何可以运行**Application代码的节点          |
|     **Executor**     |       **某个**Application运行在worker节点上的一个进程        |
|       **Task**       |              **被送到某个**Executor上的工作单元              |
|       **Job**        | **包含多个**Task组成的并行计算，往往由Spark  Action触发生成，一个Application中往往会产生多个Job |
|      **Stage**       | **每个**Job会被拆分成多组Task，作为一个TaskSet，其名称为Stage |

### Spark运行流程？



### 数据血统有什么好处？

- 优化数据治理，提高数据质量
- Linage**的高效容错机制，**在任何时候都能进行重算，根据数据血统，可以自动从节点失败中恢复分区，各个分片之间的数据互不影响



### Spark内存模型：



### Shuffle形式有几种，都做哪些优化：



### 谓词下推：

### 缓慢变化维：

### 数据治理：

### 数据血缘：

### spark怎么读取文件分片：



### spark-sql优化：



### spark广播机制：



### qarquet与orc文件的区别：



### spark分布式数据的容错机制：