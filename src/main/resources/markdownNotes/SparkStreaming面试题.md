## Spark Streaming面试题

### Spark Streaming第一次运行不丢失数据

> kafka参数auto.offset.reset 参数设置成earliest从最初偏移量开始消费数据。

### Spark Streaming精准一次消费

1. 手动维护偏移量
2. 处理完业务数据后，再进行提交偏移量操作

> 极端情况下，如在提交偏移量时断网或停电会造成 spark 程序第二次启动时重复消费问题， 所以在涉及到金额或精确性非常高的场景会使用事物保证精准一次消费 

### Spark Streaming 控制每秒消费数据得速度

> 通过spark.streaming.kafka.maxRatePerPartition参数来设置Spark Streaming从kafka分区每秒拉取得条数。

### Spark Streaming 背压机制

> 把spark.streaming.backpressure.enabled 参数设置为true，开启背压机制后Spark Streaming会根据延迟动态去kafka消费数据，上限由spark.streaming.kafka.maxRatePerPartition参数控制，所以两个参数一般会一起使用。

### Spark Streaming 一个stage耗时

> Spark Streaming stage 耗时由最慢得task决定，所以数据倾斜时某个task运行慢会导致整个SparkStreaming都运行非常慢

### Spark Streaming优雅关闭

> 把Spark.streaming.stopGracefullyOnShutdown参数设置成true，Spark会在JVM关闭时正常关闭StreamingContext，而不是立马关闭。

### Spark Streaming默认分区个数

> Spark Streaming默认分区个数与所对接得kafka topic分区个数一致，SparkStreaming里一般不会使用repartition算子增大分区，因为repartition会进行shuffle增加耗时



### SparkStreaming有哪几种方式消费kafka中得数据，他们之间得区别是什么？

#### 一：基于receiver方式：

#### 二：基于Direct方式：

> Spark1.3之后引入

这种方式会周期性得查询kafka，来获得每个topic+partition得最新offset，从而定义每个batch得offset得范围，当处理数据得job启动时，就会使用kafka得简单consumer api来获取kafka指定offset范围得数据。

##### 优点：

- **简化并行读取**

  > 如果要读取多个partition，不需要创建多个输入DStream然后对它们进行union操作，Spark会创建跟Kafka partition 一样多得RDD partition，并且会并行从kafka中读取数据，所以在kafka partition 和RDD partition之间，有一个一对一得映射关系。

- **高性能**

  > 如果要保证零数据丢失，在基于 receiver 的方式中，需要开启 WAL 机制。这种方式其实效率低下，因为数据实际上被复制了两份，Kafka 自己本身就有高可靠的机制，会对数据复制一份，而这里又会复制一份到 WAL 中。而基于 direct 的方式，不依赖Receiver，不需要开启 WAL 机制，只要 Kafka 中作了数据的复制，那么就可以通过 Kafka的副本进行恢复。 

- 一次且仅一次得事务机制

### 简述SparkStreaming窗口函数得原理

> 窗口函数就是在原来定义得**sparkStreaming计算批次大小**得基础上再次进行封装，**每次计算多个批次得数据**，同时还需要传递**一个滑动步长得参数**，用来设置当次计算任务完成之后下一次从什么地方开始计算。

