## SparkCore&SQL：

### 一：Spark有几种部署方式？简述一下

- `local：`运行在一台机器上，测试环境用
- `standalone：`构建一个基于Master+ Slaves的资源调度集群，Spark任务提交给Master运行。
- `yarn：`Spark客户端之间连接yarn，不需要额外构建Spark集群，有**yarn-client和yarn-cluster**两种模式，**主要区别在Driver程序的运行节点不同。**
- `Mesos：`国内几乎不用



### 二：Spark提交作业参数

#### 重要参数：

- `executor-cores：`一个excutor使用的内核数，2-5个，一般用4个
- `num-executors：`启动executors数量，默认为2
- `driver-cores：`driver使用内核数，默认为1
- `driver-memory：`driver内存大小，默认为512M

```shell
spark-submit \ 
  --master local[5]  \ 
  --driver-cores 2   \ 
  --driver-memory 8g \ 
  --executor-cores 4 \ 
  --num-executors 10 \ 
  --executor-memory 8g \ 
  --class PackageName.ClassName XXXX.jar \ 
  --name "Spark Job Name" \ 
  InputPath      \ 
  OutputPath 
```

### 三：Spark架构与作业提交流程

#### YarnClient运行模式：

1. spark提交脚本启动运行执行
2. 调用jar包中main方法启动Driver，初始化sc，进行任务切分
3. 向RM申请启动ExecutorLauncher，选择一台节点，让节点的NM启动EL
4. NM启动ExecutorBackend,在EB内创建Executor对象

#### YarnCluster运行模式：

1. spark提交脚本启动运行
2. 内部调用Client类里面main方法并执行
3. 封装好后发送RM的AM的发送指令，
4. 选择一台NM启动AM后，AM的Driver线程执行用户的作业
   - 执行代码
   - 初始化sc
   - 任务切分--向RM申请资源
5. 启动ExecutorBackend
6. 在EB内部创建Executor对象开始分配任务运行

### 四：如何理解Spark中血统概念：

>  宽窄依赖用来**解决数据容错时的高效性**以及**划分任务时候**的两个作用。



### 五：ReduceByKey和GroupByKey的区别：

reducebykey：按key聚合，在shuffle之前有combine操作

groupbykey：按key进行分组，直接进行shuffle(没有聚合的操作)

### 六：Repartition和Coalesce的区别

> repartition是coalesce的shuffle作为true

- 区别

repartition一定会发生shuffle

根据传入的参数判断是否会发生shuffle，

增大partition数量用repartition，减少partition使用coalesce

### 七：cache，persist和checkpoint机制

都是做RDD持久化的

- `cache:`内存，不会截断血缘关系，使用计算过程中的数据缓存。
- `checkpoint：`磁盘，截断血缘关系，在 ck 之前必须没有任何任务提交才会生效，ck 过程会额外提交一次任务。 

### 八：当 Spark 涉及到数据库的操作时，如何减少 Spark 运行中的数据库连接数？ 

> 使用 foreachPartition 代替 foreach，在 foreachPartition 内获取数据库的连接。 

### 九：spark与MaprReduce的不同之处（spark快的原因）：

- spark通过**RDD和DAG图，**有效的表示了数据在计算过程中的一些**有关性和无关性**，spark将数据与数据之间相互独立的关系把其优化成了一个stage做一个**流水线计算**，使得cpu在面对一个并行化操作时，不是漫无目的的去东做执行一个计算，西做执行一个计算，**使得当前存储的数据一定是下一步需要用到的，** 而不会去存一些做了n步之后才用到的数据，同时也是通过RDD和DAG图的宽窄依赖是的它也确定了**数据的shuffle应该出现在它最应该出现shuffle的时候**，spark不存储计算中间结果。

- spark是**多线程模型**，mapreduce是**多进程模型**，多进程每个reduce，maptask都是一个jvm进程，而多线程一个executor才是一个jvm进程，可以运行多个线程，每个线程执行一个task，虽然多进程这样**每个独立的jvm管理一个task**，每个task的任务占用资源可以更好控制，但是**由于每次启动jvm进程都需要重新申请资源**，job任务一多，这个启动时间会非常非常长。

  Spark则是通过**复用线程池中的线程来减少启动**、关闭task所需要的开销。（多线程模型也有缺点，由于同节点上所有任务运行在一个进程中，因此，**会出现严重的资源争用，难以细粒度控制每个任务占用资源**

- sparkshuffle将shuffle过程的聚合和排序的选择与过程进行了优化，需要排序的时候在排序，支持基于hash的分布式聚合，mapreduce排序不可避免。会浪费大量时间



