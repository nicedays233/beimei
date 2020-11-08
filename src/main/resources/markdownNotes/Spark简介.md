## Spark简介：

> spark是一个用来实现快速而通用的集群计算的平台
>
> 主要应用于批处理，迭代算法，交互式查询，流处理。

### 为什么使用Spark？

#### MapReduce编程模型的局限性

- 繁杂
  - 只有Map和Reduce两个操作，复杂的逻辑需要大量的样板代码
- 处理效率低
  - map中间结果写磁盘，Reduce写HDFS，多个Map通过HDFS交换数据
  - 任务调度与启动开销大
- 不适合迭代处理，交互式处理和流式处理

#### Spark是类Hadoop MapReduce的通用并行框架

- Job中间输出结果可以保存在内存，不再需要读写HDFS
- 比mapreduce平均快10倍以上

### Spark技术栈

- **SparkCore**

- **SparkStreaming**

- **SparkSQL**

- **SparkGraphX**

- **SparkMLib**



## Spark架构与运行环境：

### Spark-shell：自带交互

- 本机
  - spark-shell --master local[*]
- standalone
  - spark-shell --master
- YARN

### Spark架构设计：

#### 运行架构

>  sc调sparkcontext

![image-20200721170148919](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200721170148919.png)

- 在驱动程序中，通过SparkContext主导应用的执行
- SparkContext可以连接不同类型的Cluster Manager （Standalone，YARN，Mesos），连接后，获得集群节点上的Executor
- 一个worker节点默认一个Executor，可通过spark_worker_instances调整
- 每个应用获取自己的excutor
- 一个excutor有多个task，几核就同时处理几个task，每个task处理一个RDD分区

#### Spark架构核心组件：

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

### SparkAPI

#### SparkContext

- 连接Driver与Spark Cluster
- Spark主入口
- 每个JVM仅能有一个活跃的SparkContext
- SparkContext.getOrCreate

`创建一个SparkContext对象`

```js
//Spark app 配置：应用的名字和Master运行的位置
val sparkConf=new SparkConf().setAppName("SparkAppTemplate").setMaster("local[2]")
    //创建sparkContext对象：主要用于读取需要处理的数据，封装在RDD集合中；调度jobs执行
val sc = new SparkContext(sparkConf) 
```



#### SparkSession

![image-20200722084225662](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200722084225662.png)

> SparkSession是2.0引入的概念，目的是将不同Context结合起来.

早期由于RDD是主要的API，我们通过创建SparkContext来创建和操作RDD。

而对于其他的API，我们使用不同的context，例如Steaming，我们用StreamingContext，sql我们用sqlContext。

**但之后随者DataSet和DataFrame的API成为主流，我们需要引入SparkSession，来封装SparkConf，SparkContext和sqlContext，HiveContext。**

```js
//在spark 2.x中不推荐使用sparkContext对象读取数据，而是推荐SparkSession
    val spark = SparkSession.builder
      .appName("Simple Application")
      .master("local[2]")
      .getOrCreate()
```



#### RDD

> Spark核心，主要数据抽象，数据项拆分为多个分区（多行数据的集合）的集合的描述

>用于数据转换的接口，指向了存储在HDFS，Cassandra，HBase等，或在故障或缓存收回时重新计算其他RDD分区中的数据。

##### RDD是弹性分布式数据集（resilient distributed datasets）

- 分布式数据集
  - RDD是只读的，分区记录的集合，每个分区**分布在集群的不同节点上**，指针指向对应节点的分区
  - RDD并不存储真正的数据，**只是对数据的操作的描述**
- 弹性
  - RDD默认存放在内存中，当内存不足，spark自动将RDD写入磁盘
- 容错性
  - 根据数据血统，可以自动从节点失败中恢复分区

##### RDD与DAG：

- 两者为Spark提供的核心抽象
- DAG反映了RDD之间的依赖关系

##### RDD的特性：

- 一系列的**分区**信息，每个任务处理一个分区
- 每个分区上都有**compute函数**，计算该分区中的数据
- RDD之间有**一系列的依赖**
- **分区器**决定数据（key-value），分配至哪个分区
- **优先位置列表**，将计算任务分派到其所在处理数据块的存储位置

#### DataSet

> 特定领域对象中的强类型集合，它可以使用函数并行的进行转换操作

#### DataFrame

> 最常见的结构化API，包含行和列的数据表，特殊的DataSet

模式（schema）：说明这些列和列类型的一些规则

分布式dataFrame，这种数据集是 **以RDD为基础的**，其被组织成指定的列，**类似于关系数据库的二维表格**



## Spark安装教程：

### 单机版：

#### 第一步：前置安装JDK(Spark 不一定依靠Hadoop)

#### 第二步：下载spark-2.3.4-bin-hadoop2.6.tgz 解压

```shell
tar -zxvf spark-2.3.4-bin-hadoop2.6.tgz
mv /opt/spark-2.3.4-bin-hadoop2.6 /opt/soft/spark234
```

#### 第三步：在conf修改spark-env.sh

```shell
vi /opt/soft/spark234/conf/spark-env.sh
```

- 末尾添加

```shell
export SPARK_MASTER_HOST=192.168.56.101 #主节点IP
export SPARK_MASTER_PORT=7077 #任务提交端口
export SPARK_WORKER_CORES=2 #每个worker使用2核
export SPARK_WORKER_MEMORY=3g #每个worker使用3g内存
export SPARK_MASTER_WEBUI_PORT=8888 #修改spark监视窗口的端口默认8080

```

#### 第四步：修改sbin目录下spark-config.sh

```shell
vi /opt/soft/spark234/sbin/sprak-config.sh
```

```shell
export JAVA_HOME=/opt/soft2/jdk180/jdk1.8.0_111
```

#### 第五步：开启spark

- 先在sbin目录下开启master和worker进程

```shell
vi /opt/soft/spark234/sbin
./start-all.sh
```

- 去bin目录开启黑窗口进入spark界面

```shell
vi /opt/soft/spark234/bin
./spark-shell
```

![image-20200725165025952](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200725165025952.png)



### 分布式版：

#### 第一步：前置安装JDK(Spark 不一定依靠Hadoop)

#### 第二步：下载spark-2.3.4-bin-hadoop2.6.tgz 解压，

```shell
tar -zxvf spark-2.3.4-bin-hadoop2.6.tgz
mv /opt/spark-2.3.4-bin-hadoop2.6 /opt/soft/spark234
```

#### 第三步：在conf修改spark-env.sh和slaves

`修改slaves`

```shell
cd /opt/soft/spark234/conf/

cp slaves.template slaves

vi /opt/soft/spark234/conf/slaves
```

- 给每个节点添加从节点的IP

![image-20200725165447354](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200725165447354.png)

`修改spark-env.sh`

```shell
cd /opt/soft/spark234/conf/

cp spark-env.sh.template spark-env.sh

vi /opt/soft/spark234/conf/spark-env.sh
```

- 末尾添加

```shell
export SPARK_MASTER_HOST=192.168.56.101 #主节点IP
export SPARK_MASTER_PORT=7077 #任务提交端口
export SPARK_WORKER_CORES=2 #每个worker使用2核
export SPARK_WORKER_MEMORY=3g #每个worker使用3g内存
export SPARK_MASTER_WEBUI_PORT=8888 #修改spark监视窗口的端口默认8080

```

#### 第四步：修改sbin目录下spark-config.sh

```shell
vi /opt/soft/spark234/sbin/sprak-config.sh
```

```shell
export JAVA_HOME=/opt/soft2/jdk180/jdk1.8.0_111
```

#### 第五步：把主节点配置好的spark发布到从节点上，开启spark

- 先在sbin目录下开启master和worker进程

```shell
cd /opt/soft/spark234/sbin
./start-all.sh
```

- 去bin目录开启黑窗口进入spark界面

```shell
cd /opt/soft/spark234/bin
./spark-shell
```

![image-20200725165025952](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200725165025952.png)

