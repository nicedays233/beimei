![image-20200629091352859](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200629091352859.png)

分布式放在云中

有可能部分数据存储存在内存里，但是需要持久化的肯定是在磁盘里的。

高速的网络IO传输速度：1GB/s





hadoop有的时候无法把数据存储和数据计算分离开，

但是云可以。

![image-20200629093356412](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200629093356412.png)

### 分布式的高可用：

#### 1.备份

#### 2.



hadoop分布式计算每台机器没有共享

hadoop可以存不同数据格式的内容

格式：序列化？

hadoop vs RDBMS



|          | RDMS                                       | Hadoop                         |
| -------- | ------------------------------------------ | ------------------------------ |
| schema   | 写时必需考虑格式                           | 读时必须考虑格式问题           |
| 速度     | 读时很快（B+树）                           | （Hive读Mapreduce）写时很快    |
|          |                                            |                                |
| 处理能力 | 存储，没有处理                             | 计算与存储结合（云中两块分离） |
| 数据格式 | 结构化                                     | 任何格式                       |
| 使用情况 | 交互式数据分析<br />复杂的事务性处理<br /> | 非结构数据处理<br />大量数据   |

![image-20200629095741580](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200629095741580.png)

hadoop3.0增加了Erasure Code（纠删码）

性能优化和稳定性得到很大提升

2.0和1.0数据备份安全，对于每个数据块都会有三个备份，把三个备份分发到不同节点上。

那就意味着有3倍的存储量

所以3.0有了纠删码算法，就只有一个备份，如果有一块丢了，那么我就可以通过其他备份把这块丢失的算出来。

![image-20200629100848841](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200629100848841.png)



zookeeper解决了集群信息管理问题：

flume把日志数据收集送到hdfs下，现在升级可以完成数据传输的功能，

sqoop很单一，rdbms与hadoop互相迁移的功能

hbase

oozie任务定时系统，当写个spark，hive任务，任务之间有执行顺序，通过这个系统可以定义成工作流程，把工作序列化完成。

pig脚本语言，通过pig的脚本来执行mapreduce任务，现在有了spark，---已经退休了

mahout基于mapreduce的机器学习库--已经退休了

hive通过写sql将操作翻译成mapreduce或者sparksql任务或者Tez任务执行。

tez比mapreduce快很多

presto是sql执行引擎，交互式的数据查询，会立马给你结果，hive做不到，（他可能执行半个多小时），但presto处理不了大数据的联合查询



impala其实就是hive，性能比hive快了很多，底层是mapreduce

hcatlog处理元数据管理，在hadoop环境下，元数据的数据所在地。

ambari管理软件，用来检测hadoop不同模块的状况



![image-20200629104323797](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200629104323797.png)

zookeeper集群协调管理

![image-20200629104423060](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200629104423060.png)

Hadoop

NN

-接收所有节点活着还是挂掉的信息

-文件名，文件大小，文件块大小，文件备份信息

信息放在nn内存里

standby node-NN备份，nn挂了standby-nn来顶替

2NN-围绕数据的可靠性

元数据的合并处理，NN将edit log写到介质硬盘上，fsimage是nn某个时间点的数据快照，过段时间，fsimage和edit logs合并了成新的镜像。

namespace：

![image-20200629111116259](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200629111116259.png)

job运行在NN上

![image-20200629113146489](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200629113146489.png)

一个container里可以放1-n个block

去寻找dn位置时，永远从内存去拿nn

![image-20200629120521237](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200629120521237.png)

删除和强制性删除

![image-20200629121059217](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200629121059217.png)

![image-20200629121551775](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200629121551775.png)

![image-20200629121758558](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200629121758558.png)

![image-20200629121954020](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200629121954020.png)

![image-20200629122331851](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200629122331851.png) 