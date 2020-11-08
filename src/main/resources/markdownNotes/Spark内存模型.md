## Spark内存模型：

### Spark核心组件：

#### Driver：

> spark驱动器节点，用于执行Spark任务的main方法

##### 主要负责：

- 将用户程序转化为作业job
- 在executor之间调度任务task
- 跟踪executor的执行情况

#### Executor：

> Executor为JVM进程，运行具体任务

PS：Executor节点在Spark应用启动后，一起启动，生命周期和应用程序相同，如果Executor节点故障，Spark应用会将出错节点上任务调度到其他Executor上继续运行。

### Spark通用运行流程：

![image-20200803115724224](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200803115724224.png)

- 任务提交后，先启动Driver进程
- 随后Driver进程向集群管理器注册应用程序。
- 之后集群管理器根据此任务的配置文件分配Executor并启动它，当Driver所需的资源全部满足后，Driver开始执行main函数
- Spark因为是懒执行，当遇到action算子，才开始反向推算，根据宽依赖划分stage，之后每个stage对应一个taskset，一个taskset对应多个task，本地化原则下，task会被分发到指定Executor去执行，执行过程中，Executor不断与Driver进行通信，报告任务运行情况。
- 



##### 核心功能：

- 负责运行组成Spark应用的任务，并将结果返回给驱动器进程
- 通过自身的块管理器（BM），为用户程序要求缓存的RDD提供内存式存储，RDD是直接缓存在Executor进程内的，因此任务可以在运行时充分利用缓存数据加速运算

作为一个基于内存的分布式计算引擎，

在执行spark应用程序时，spark集群启动**Driver和Executor**两种JVM进程。

前者为**主控进程**，负责创建spark上下文，提交spark作业job，并将作业转化为计算任务Task，在各个executor进程间协调任务的调度。

后者**负责在工作节点执行具体的计算任务**，并将结果返回给Driver，同时为需要持久化的**RDD提供存            储功能**，由于Driver的内存管理相对来说较为简单。

### 堆内内存：

> 堆内内存的大小，由 Spark 应用程序启动时的 –executor-memory 或 spark.executor.memory 参数配置。
>
> Executor 内运行的并发任务共享 JVM 堆内内存，**这些任务在缓存 RDD 数据和广播（Broadcast）数据时占用的内存被规划为存储（Storage）内存，而这些任务在执行 Shuffle 时占用的内存被规划为执行（Execution）内存，剩余的部分不做特殊规划，那些 Spark 内部的对象实例，或者用户定义的 Spark 应用程序中的对象实例，均占用剩余的空间**。不同的管理模式下，这三部分占用的空间大小各不相同。



### 堆外内存：

> 进一步优化内存的使用，提高shuffle时排序的效率。

#### 堆外内存的好处：

- 直接操作系统堆外的内存，减少了不必要的内存开销。减少了频繁GC扫描和回收。
- 堆外内存被精准申请和释放，序列化数据占用的空间被精确计算。

`在默认情况下堆外内存并不启用，可通过配置 spark.memory.offHeap.enabled 参数启用，并由 spark.memory.offHeap.size 参数设定堆外空间的大小。`

#### 。

