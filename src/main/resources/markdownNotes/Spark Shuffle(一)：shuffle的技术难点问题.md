## Spark Shuffle(一)：shuffle的技术难点问题

### 解决shuffle的分区问题：

> map端write时的数据分区发往reduce的情形

#### 如何确定分区个数？

> 每个map task的输出数据的分区个数可由用户自定义，但一般定义为集群可用cpu的1-2倍。
>
> 相对应reduce stage开启对应数量的task来处理。

#### 如何对map task输出数据进行分区？

> 对每个map task 输出的<k，v>对，根据key值hash（key）%2计算partitionid，不同id不同分区。

### 解决shuffle的数据聚合问题：

> reduce端read拉取map端数据把不同map端相同key值聚合的情形

- 在线聚合法：

  > mapreduce做不到在线聚合，它通常要把key相同的全部放到list后，才能再执行聚合。
  >
  > **spark当从map端拿到的每个record（k，v）记录进入HashMap时，就进行聚合**



### 解决Map端combine问题：

> 提前在map端用hashmap进行聚合，网络发送时，减少网络io

### 解决shuffle的sort问题：

> 首先要明确当数据需要排序时，reduce端一定要排序，writer也就是map端可排可不排，看情况，排了减少reduce端排序复杂度，但是增加计算时间成本。不排刚好相反，依情况而定。

#### map如果需要排序，何时排序？聚合前还是聚合后？

> 由mapreduce可知，它是**先排序再聚合**的，且排序在源码写死，不管如何都必须排序。**好处是**排序完的数据可以直接从前往后聚合，就用不着hashmap了。**缺点是**排序的数据需要大量的连续内存存储，且两个过程无法同时进行。

spark对此进行了优化，是**先聚合后排序**，设计了特殊的HashMap进行聚合，并将record（k，v）引用放入线性数据结构进行排序，灵活性高，**可惜需要复制record的引用，空间占用较大。**

### 解决shuffle内存不足的问题：

> 当数据量大时，这个问题即可能出现在write端，也可能出现在read端。

#### 解决方案：内存+磁盘混合存储

> 先将数据在内存HashMap进行聚合，不断塞入后内存空间不足，将聚合的数据split到磁盘上，空闲的内存处理后面塞入的数据，split到磁盘的数据只是部分聚合，最后要将所有的数据进行全局聚合，要对数据进行排序，减少磁盘I/O                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  

### 根据算子智能判定是否聚合和排序

| 包含shuffle的算子操作                                        | write 端 combine | write 端 sort | read 端 combine | read 端 sort |
| ------------------------------------------------------------ | ---------------- | ------------- | --------------- | ------------ |
| partitionBy()                                                | ×                | ×             | ×               | ×            |
| groupBy(),cogroup(),join(),<br />coalesce(),intersection(),subtract(),<br />subtractByKey() | ×                | ×             | √               | ×            |
| reduceByKey(),aggregateByKey(),<br />combineByKey(),foldByKey(),<br />distinct() | √                | ×             | ×               | ×            |
| sortByKey(),sortBy(),<br />repartitionAndSortWithinPartition() | ×                | ×             | √               | √            |



### 未优化Shuffle--HashShuffleManager：

> 1.2版本以前的默认的shuffle引擎

#### HashShuffleManager机制：

> 前提：假设每个Executor只有一个CPU core，同一时间只能执行一个task线程。

- 普通运行机制

![image-20200826133337965](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200826133337965.png)

`shuffle write阶段`

在一个stage结束计算之后，在下一个stage将要执行shuffle算子（groupByKey等），所以每个task处理的数据按key分区，相同key被写入同一磁盘文件，每一个磁盘文件都**只属于reduce端的stage的一个task**（task比一个磁盘文件的概念要大），写磁盘之前，数据写入内存缓冲，缓冲填满之后，会溢写到磁盘文件。一个task对应一个分区。

>比如下一个stage总共有100个task，那么当前stage的每个task都要创建100份磁盘文件。如果当前stage有50个task，总共有10个Executor，每个Executor执行5个Task，那么每个Executor上总共就要创建500个磁盘文件，所有Executor上会创建5000个磁盘文件

`shuffle read阶段`

>shuffle read的过程中，每个task只要从上游stage的所有task所在节点上，拉取属于自己的那一个磁盘文件即可。

shuffle read一边拉取一边进行聚合的。每个shuffle read task都会有一个自己的buffer缓冲，每次都只能拉取与buffer缓冲相同大小的数据，然后通过内存中的一个Map进行聚合等操作。聚合完一批数据后，再拉取下一批数据，并放到buffer缓冲中进行聚合操作。以此类推，直到最后将所有数据到拉取完，并得到最终的结果。

#### Hash shuffle普通机制的问题

1. Shuffle前在磁盘上会产生海量的小文件，建立通信和拉取数据的次数变多,此时会产生大量耗时低效的 IO 操作 (因為产生过多的小文件)
2. 可能导致OOM，大量耗时低效的 IO 操作 ，导致写磁盘时的对象过多，读磁盘时候的对象也过多，这些对象存储在堆内存中，会导致堆内存不足，相应会导致频繁的GC，GC会导致OOM。由于内存中需要保存海量文件操作句柄和临时信息，如果数据处理的规模比较庞大的话，内存不可承受，会出现 OOM 等问题。

- 合并运行机制

  > 复用buffer来优化shuffle过程中产生的小文件的数量，
  >
  > Hash shuffle是不具有排序的shuffle

  > 开启合并机制的配置是spark.shuffle.consolidateFiles

  ![image-20200826194507684](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200826194507684.png)

  开启consolidate机制之后，shuffle write过程会出现一个shuffleFileGroup概念，第一批cpu并行的100个task对应下一个stage的50task数量每个task各生成50个后，磁盘文件会形成一个shuffleFilegroup，当具有相同key再次溢写时，不会再单独形成一个磁盘文件，会复用之前已有的shuffleFileGroup，大大减少了具有相同key多个磁盘文件的情况。

#### Hash shuffle运行机制的问题

> 如果 Reducer 端的并行任务或者是数据分片过多的话则 Core * Reducer Task 依旧过大，也会产生很多小文件。

### 优化Shuffle--SortShuffleManager：

> 虽然单词有sort，但是在数据量较小时，会启用bypass机制不进行排序

#### SortShuffleManager机制：

- SortS机制

  ![image-20200827191546436](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200827191546436.png)

  ​	`shuffle write`

  - **分区：** 数据将会按key和分区进行排序，若没有合并操作只会根据分区进行排序

  - **排序：** 在溢写前，根据key对内存数据结构已有数据进行排序

  - **溢写：** 

    > 数据在进入下一个stage之前，先写入一个内存数据结构中（5M）,根据不同的shuffle算子，选取不同数据结构，reduceByKey选map，join选Array

    当内存数据结构不够时，进行溢写，然后排序后，分批将数据写入磁盘文件。

  - **合并：** 多次写入内存数据结构的过程中，经常性会造成溢写产生多个临时文件，最后会将这些临时文件通过归并合并写入磁盘文件，最后只会产生一个磁盘文件对应一个task

    `shuffle read`

  - 上一个stage的task会单独写一份**索引文件**，**标识下游各个task数据在文件的startoffset和end offset**

  - readtask运行时对其索引进行拉取

  > **tips:** 
  >
  > shuffle中的定时器：定时器会检查内存数据结构的大小，如果内存数据结构空间不够，那么会申请额外的内存，申请的大小满足如下公式：
  >
  > applyMemory=nowMenory*2-oldMemory
  >
  > **申请的内存=当前的内存情况*2-上一次的内嵌情况**

  

- bypass运行机制

  >适用于没有聚合，数据量不大的场景

  > 当**shuffle read task**的数量小于等于**spark.shuffle.sort.bypassMergeThreshold**参数的值时(默认为200)，就会启用bypass机制。

![image-20200827190705705](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200827190705705.png)

写入磁盘文件是通过 Java的 BufferedOutputStream 实现的，BufferedOutputStream 是 Java 的缓冲输出流，**首先会将数据缓冲在内存中，（io流的内存狠小），当内存缓冲满溢之后再一次写入磁盘文件中**，这样可以减少磁盘 IO 次数，提升性能。

