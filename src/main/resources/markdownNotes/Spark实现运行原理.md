## Spark运行原理：

### 一：Spark word count 运行原理：

![image-20200728153255115](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200728153255115.png)

### 二：Stage：

![image-20200729192135189](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200729192135189.png)

由上图可知：

- 一个Stage对应着有多个Task
- 一个RDD有多个分区
- 一个分区会运行着一个task处理数据
- task横向贯穿stage

**通过是不是会产生一个shuffle来区分不同的Stage**

### 三：为什么要执行Stage？

- **数据本地化**
  - 移动计算，不是移动数据
  - 保证一个stage内不会发生数据移动

### 四：Spark Shuffle过程：

- 在分区之间重新分配数据
  - 父RDD中**同一分区**中的数据按照算子要求重新进入子RDD的**不同分区**中
  - 中间结果写入磁盘
  - 由子RDD拉取数据，而不是由父RDD推送
  - 默认情况下，Shuffle不会改变分区数量

### 五：RDD的依赖关系：

> DAG图确定后，系统从后往前划分stage，遇到宽依赖就分开断成新的stage

- **Lineage：血统，遗传**
  - 保存了RDD的依赖关系
  - RDD实现了基于lineage的容错机制
- 依赖关系
  - 宽依赖
    - 一对多
  - 窄依赖
    - 一对一



### 六：DAG工作原理：

- 根据RDD之间的依赖关系，形成DAG执行计划
- DAG Scheduler将DAG划分为多个Stage
  - 划分依据：是否发生宽依赖
  - 划分规则：从后往前，遇到宽依赖切割为新的Stage
  - 每个Stage由一组并行的Task组成

### 七：RDD优化：

#### Spark提高并行度：

##### 1.task数量：

> 设置成总cpucore数量2-3倍

##### 2.设置一个sparkApp并行度：

##### 3.增加hdfs得block数：

##### 4.RDDrepartition：

##### 5.reduceByKey指定分区数量：

##### 6.coalesce：将RDD的原本N个分区，划分为M个分区

![image-20200728164317222](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200728164317222.png)

> 将本来要传到N个分区的，变成传到M个分区，M小了就容易形成窄依赖，就不用shuffle
>
> N>M:窄依赖
>
> N<M
>
> N~=M



#### RDD持久化

- **RDD缓存机制：**缓存数据至内存/磁盘，可大幅度提高spark应用性能。
- **缓存策略：**storageLevel
  - memory_only
  - memory_and_disk
  - disk_only
- **缓存应用场景**
  - 从文件加载数据之后，因为重新获取文件成本较高
  - 经过较多的算子变换之后，重新计算成本较高
  - 单个非常消耗资源算子之后

### 八：RDD分布式共享变量：

- **广播变量**：允许将一个**只读**变量缓存到**每个节点**上，而不是**每个任务传递一个副本。**

```js
var broadcastVar = sc.broadcast(Array(1,2,3)) // 定义i广播变量
broadcastVar.value // 访问方式
```

- **累加器**：只允许added操作，常用于实现计数

```js
val accum = sc.accumulator(0,"My Account")
sc.parallelize(Array(1,2,3,4)).foreach(x => accum += x)
accum.value
```

### 九：RDD分区设计：

- `分区太小限制2GB`
- `分区太少`
  - 不利于并发
  - 更容易受数据倾斜影响
  - groupBy,reduceByKey，sortByKey等内存压力增大
- `分区过多`
  - shuffle开销越大
  - 创建任务开销越大
- `分区经验`
  - 每个分区大约128MB
  - 如果分区小于但接近2000，则设置为大于2000

### 十：数据倾斜：

1. 避免shuffle
2. 减少shuffle数据量

#### 避免shuffle：

- 

>  两大方向：避免shuffle，减少shuffle的数据量

- 往往是因为分区中数据分配不均匀，数据集中在少量分区

  > groupby,join之后

#### 解决方案：

- 避免shuffle
- 缩小key粒度
- 增大key粒度
- 提高shuffle操作的reduce并行度
- 直接过滤倾斜的key
- broadcast将reducejoin变成mapjoin
- 随机key双重聚合（加随机数）

- hash加盐重新分区
- 

