##  HBase物理架构：

![image-20200626211040297](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200626211040297.png)

### HMaster：

#### HMaster的主要作用：--负责table和region管理工作

- `分发Region`--区

  每一个Region会有设定大小，当超过设定的上限，我们需要多个Region,

  其次，HBase系统会将这些Region尽量均衡地分发给这些“从机（Slaver）”，让集群中每台从机都干同样多同样重的活。这可以说是HMaster的首要任务。

- `监控HRegionServer`

  - **负责HRegionServer的故障转移：**

  HRegionServer会**定期地向HMaster发送心跳报告**。当**HMaster收不到HRegionServer的消息时**，就认为该HRegionServer已经失去作用了。这个时候HMaster就得下达指令，将原本在HRegionServer上的数据迁移到其它正常工作的机器上去。

  到这里你肯定会有个疑问：根据前面讲到的判断**HRegionServer故障的方式**来看，这个时候HMaster已经不能够和该**HRegionServer通信**了，那你是怎么下达指令，让原本在**这台HRegionServer**上的数据进行迁移的呢？这个问题，这里暂且不讲，我们只要知道，它能够做到就是了。刚开始接触，不要一下子灌输太多概念，很容易乱的。HDFS的好处在这就体现出来了。

  - **负责HRegionServer的负载均衡**

  当HBase系统中某台机器上的某个Region的大小超过上限时，它会被RegionServer切割成两半，切割后多出来的一个Region又会由HMaster根据集群的情况来做负载均衡，其目的就是尽可能地让每台从机干同样多同样重的活。这里还有一个：RegionServer中由“小合并”“大合并”生成的Region也会需要HMaster来做负载均衡。

  那这里又有一个新的疑问：HMaster是如何得知HRegionServer是忙还是闲的呢？ HRegionServer会定期向HMaster发送一份自己的运行报告，类似于企业当中各部门领导定期向老板递交工作报告一样。然后HMaster就汇总这些运行报告并分析从而作出决策并最终下达指令。

- `管理元数据`

  在HBase中有一个由系统创建的表： hbase:meta 。这里我们姑且称它为“元数据表”。那这个“元数据表”是干什么用的呢？

  原来啊，在HBase中，所有的数据都是以“表”的形式来管理的。而当你的表增长到一定程度的时候，它会影响到你CRUD的效率。举个粟子，假设你的某张表A里有1亿条数据，现在你要查询其中一条数据。又假设你又有一张表B里面有1000条数据，同样你要查询其中一条数据，你说A和B哪个检索速度快？因此，当你的表增长到一定程度时，HMaster就会把这个表切割成几块，假设有一张表共有1000行，HMaster把它分割成两块T1和T2，T1的数据范围从第0行到第499行。T2的数据范围从第500行到第999行。不同的块根据负载均衡存储在不同的HRegionServer中。然后你要查询某一条数据的话，就首先确定你这条数据是坐落在哪一个“块”当中的，确定好后直接去这个“块”当中查询，这样检索速度就快很多了。那么，这些不同的“块”被分别存储到哪个HRegionServer中呢？这些不同的“块”又是包含了哪些范围的数据呢？这些信息就是记载在这个 hbase:meta 也就是“元数据”表中的了。一句大白话总结：**元数据表是负责记载你想要查询的数据是在哪台HRegionServer上保存着的信息的**。

  那话说回来，HMaster对于“元数据表”的管理方式，就是负责更新这个表中的数据内容的咯，换句话说就是如果HMaster挂掉了，那这个hbase:meta的数据就停止更新了。

  

###  HRegionServer：（并发量5M）

![img](https://img2018.cnblogs.com/blog/1146198/201812/1146198-20181214103340382-596022782.png)



#### 1.HLog ----简直和NN的editlog还有mysql的log文件一毛一样

>  一个HRegionServer中就只有一个HLog。

HLog它是采用一种叫做`预写日志`（write-ahead logging，简称WAL）的方式来记录数据的日志文件。**数据在这个日志文件里起到一个备份的作用，它是用来作容灾的。HLog也是存储在HDFS上的**。

当Client想要写数据到HBase数据库中时，数据首先会写到这个HLog中。当数据在HLog中成功保存以后就会告诉客户端：我已经成功保存好你要我保存的数据了。随后进行下一步的保存操作。需要注意的是，数据成功保存进HLog中以后，仅仅完成了HBase数据存储的三分之一而已。但在这里，不讲这么多。

 

#### 2.HRegion

> 一个HRegionServer中有**0 ~ n个HRegion**。

`Region概念：`

- Region是HBase**数据存储和管理的基本单位**。
- 一个表中可以包含**一个或多个Region**。
- 每个Region只能被**一个RS（RegionServer）提供服务**，RS可以同时服务多个Region，来自不同RS上的Region组合成表格的整体逻辑视图。

`Region组成：`

![img](https://img2018.cnblogs.com/blog/666745/201809/666745-20180914233752662-2123317375.png)

- **HRegion：** 一个Region可以包含多个`Store`；
- **Store：** 每个Store包含一个`Memstore`和若干个`StoreFile`；
- **StoreFile：** 表数据真实存储的地方，`HFile是表数据在HDFS上的文件格式`。

`如何找到Region定位流程：`

> B+树定位，通过ZooKeeper 来查找 -ROOT-，然后是.META.，然后找到Table里的Region





。HRegionServer在收到数据存储的请求以后，首先会将这些要被存储的数据写到HLog中。当HLog中写成功以后，。其实这种方式优点还是很明显的，既以提升“Client的响应”速度，又能减少IO操作，在数据存储中，减少IO就意味着延长存储介质的寿命，存储介质寿命延长了更意味着企业能降低运维成本。厉害了。。。

#### 3.Store--一个Store代表一个列簇

> 每一个HRegion内部又维护着0 ~ n个Store

![image-20200626204409158](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200626204409158.png)

#### 4.StoreFile--一个列簇得一部分数据

> Store内部又维护着一个MemStore和0 ~ n个HFile，最终存储数据用的在HDFS之上的真实文件

![image-20200626204647494](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200626204647494.png)

这个MemStore是一段**内存空间**。而这个StoreFile就是HFile，再将这些数据写到MemStore中。而MemStore由于是内存，你往内存中写数据那速度就快了，在往内存中也写成功以后呢，HRegionServer就要向Client返回一个“我已经把你要我保存的数据保存起来了”的信号了。但是实际上HRegionServer在“骗”你。这个时候你如果到HDFS的后台上去看，你根本找不到你要保存的那段数据的文件。换句话说，HBase之所以要管理起大数据来速度这么快，很大一部分功劳在于它是一个很“狡猾的骗子”。HRegionServer啊，只有在MemStore中存储的数据达到一定的量以后，才会一次性的将这些数据输出到HFile中。

#### 5.blockcache

- 读缓存，数据被读取之后仍然缓存在内存中
- 有LruBlockCache（效率较高，GC压力大）和BucketCache（效率较低，没有GC压力）两种BlockCache，默认为LruBlockCache
- 每个RegionServer中只有一个BlockCache实例


## HBase物理架构工作流程：

### 一：读操作：

![image-20200626205353475](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200626205353475.png)

**第一步：** client通过zookeeper的调度，通过**读取zk的-root表**，确定**meta表的region位置**，再通过读取meta表，读取用户表的region位置信息。

**第二步：** 根据namespace、**表名和rowkey在meta表中找到对应的region信息后**，通过region位置信息找到相应的RegionServer，通过RegionServer找到相应的数据存放的Region，并读取数据。

**第三步：** Regionserver的内存分为**MemStore和BlockCache**两部分，MemStore主要用于写数据，BlockCache主要用于读数据。读请求先到MemStore中查数据，查不到就到BlockCache中查，再查不到就会到StoreFile上读，并把读的结果放入BlockCache。

---

### 二：写操作

**第一步：** client通过zookeeper的调度，通过**读取zk的-root表**，确定**meta表的region位置**，再通过读取meta表，读取用户表的region位置信息。

**第二步：** 根据namespace、**表名和rowkey在meta表中找到对应的region信息后**，通过region位置信息找到相应的RegionServer，并将对应的数据发送到该Regionserver检查操作，看Region是不是只读状态，BlockMemorySize大小限制等。

**第三步：** 数据先写入hlog，然后**写入memstore**，知道memstore **到达一定的阈值**，memstore到达阈值后，会**创建一个新的memstore**，并将老的添加到flush队列，由**单独的线程flush到磁盘**上，成为一个**storeFile**。

> PS:当得到了需要访问的Regionserver之后，Client，会向对应的Regionserver发起写请求，
> 数据写入流程，依次将数据写入MemoryStore 和HLog，在写入MemoryStore 和HLog的过程时，需要获取相关的锁，而且写入MemoryStore 和HLog是原子性的，要么都成功，要么都失败。

> 与此同时，zookeeper会记录一个checkpoint点，表示这个时间之前的数据已经持久化了，到系统故障导致memstore丢失的时候，可以通过hlog进行数据的恢复。

**第四步：** 随着storeFile的不断增多，当其数量达到一定的阈值之后，会触发Compact操作，**将多个StoreFile合并成一个**，对同一个key的修改合并到一起，同时对版本进行合并删除。
通过不断合并，当StoreFile到达一定大小的时候，会触发Split操作，把当前Region的文件，分成两个文件，放到相应的Region，此时父Region会下线。这样使得原先1个Region的压力得以分流到2个Region上。







---

### 细节扩展：

#### 一：为什么Client只需要知道Zookeeper地址就可以了呢？

> HMaster启动的时候，会把Meta信息表加载到zookeeper。
> Meta信息表存储了HBase所有的表，所有的Region的详细的信息，比如Region开始的key，结束的key，所在Regionserver的地址。Meta信息表就相当于一个目录，通过它，可以快速定位到数据的实际位置，所以读写数据，只需要跟Zookeeper对应的Regionserver进行交互就可以了。HMaster只需要存储Region和表的元数据信息，协调各个Regionserver，所以他的负载就小了很多。

#### 二：HBase三大模块如何一起协作的。(HMaster,RegionServer,Zookeeper)

通过三个问题解释

`1.当HBase启动的时候发生了什么？`

> HMaster启动的时候会连接zookeeper，将自己注册到Zookeeper，首先将自己注册到Backup Master上，因为可能会有很多的节点抢占Master，最终的Active Master要看他们抢占锁的速度。
> 将会把自己从Backup Master删除，成为Active Master之后，才会去实例化一些类，比如Master Filesytem，table state manager。

> 当一个节点成为Active Master之后，他就会等待Regionserver汇报。
> 首先Regionserver注册Zookeeper，之后向HMaster汇报。HMaster现在手里就有一份关于Regionserver状态的清单，对各个Regionserver（包括失效的）的数据进行整理，
> 最后HMaster整理出了一张Meta表，这张表中记录了，所有表相关的Region，还有各个Regionserver到底负责哪些数据等等。然后将这张表，交给Zookeeper。
> 之后的读写请求，都只需要经过Zookeeper就行了。

> Backup Master 会定期同步 Active Master信息，保证信息是最新的。

`2.如果Regionserver失效了，会发生什么？`

> 如果某一个Regionserver挂了，HMaster会把该Regionserver删除，之后将Regionserver存储的数据，分配给其他的Regionserver，将更新之后meta表，交给Zookeeper
> 所以当某一个Regionserver失效了，并不会对系统稳定性产生任何影响。

`3.当HMaster失效后会发生什么？`

> 如果Active 的HMaster出现故障,处于Backup状态的其他HMaster节点会推选出一个转为Active状态。当之前出现故障的HMaster从故障中恢复，他也只能成为Backup HMaster，等待当前Active HMaster失效了，他才有机会重新成为Active HMaster

> 对于HA高可用集群，当Active状态的HMaster失效，会有处于Backup 的HMaster可以顶上去，集群可以继续正常运行。

> 如果没有配置HA，那么对于客户端的新建表，修改表结构等需求，因为新建表，修改表结构，需要HMaster来执行，会涉及meta表更新。那么 会抛出一个HMaster 不可用的异常，但是不会影响客户端正常的读写数据请求。

#### 三：为什么需要合并Region?

> 那为什么需要合并Region呢？这个需要从Region的Split来说。当一个Region被不断的写数据，达到Region的Split的阀值时（由属性hbase.hregion.max.filesize来决定，默认是10GB），该Region就会被Split成2个新的Region。随着业务数据量的不断增加，Region不断的执行Split，那么Region的个数也会越来越多。

> 一个业务表的Region越多，在进行读写操作时，或是对该表执行Compaction操作时，此时集群的压力是很大的。这里笔者做过一个线上统计，在一个业务表的Region个数达到9000+时，每次对该表进行Compaction操作时，集群的负载便会加重。而间接的也会影响应用程序的读写，一个表的Region过大，势必整个集群的Region个数也会增加，负载均衡后，每个RegionServer承担的Region个数也会增加。

> 因此，这种情况是很有必要的进行Region合并的。比如，当前Region进行Split的阀值设置为30GB，那么我们可以对小于等于10GB的Region进行一次合并，减少每个业务表的Region，从而降低整个集群的Region，减缓每个RegionServer上的Region压力。

#### 