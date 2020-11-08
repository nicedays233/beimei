## kafka面试题：

### 1.Kafka中broker的意义：

### 2.kafka服务器能接收到的最大信息是什么？

### 3.Kafka中zookeeper起什么作用？

> zookeeper 是一个分布式的协调组件，早期版本的kafka用zk做meta信息存储，consumer的消费状态，group的管理以及 offset的值。考虑到zk本身的一些因素以及整个架构较大概率存在单点问题，新版本中逐渐弱化了zookeeper的作用。新的consumer使用了kafka内部的group coordination协议，也减少了对zookeeper的依赖，

 但broker依然依赖于ZK，zookeeper 在kafka中还用来选举controller 和 检测broker是否存活等等。

### 4.解释kafka用户如何消费信息？

### 5.kafka consumer消费数据有哪些特点

- offset的管理是基于消费组（group.id）的级别
- 每个Partition只能由同一消费组内的一个Consumer来消费
- 每个Consumer可以消费多个分区
- 消费过的数据仍会保留在Kafka中
- 消费者不能超过分区数量

### 6.如何提高远程用户的吞吐量

### 7.如果副本在ISR中停留了很长时间表明什么？

### 8.有可能在生产后发生消息偏移吗？

### 9.为什么要使用消息队列？

**缓冲和削峰**：上游数据时有突发流量，下游可能扛不住，或者下游没有足够多的机器来保证冗余，kafka在中间可以起到一个缓冲的作用，把消息暂存在kafka中，下游服务就可以按照自己的节奏进行慢慢处理。

**解耦和扩展性**：项目开始的时候，并不能确定具体需求。消息队列可以作为一个接口层，解耦重要的业务流程。只需要遵守约定，针对数据编程即可获取扩展能力。

**冗余**：可以采用一对多的方式，一个生产者发布消息，可以被多个订阅topic的服务消费到，供多个毫无关联的业务使用。

**健壮性**：消息队列可以堆积请求，所以消费端业务即使短时间死掉，也不会影响主要业务的正常进行。

**异步通信**：很多时候，用户不想也不需要立即处理消息。消息队列提供了异步处理机制，允许用户把一个消息放入队列，但并不立即处理它。想向队列中放入多少消息就放多少，然后在需要的时候再去处理它们。

### 10.kafka producer如何优化打入速度？

> 增加线程

> 提高 batch.size

> 增加更多 producer 实例

> 增加 partition 数

> 设置 acks=-1 时，如果延迟增大：可以增大 num.replica.fetchers（follower 同步数据的线程数）来调解；

> 跨数据中心的传输：增加 socket 缓冲区设置以及 OS tcp 缓冲区设置。

### 11.kafka unclean 配置代表啥，会对 spark streaming 消费有什么影响？

> unclean.leader.election.enable 为true的话，意味着非ISR集合的broker 也可以参与选举，这样有可能就会丢数据，spark streaming在消费过程中拿到的 end offset 会突然变小，导致 spark streaming job挂掉。如果unclean.leader.election.enable参数设置为true，就有可能发生数据丢失和数据不一致的情况，Kafka的可靠性就会降低；而如果unclean.leader.election.enable参数设置为false，Kafka的可用性就会降低。
>
>  

### 12.如果leader crash时，ISR为空怎么办？

> kafka在Broker端提供了一个配置参数：unclean.leader.election,这个参数有两个值：
>
> true（默认）：允许不同步副本成为leader，由于不同步副本的消息较为滞后，此时成为leader，可能会出现消息不一致的情况。
>
> false：不允许不同步副本成为leader，此时如果发生ISR列表为空，会一直等待旧leader恢复，降低了可用性。

### 13.kafka的message格式是什么样的？

> 一个Kafka的Message由一个固定长度的header和一个变长的消息体body组成
>
> header部分由一个字节的magic(文件格式)和四个字节的CRC32(用于判断body消息体是否正常)构成。
>
> 当magic的值为1的时候，会在magic和crc32之间多一个字节的数据：attributes(保存一些相关属性，
>
> 比如是否压缩、压缩格式等等);如果magic的值为0，那么不存在attributes属性
>
> body是由N个字节构成的一个消息体，包含了具体的key/value消息

### 14.kafka中consumer group 是什么概念

同样是逻辑上的概念，是Kafka实现单播和广播两种消息模型的手段。同一个topic的数据，会广播给不同的group；同一个group中的worker，只有一个worker能拿到这个数据。换句话说，对于同一个topic，每个group都可以拿到同样的所有数据，但是数据进入group后只能被其中的一个worker消费。group内的worker可以使用多线程或多进程来实现，也可以将进程分散在多台机器上，worker的数量通常不超过partition的数量，且二者最好保持整数倍关系，因为Kafka在设计时假定了一个partition只能被一个worker消费（同一group内）。



### 15.kafka消息数据积压，kafka消费能力不足怎么处理？

- 增加topic的分区数，同时提升消费者组的消费者数量
- 提高每批次拉取数量

### 16.kafka参数优化

1. broker参数配置（server.properties）

   > 日志保留策略配置
   >
   > log.retention.hours=72

   > replica相关配置
   >
   > default.replication.factor:1

   > 网络通信延时
   >
   > replica.socket.timeout.ms:30000 #当集群之间网络不稳定时,调大该参数 
   >
   > replica.lag.time.max.ms=600000 # 如果网络不好,或者 kafka 集群压力较 大,会出现副本丢失,然后会频繁复制副本,导致集群压力更大,此时可以调大该参数 

2. producer优化(producer.properties)

   > compression.type:none                       (gzip  snappy   lz4)
   >
   > #默认发送不进行压缩，选一种压缩，大幅减缓网络压力和Broker的存储压力

   

3. kafka内存调整(kafka-server-start.sh)

   > export KAFKA_HEAP_OPTS="-Xms4g -Xmx4g"
   >
   > 默认内存1个g，生产环境尽量不超过6个g

### Kafka单条日志传输大小

> 单条默认值为1M，单常常会出现一条消息大于1m的时候，需要对kafka的server.properties

```shell
replica.fetch.max.bytes:104857 broker可复制的消息的最大字节数
message.max.bytes:1000012 kafka会接收单个消息size的最大限制
```

