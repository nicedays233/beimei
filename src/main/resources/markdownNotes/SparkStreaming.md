## SparkStreaming：

### SparkStreaming架构和工作原理：

![image-20200810143127495](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200810143127495.png)

### SparkStreaming内部工作流程：

- **微批处理：输入->分批处理 -> 结果集**
  - 以离散流的形式传入数据（DStream：Discretized Streams）
  - **流**被分成微批次**(1-10s)**，每一个**微批都是一个RDD**



### StreamingContext：

> Spark Streaming流处理入口

#### 创建StreamingContext： 

```js
import org.apache.spark._
import org.apache.spark.streaming._
import org.apache.spark.streaming.StreamingContext._
val conf=new SparkConf().setMaster("local[2]").setAppName("kgc streaming demo")
val ssc=new StreamingContext(conf,Seconds(8)) 
```

- 一个JVM只能有一个**StreamingContext**启动
- **StreamingContext**停止后不能再启动

### 离散流 DStreams（Discretized Streams）

- DStream是SparkStreaming提供的基本抽象
- DStream由一系列连续的RDD表示
- DStream中每个RDD包含来自某个间隔（batch interval）的数据
- 应用于DStream上的任何操作都转换为底层RDDs上的操作

### 输入Input DStreams与Receivers（接收器）

> Input DStream是表示**从流媒体源接收的输入数据流的DStream**

- 每个Input DStream（除文件流外）都与一个接收方Receiver对象相关联，接收方接收 来自源的数据并将其存在spark内存。



> TIPS:
>
> - 在本地运行 Spark Streaming 程序时，不要使用“local”或“local[1]”作为主URL。这两种方法都意味着只有一个线程将用于在本地运行任务。如果使用基于接收器的输入 DStream(例如 sockets、Kafka、Flume 等)，那么
>   将使用单个线程来运行接收器。因此，在本地运行时，始终使用“local[n]”作为主 URL，其中要运行 n 个接收方。 
> - 在集群上运行时，分配给 Spark Streaming 应用程序的内核数量必须大于接收器的数量。否则，系统将接收数据，但无法处理它



### 数据源种类：

#### 基础数据源：

- Socket源
- 文件流
- RDD队列

#### 高级数据源：

- Flume源
- Kafka源

#### 自定义数据源：

### DStream API

### 转换操作：

> 与RDD类似，参考RDD的算子即可，这里介绍几个特殊的

#### `updateStateByKey(func)：`处理有状态流

> 返回一个新的“状态”DStream，其中通过对键的前一个状态和键的新值应用给定的函数来更新每个键的状态。这可以用来维护每个键的任意状态数据。 

**必须执行的两个步骤：**

1. 定义状态——状态可以是任意的数据类型。 
2. 定义状态更新函数——使用一个函数指定如何使用输入流中的前一个
   状态和新值来更新状态。 在每个批处理中，Spark 将对所有现有 keys 应用状态更新功能，而不管它们在批处理中是否有新数据。如果更新函数返回 None，则键值对将被删除。 

```js
  //TODO 创建一个spark streamingContext
    val conf = new SparkConf().setMaster("local[*]").setAppName("up")
    val ssc = new StreamingContext(conf, Seconds(5))

    //TODO 创建一个inputStream
    val input = ssc.socketTextStream("niceday", 5678)  
    //TODO 创建一个checkpoint
    ssc.checkpoint("e:\\大数据\\mykafka-log")

	// TODO 使用updateStateByKey
    // 写有状态处理方法
    // 处理(hello,1)  (word, 2)拿到hello等等相同key的value，进行一段操作
    // 因为可能有多个key相同2，所以是seq序列
    def updateFunc(currentValue: Seq[Int], preValue: Option[Int]) = {
      val cursum = currentValue.sum
      val pre = preValue.getOrElse(0)
      Some(cursum + pre)
    }
    


    // transforms本质就是将Dstream进行转换操作
    val res: DStream[(String, Int)] = input.transform{_.flatMap(_.split(" ")).map((_, 1))}
    val value = res.updateStateByKey(updateFunc)

    ssc.start()
    ssc.awaitTermination()
```

#### Windows窗口计算流

![image-20200822235106250](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200822235106250.png)

窗口实现了，将多个RDD也就是说多个批处理操作合并成一个打的批处理场景，进行操作，并且可以下一次的批处理操作可以设定步长，两个批处理之间可以有重复的RDD被操作。因此要设两个参数

-  窗口长度—窗口的持续时间
- 滑动间隔—窗口操作执行的间隔

这个参数一定要是单个批处理的时间间隔的倍数，

这其实很好理解，单个批处理的时间间隔是最小单位，不可分割的原子，因此不能只移动半个间隔，同时也不能只含阔半个间隔。

### 输出Output：

- `print()`

- `saveAsTextFile(prefix,[suffix])`

  > 将 DStream 的内容保存为文本文件。每
  > 个批处理间隔的文件名是根据前缀和后缀“prefix-TIME_IN_MS[.suffix]”生成的

- `saveAsObjectFiles(prefix,[suffix])`

  > 将这个 DStream 的内容保存为序列化的 Java 对象的序列文件

- `saveAsHadoopFiles(prefix,[suffix])`

  > 将 DStream 的内容保存为 Hadoop 文件

- `foreachRDD(func)`

  - 接收一个函数，并将函数作用于DStream每个RDD上
  - 函数再Driver节点中执行



### SparkStreaming写数据到kafka:



### SparkStreaming窗口：

#### 简单示例：

- 单词统计---基于TCPSocket接收文本数据

```shell
nc -lk 9999 #数据服务器。当ssc启动后输入测试数据
```

```js
import org.apache.spark._
import org.apache.spark.streaming._
import org.apache.spark.streaming.StreamingContext._
val sparkConf = new SparkConf().setMaster("local[2]").setAppName("NetworkWordCount")
val ssc = new StreamingContext(sparkConf, Seconds(1))
val lines = ssc.socketTextStream("localhost", 9999)//指定数据源
val words = lines.flatMap(_.split(" "))
val wordCounts = words.map(x => (x, 1)).reduceByKey(_ + _)
wordCounts.print()
ssc.start()
// 等待处理结果
ssc.awaitTermination()
```

###                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                