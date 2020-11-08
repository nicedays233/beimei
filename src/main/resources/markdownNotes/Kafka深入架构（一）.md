## Kafka基本简介与命令：

> Kafka是一种高吞吐量的分布式发布-订阅消息系统

- 快速，但Broker每秒几百MB读取
- 不停机扩展集群
- 消息副本冗余
- 实时数据管道

### 一：为什么要使用消息中间件（MQ）？

- **异步调用**
  - 同步变异步
- **应用解耦**
  - 提供基于数据的接口层
- **流量削峰**
  - 缓解瞬时高流量压力

### 二：kafka单机部署

> Kafka 必须依赖 ZooKeeper，所以应该确保 ZooKeeper 已成功运行。Kafka 内置 了 ZooKeeper，故如果未安装 ZooKeeper 可以使用其内置 ZooKeeper。

#### 第一步：解压tar包并复制

```shell
tar -xzf kafka_2.11-2.0.0.tgz
mv kafka_2.11-2.0.0.tgz /opt/soft/kafka211
```

#### 第二步：配置全局变量

```shell
export KAFKA_HOME=/opt/soft/kafka211
export PATH=$PATH:$KAFKA_HOME/bin
```

#### 第三步：修改server.properties

```shell
vi /opt/soft/kafka211/config/server.properties
```

- 修改内容

```shell
# 机器id每台不一样就行
broker.id=0
# 修改logdir的地址
log.dirs=/data/kafka-logs
# 连接zk的地址
zookeeper.connect=localhost:2181 #localhost 可根据情况换 
```

#### 第四步：先启动zk，开启kafka：

```shell
zkServer.sh start
kafka-server-start.sh /opt/soft/kafka211/config/server.properties
```

![image-20200812113408830](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200812113408830.png)

### 二：Topic：主题

- **Topic**
  - 主题是已发布消息的类别名称
  - 发布和订阅数据必须指定主题
  - **主题副本数量不大于Brokers个数**

- **Partition**
  - 一个主题包含多个分区，默认按Key Hash分区
  - 每个Partition对应一个文件夹<topic_name>-<partition_id>
  - 每个Partition被视为一个有序的日志文件（LogSegment）
  - **Replication策略是基于Partition,而不是Topic**
  - **每个Partition都有一个Leader，0或多个Followers**

---

### 三：Message

- **header**：**消息头，固定长度**
  - offset：唯一确定每条消息在分区内的位置
  - CRC32：用crc32校验消息
  - "magic"：表示本次发布Kafka服务程序协议版本号
  - "attributes"：表示为独立版本、或标识压缩类型、或编码类型

- **body**：**消息体**
  - key：表示消息键，可选
  - value bytes payload：表示实际消息数据

---

### 四：Producer：生产者

- 生产者将消息写入到Broker
  - Producer直接发送消息到Broker上的Leader Partition
  - Producer客户端自己控制着消息被推送到哪些Partition
    - 随机分配、自定义分区算法等
  - Batch推送提高效率

---

### Broker：消息服务器

- **kafka集群中每个Broker都可以响应Producer的请求**
  - 哪些Brokers是存活的？
  - topic的leader partition在哪？
- **每个Broker充当Leader和Followers保持负载平衡**
  - leader处理所有读写请求
  - followers被动复制leader

---

### Consumer：消费者

- **消费者通过订阅消费信息**
  - offset的管理是基于消费组的级别
  - 每个partition只能由同一消费组的一个Consumer来消费
  - 每个Consumer可以消费多个分区
  - 消费过的数据仍会保留在kafka中
  - 消费者不能超过分区数量
- **消费模式**
  - 队列：所有消费者在一个消费组内
  - 发布/订阅：所有消费者被分配到不同的消费组



---

### ZooKeeper在Kafka中的作用：

- **Broker注册并监控状态**
  - /brokers/ids
- **Topic注册**
  - /brokers/topics
- **生产者负载均衡**
  - 每个Brokers启动时，都会完成Broker注册过程，生产者会通过该节点的变化来动态的感知Broker服务器列表的变更。
- **offset维护**
  - **0.10之后kafka使用自己内部主题维护offset**

### 一些简单命令：

#### 开启kafka：

```js
kafka-server-start.sh /opt/soft/kafka211/config/server.properties 
```



#### 创建主题：

```shell
 kafka-topics.sh --create --zookeeper 192.168.56.101:2181 --replication-factor 1 --partitions 1 --topic flumeKafkaStream1
# replication-factor备份数量
 
```

#### 查看主题：

```shell
kafka-topics.sh --zookeeper 192.168.56.101:2181 --list
```

#### 向消息队列中生产消息：

```shell
kafka-console-producer.sh --broker-list 192.168.56.101:9092 --topic demo
```

#### 消费信息

```shell
kafka-console-consumer.sh --bootstrap-server 192.168.56.101:9092 --from-beginning --topic demo
```

#### 删除主题

- 修改配置

```shell
cd /opt/soft/kafka211/config/server.properties
```

- 添加配置

```shell
delete.topic.enable=true
```

- 命令删除主题

```shell
kafka-topics.sh --zookeeper 192.168.56.101:2181 --delete -- topic mydemo
```

#### 查看对应分区的数据

```js
kafka-run-class.sh kafka.tools.GetOffsetShell --topic msgEvent --time -1 --broker-list 192.168.56.101:9092 --partitions 0
```



![image-20200820084213278](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200820084213278.png)

#### 重置用户组游标

```shell
kafka-consumer-groups.sh --bootstrap-server 192.168.56.101:9092 --group test2 --reset-offsets --all-topics --to-earliest --execute
```

#### 消费单个分区

![image-20200820084359561](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200820084359561.png)

#### 查看消费组消费游标

```shell
kafka-consumer-groups.sh --describe --group group1 --bootstrap-server 192.168.56.101:9092
```



![image-20200820084424994](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200820084424994.png)

![image-20200820084601232](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200820084601232.png)