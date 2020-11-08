## Hadoop---MapReduce---

#### 大数据4V特征：

- **Volume：**90%的数据是过去两年产生----**大数据量**
- **Velocity：**数据增长速度快，时效性高----**速度快**
- **Variety：**数据种类和来源多样化：结构化数据，半结构化数据，非结构化数据----**多样化**
- **Value：**需挖掘获取数据价值----**价值密度低**

![image-20200629084839027](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200629084839027.png)



![image-20200629085256096](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200629085256096.png)

大数据的两个天生的特性：时间戳和不可修改性



hadoop多节点处理数据不是将数据从各个服务器去拉取处理数据，而是将代码发送到各个服务器上进行处理。完成了并行工作

#### Hadoop三大核心：

- **HDFS：**Hadoop Distributed File System 分布式存储系统
  - 提供高可靠性，高扩展性和高吞吐率的数据存储服务

- **YARN：**Yet Another Resource Negotiator资源管理调度系统，负责集群资源的管理和调度
- **MapReduce：**分布式运算框架

#### Hadoop4大特征：

- 扩容能力：可靠存储和处理千兆字节（PB）数据
- 成本低：用普通机器组成得服务器群来分发以处理数据，可达数千节点。
- 高效率：通过分发数据，Hadoop可以并行处理
- 可靠性：Hadoop自动维护数据多份副本，失败任务自动重新部署计算任务。

|          | RDBMS                                  | Hadoop                             |
| -------- | -------------------------------------- | ---------------------------------- |
| 格式     | 写数据时要求                           | 读数据时要求                       |
| 速度     | 读数据速度快                           | 写数据速度快                       |
| 数据监管 | 标准结构化                             | 任意结构数据                       |
| 数据处理 | 有限的处理能力                         | 强大处理能力                       |
| 数据类型 | 结构化数据                             | 结构化，半结构化，非结构化         |
| 应用场景 | 交互式OLAP分析ACID事务处理企业业务系统 | 处理非结构化数据，海量数据存储计算 |



#### HDFS架构：

![image-20200601193516432](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200601193516432.png)

#### HDFS优点：

- 支持处理超大文件
- 可运行廉价机器上
- 高容错性
- 流式文件写入

#### HDFS缺点：----不合适实时

- 不适合低延时数据访问场景
- 不适合小文件存取场景
- 不适合并发写入，文件随机修改场景

错误在logs上找

share ，jar包和帮助文档所在地

tmp/dfs/data 里存有datanode的版本号，uuid来确认时本机的datanode差的

tmp/dfs/name 里存有namenode的版本号，他们的集群id是一样的，还存着fsimage和edit

tmp/dfs/name 里存有secondnamenode的版本号，，还存着fsimage和edit

#### HDFS CLI （命令行）

###### 基本格式：

- ###### hdfs dfs  

- ###### hadoop fs (已过时)

###### 命令：

- -ls
- -cat
- -put
- mkdir
- -text
- -get
- rm /rm-R



##### NameNode:元数据节点（NN）

- 管理文件系统的namespace/元数据
- 一个HDFS集群只有一个**active的NN**

##### DataNode:数据节点（DN）

- 数据存储节点，**保存和检索block**
- 一个集群可以有多个数据节点

##### Secondary NameNode:从元数据节点（SNN）

- 合并Namenode的editlogs到fsimage文件中
- 辅助NN将内存中元数据信息持久化

###### HDFS副本机制

- block数据块128m：

  - HDFS平均寻道时间大概为10ms

  - 大量测试发现寻道时间为传输时间的1%，为最佳状态

  - 目前磁盘传输100MB/s，计算出最佳大小：100MB/s * 1 = 100MB

    再经过cpu读取固定是2的整数次幂，所以我们将块设定为128MB

- 副本数默认为3

- 存放机制：

  - 一个在本地机架节点
  - 一个在同一个机架不同节点
  - 一个在不同机架的节点

###### HDFS高可用：（High Availability）

- 2.x版本
  - 解决：HDFS Federation方式，共享DN资源

说白了就是管理文件的目录

它保存了两个核心的数据结构：Fslmage和EditLog

- FsImage负责维护文件系统树和树中所有文件和文件夹的元数据。------**维护文件结构和文件元信息**
- 操作日志文件EditLog中记录了所有针对文件的创建，删除，重命名操作。------**记录对文件的操作**

![image-20200601231915191](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200601231915191.png)

###### HDFS读文件流程：

读文件流程：

1、首先调用FileSystem.open()方法，获取到DistributedFileSystem实例

2、DistributedFileSystem 向Namenode发起RPC(远程过程调用)请求获得文件的开始部分或全部block列表，对于每个返回的块，都包含块所在的DataNode地址。

   这些DataNode会按照Hadoop定义的集群拓扑结构得出客户端的距离，然后再进行排序。如果客户端本身就是一个DataNode，那么他将从本地读取文件。

3、DistributedFileSystem会向客户端client返回一个支持文件定位的输入流对象FSDataInputStream，用于客户端读取数据。

   FSDataInputStream包含一个DFSInputStream对象，这个对象用来管理DataNode和NameNode之间的I/O

4、客户端调用read()方法，DFSInputStream就会找出离客户端最近的datanode并连接datanode

5、DFSInputStream对象中包含文件开始部分的数据块所在的DataNode地址，首先它会连接包含文件第一个块最近DataNode。随后，在数据流中重复调用read()函数，直到这个块全部读完为止。

###### HDFS写文件流程：

1 Client发起文件上传请求，调用DistributedFileSystem对象的create方法，创建一个文件输出流（FSDataOutputStream）对象

2 通过DistributedFileSystem对象与Hadoop集群的NameNode进行一次RPC远程调用，NameNode检查目标文件是否已存在，父目录是否存在，返回是否可以上传；在HDFS的Namespace中创建一个文件条目（Entry），该条目没有任何的Block

------

3 通过FSDataOutputStream对象，向DataNode写入数据，数据首先被写入FSDataOutputStream对象内部的Buffer中，然后数据被分割成一个个Packet数据包

4 以Packet最小单位（默认64K），基于Socket连接发送到按特定算法选择的HDFS集群中一组DataNode（正常是3个，可能大于等于1）中的一个节点上，在这组DataNode组成的Pipeline上依次传输Packet：client请求3台DataNode中的一台A上传数据（本质上是一个RPC调用，建立pipeline），A收到请求会继续调用B，然后B调用C，将整个pipeline建立完成，后逐级返回client；

5 这组DataNode组成的Pipeline反方向上，发送ack，最终由Pipeline中第一个DataNode节点将Pipeline ack发送给Client

6 完成向文件写入数据，Client在文件输出流（FSDataOutputStream）对象上调用close方法，关闭流

7 调用DistributedFileSystem对象的complete方法，通知NameNode文件写入成功







  如果第一个block块的数据读完，就会关闭指向第一个block块的datanode连接，接着读取下一个block块

6、如果第一批block都读完了，DFSInputStream就会去namenode拿下一批blocks的location，然后继续读，如果所有的block块都读完，这时就会关闭掉所有的流。

 read 方法是并行的读取 block 信息，不是一块一块的读取；NameNode 只是返回Client请求包含块的DataNode地址，并不是返回请求块的数据；

 最终读取来所有的 block 会合并成一个完整的最终文件。

操作流程如上图：

当客户端对元数据进行增删改请求时，由于hadoop要求比较高，**它会先将操作写入到editlog文件里**，**先持久化**，然后将具体；此时2NN发现时间到了，或者edit数据满了或者刚开机时，就会请求执行辅助操作，**NN收到后将edit瞬间复制一份**，这个时候客户端传过来的数据继续写到edit里，我们把复制的edit和fsimage拷贝到2NN里，操作写在2NN的内存里合并，合并后将文件返回给NN做为新的Fsimage。

所以一旦NN宕机2NN比NN差一个edit部分，无法完全恢复原先状态，只能说辅助恢复。

但是辅助Namenode总是落后于主Namenode，所以在Namenode宕机时，数据丢失是不可避免的。在这种情况下，一般的，要结合第一种方式中提到的远程挂载的网络文件系统(NFS)中的Namenode的元数据文件来使用，把NFS中的Namenode元数据文件，拷贝到辅助Namenode，并把辅助Namenode作为主Namenode来运行


为了读写速度，datanode的位置信息是存在namenode的内存里的，不存硬盘，又因为会担心宕机，所以要备份一个fsimage，不断传数据，不断备份又会产生一致性问题，节点断电，数据丢失，所以采用editlog，延迟更新的方式，定期更新。但是定期更新这个操作由NN来做压力会太大，效率会变低，所以引入2NN来辅助。

通常，SecondaryNamenode 运行在一个单独的物理机上，因为合并操作需要占用大量的CPU时间以及和Namenode相当的内存

但namenode的fsimage并不永久保存块的位置信息，因为这些信息在系统启动时由数据节点重建

## 

