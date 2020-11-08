### 一：避免Hive进行MapReduce

- **select * from xxx**
- where中过滤条件仅为**分区字段**时

> 执行下面命令，可以让Hive尝试使用本地模式执行操作：

```shell
set hive.exec.mode.local.auto=true;
```

### 二： JOIN优化：

- 多表join时，如果on子句连接键相同，那么将最大的表放在最后，Hive会尝试将**其他表缓存起来**，扫描最后 那个表进行计算（小表最大25M）

### 三：设置合理的reduce数：

MapReduce 程序中，reducer 个数的设定极大影响执行效率，这使得 Hive 怎样决定 reducer 个数成为一个关键问题。遗憾的是 Hive 的估计机制很弱，不指定 reducer 个数的情况下，Hive 会猜测确定一个 reducer 个数，基于以下两个设定：

- hive.exec.reducers.bytes.per.reducer（默认为 256000000
- hive.exec.reducers.max（默认为 1009）
- mapreduce.job.reduces=-1（设置一个常量 reducetask 数量）

计算 reducer 数的公式很简单： N=min(参数 2，总输入数据量/参数 1) 通常情况下，有必要手动指定 reducer 个数。考虑到 map 阶段的输出数据量通常会比输入有 大幅减少，因此即使不设定 reducer 个数，重设参数 2 还是必要的。

依据 Hadoop 的经验，可以将参数 2 设定为 0.95*(集群中 datanode 个数)。

### 四：优化Hive数据倾斜问题：

> 数据倾斜产生原因：
>
> - key分布不均匀。
> - map端数据倾斜，输入文件太多且大小不一 。
> - reduce端数据倾斜，分区器问题。
> - 业务数据本身的特征。



#### 业务场景解决：

---

> 空值数据过多，全部移到一个reduce端处理

`解决办法:给空值变成字符串+随机数`

---

> 不同数据类型关键字段关联，未处理的类型全部都分到一个reducer中

`解决办法:将数据类型转成一致`

---

> key值过于集中，很多key值分到一个reduce中

`解决办法:将key值集中的数据新生成一张小表存入内存，再使用mapjoin，在map端完成reduce`

---

#### 调节hive配置参数:

- **设置hive.map.aggr=true** 

   ---map端部分聚合，相当于Combiner

- **设置hive.groupby.skewindata=true**

   ---有数据倾斜时，查询计划生成两个mr job， 第一个job先进行key随机分配处理，先缩小数据量。第二个job再进行真正的group by key处理

----

### 五：JVM重用：

> 解决小文件和task特别多的场景

修改hadoop的mapred-site.xml文件进行设置

```xml
<property>
    <name>mapred.job.reuse.jvm.num.tasks</name>
    <value>10</value>
</property>

```

> 使得jvm实例在同一个job中重新使用N次，减少JVM启动造成的开销。

1、hive语句的书写顺序：（从前往后）
(1)select
(2)from
(3)join on
(4) where
(5)group by
(6)having
(7)distribute by/cluster by
(8) sort by
(9) order by
(10) limit
(11) union(去重不排序)/union all（不去重不排序）

2、hive语句的执行顺序：
(1)from
(2)on
(3)join
(4)where
(5)group by
(6)having
(7)select
(8)distinct
(9)distribute by /cluster by
(10)sort by
(11) order by
(12) limit
(13) union /union all