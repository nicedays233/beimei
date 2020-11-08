## Kafka额外知识点：

### 1.4 容灾 

> Kafka 容灾指当 Broker 宕机时的恢复机制。在 Kafka 集群中会有一个或者多个 Broker，其中有一个 Broker 会被选举为控制器（Kafka Controller），它负责管理整个集群中所有分区和副本的状态。

➢ 当某个分区的 Leader 副本出现故障时，由控制器负责为该分区选举新的Leader 副本。 
➢ 当检测到某个分区的 ISR 集合发生变化时，由控制器负责通知所有
Broker 更新其元数据信息。 
➢ 当使用 kafka-topics.sh 脚本为某个 topic 增加分区数量时，同样还是由控制器负责分区的重新分配。 



Kafka中的控制器选举的工作依赖于ZooKeeper，成功竞选为控制器的Broker会在 ZooKeeper 中创建/controller 这个临时（EPHEMERAL）节点，此临时节点
的内容参考如下： 
{"version":1,"brokerid":0,"timestamp":"1561214469054"} 
brokerid 表示称为控制器的 Broker 的 id 编号，timestamp 表示竞选称为控制
器时的时间戳。 

### Broker 容灾流程如下： 

1. Controller 在 ZooKeeper 的 /brokers/ids/[brokerId] 节点注册 Watcher，当 Broker 宕机时 ZooKeeper 会监听到。 
2. Controller 从/brokers/ids 节点读取可用 Broker。 
3. Controller 决定 set_p，该集合包含宕机 Broker 上的所有 Partition。 
4. 对 set_p 中的每一个 Partition： 
   （1）从/brokers/topics/[topic]/partitions/[partition]/state 节点读取 ISR； 
   （2）决定新 Leader； 
   （3）将新 Leader、ISR、controller_epoch 和 leader_epoch 等信息写入 state
   节点。 
5. 通过 RPC 向相关 Broker 发送 leaderAndISRRequest 命令

### 1.6 负载均衡 

在创建一个 Topic 时，Kafka 尽量将 Partition 均分在所有的 Broker 上，并且将 Replicas 也均分在不同的 Broker 上，这点如前面分区策略、副本策略中所述。 

另外关于 Leader 的负载均衡也需要注意，当一个 Broker 停止时，所有本来将它作为 Leader 的分区将会把 Leader 转移到其他 Broker 上去，极端情况下，会导致同一个 Leader 管理多个分区，导致负载不均衡，同时当这个 Broker 重启时，如果这个 Broker 不再是任何分区的 Leader，Kafka 的 Client 也不会从这个 Broker来读取消息，从而导致资源的浪费。 Kafka 中有一个被称为优先副本（preferred replicas）的概念。如果一个分区有 3 个副本，且这 3 个副本的优先级别分别为 0，1，2，根据优先副本的概念，0会作为Leader。当 0节点的Broker挂掉时，会启动1这个节点Broker当做Leader。当 0 节点的 Broker 再次启动后，会自动恢复为此 Partition 的 Leader。不会导致负载不均衡和资源浪费，这就是 Leader 的均衡机制。可在配置文件conf/ server.properties 中配置开启（默认就是开启）：

```shell
auto.leader.rebalance.enable=true 
例如，某个 Topic 详情如下： 
./kafka-topics.sh --zookeeper 127.0.0.1:2181 --describe --topic logdata-es 
Topic:logdata-es PartitionCount:2 ReplicationFactor:2 Configs: 
Topic: logdata-es Partition: 0 Leader: 0 Replicas: 0,1 Isr: 0,1 
Topic: logdata-es Partition: 1 Leader: 1 Replicas: 1,0 Isr: 0,1 
```

> Topic logdata-es 中 Partition 0 的 Replicas 为[0,1]，则 0 为 Preferred Replica。

### 提交偏移量的方式剖析： 

#### （1）自动提交 Automatic Commit 

enable.auto.commit 设置成 true（默认为 true），那么每过 5s，消费者自动把从 poll() 方 法 接 收 到 的 最 大 的 偏 移 量 提 交 。 提 交 的 时 间 间 隔 由auto.commit.interval.ms 控制，默认是 5s。自动提交的优点是方便，但是可能会重复处理消息。 

#### （2）手动提交偏移量  

将 enable.auto.commit 设置成 false，让应用程序决定何时提交偏移量。commitSync()提交由 poll()方法返回的最新偏移量，所以在处理完所有消息后要确保调用 commitSync()，否则会有消息丢失的风险。commitSync()在提交成功或碰到无法恢复的错误之前，会一直重试。如果发生了再均衡，从最近一批消息到发生再均衡之间的所有消息都会被重复处理。 

不足：Broker 在对提交请求作出回应之前，应用程序会一直阻塞，会限制应用程序的吞吐量。 