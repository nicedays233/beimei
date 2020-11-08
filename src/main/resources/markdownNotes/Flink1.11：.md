## Flink1.11：

### 流批得本质：

#### 流是批得特例：

> 以批处理为基础，将我的批处理细粒度化成微批，每来一条处理一次
>
> SparkSteaming，
>
> （本身有攒批得逻辑，有对批处理进行调度计算得过程，会比真正得流计算慢一点 ）



#### 批是流得特例：

> 以流处理为基础，每条数据得到来触发一次计算，Flink

### 流计算问题：

#### 延时问题

#### 更新撤回

#### 容错续跑

#### 透明升级

#### 乱序问题

#### 正确性问题

#### 部署问题

#### 弹性扩容

### 并行处理和编程范式

### DataSteeamAPI

![image-20200924003233715](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200924003233715.png)

### 状态和时间

![image-20200924005253943](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200924005253943.png)

### Flink连接器

> Flume像一个积极得收集者（多数据源），kafka像一个大慈善家（多消费者）

![image-20200924003950412](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200924003950412.png)

### unalignedCheckpoints

### WatermarkIdlenessDetection

### Batch and Streaming Unification

### Application Mode Deployments

### Change Data Capture

### Pandas UDF PyFlink\                                                                                                                                                                                                                                                                                                        