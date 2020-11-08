## Spark Shuffle(二)：shuffle read和write框架设计与实现

### shuffle write：

> write阶段有分区，聚合，排序三个功能，但不一定都要实现
>
> map()->数据聚合->排序->分区

#### write的三种情况：

##### map端要分区，不聚合，不排序



##### map端要分区，不聚合，要排序

##### 

##### map端要分区，要聚合，不排序





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