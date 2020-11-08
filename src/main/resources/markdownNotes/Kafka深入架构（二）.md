## Kafka工作流程及文件存储机制

### 工作流程：

![image-20200809234611546](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200809234611546.png)

- 第一步：生产者往broker的topic的leader发送数据，follower同步数据

- 第二步：消费者从leader去消费数据

### topic底层存储：

- topic分为**多个partition**

- 每个分区的文件分成**多个segment，**

- segment存着**.log日志文件和.index索引文件**

![image-20200810003441731](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200810003441731.png)

offset=8 通过名称先确定是哪一个index文件，再用offset-文件名找到是第几个偏移量。



> index和log位于同一个文件夹下，文件夹命名规则是：topic名称+ 分区序号

## Producer生产者架构：

### 一：分区存储策略：

#### 1.分区的原因：

- 方便集群中扩展
- 可以提高并发

#### 2.分区的原则：

> producer发送数据封装成ProducerRecord对象

##### ProducerRecord构造器：

![image-20200810004101122](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200810004101122.png)



- `指明partition的情况下`，直接将指明的值直接作为partition值
- `没有指明partition值但由key的情况下`，会将key的hash值与topicpartition进行取余得到partition值
- `没有指明partition值也没有key的情况下`，第一次调用随机生成一个整数（后面每次调用在整数上自增），将这个值与topic可用的partition总数取余得到partition值，也就是round-robin算法。

### 二：数据可靠性保证策略：

#### 生产者到Kafka端发送数据：

> producer给leader发送完数据后，leader会将follower同步完成后，leader再发送ack，这样才能保证leader挂掉之后，能再follower中选举出合适的leader，

##### 副本数据同步策略：

- kafka由于会存放大量数据，不会去选择半数存活机制，半数会造成大量数据冗余。
- 因为都是部署在一个机架上的，所以网络延迟对kafka影响比较小

多少个follower同步完成后发送ack？

半数以上,因为为了防止脑裂同时参与投票也需要半数以上，

![image-20200810005415316](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200810005415316.png)

![image-20200810005607669](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200810005607669.png)

![image-20200810005749512](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200810005749512.png)



##### ISR：动态集合in-sync replica set

> 当有follower完成数据同步后，follower就给leader发送ack，follower长时间未响应，将被踢出ISR，leader故障，从ISR中选举新的leader

**踢出时间阈值由：**

```shell
replica.lag.time.max.ms #参数设定
```

##### 故障节点发生处理细节：

> **LEO（log-end-offset）**：每个副本的最后一个offset 

> **HW（high watemark）**：所有副本中最小的LEO

- follower故障：

> follower会被踢出ISR，follower读取本地磁盘的记录得HW，高于log文件得全部删掉，从HW开始进行向leader同步
>
> 等该 follower 的 LEO 大于等于该 Partition 的 HW，即 follower 追上 leader 之后，就可以重新 加入 ISR 了。 

- leader故障：

> leader发生故障后，从ISR中选出一个新的leader之后，，之后，为保证多个副本之间的 数据一致性，其余的 follower 会先将各自的 log 文件高于 HW 的部分截掉，然后从新的 leader同步数据。
>
> 只能保证副本得数据一致性

##### ack应答机制：

- ack参数等级
  - 0：producer不等待broker的ack，broker已接受到还没写入磁盘就返回成功，可能会造成数据丢失
  - 1：producer等待broker的ack，partition的leader落盘成功返回ack，**follower同步成功之前leader故障，数据可能会丢失**
  - -1（all）：leader和follower全部落盘成功才返回ack**，当follow同步完成之后，leader挂了，producer又发了一次写入broker请求，结果在另外一个leader又写了一次，造成数据重复**



##### Exactly Once语义:

> 保证每条信息被发送且仅被发送一次

0.11后，kafka引入`幂等性机制`（dempotent）（实例化一次机制），配合acks = -1时得at least once语义（会重复不丢失），完成了exactly once



> 只需将enable.idempotence属性设置为true，kafka自动将acks属性设为-1

###### 幂等性实现：

> 开启幂等性的 Producer 在初始化的时候会被分配一个 PID，发往同一 Partition 的消息会附带 SequenceNumber。而 Broker 端会对<PID,Partition,SeqNumber>做缓存，当具有相同主键的消息提交时，Broker 只会持久化一条。
> 但是 PID 重启就会变化，同时不同的 Partition 也具有不同主键，所以幂等性无法保证跨 分区跨会话的 ExactlyOnce

## Consumer消费者端架构：

### 一：消费方式：

> consumer采用pull模式从broker中读取数据

**push模式很难适应消费速率不同得消费者，因为消息发送速率是由broker决定的**，他的目标是尽可能以最快速度传播信息，但是这样很容易造成consumer来不及处理信息。

**pull模式不足是，如果kafka没有数据，消费者可能会陷入循环中，一直返回空数组**，针对这一点，消费者再消费数据会传入一个时长参数timeout，当前没有数据共消费才返回。

### 二：分区分配策略：

> 一个 consumergroup 中有多个 consumer，一个 topic 有多个 partition，所以必然会涉及 到 partition 的分配问题，即确定那个 partition 由哪个 consumer 来消费。 

#### roundrobin分配：

### 三：offset--读取偏移量的维护

> ​	由于 consumer 在消费过程中可能会出现断电宕机等故障，consumer 恢复后，需要从故 障前的位置的继续消费，所以 consumer 需要实时记录自己消费到了哪个 offset，以便故障恢复后继续消费。

offset就是上图的012345的偏移量

 一次发一批数据 

