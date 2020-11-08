## 用户离线标签兴趣取向平台：

### 一：数据探索

```js
val dfUsers = spark.read.format("csv").option("header", "true").load("hdfs:///events/data/users.csv")

 dfUsers.select("user_id").distinct.count
dfUsers.count


 
import org.apache.spark.sql.types._
import org.apache.spark.sql.functions._

val df1 = dfUsers.select(col("user_id"), col("birthyear").cast(IntegerType).as("f_birthyear"), col("birthyear"))
val df2 = df1.filter(col("f_birthyear").isNull)
df2.count

df2.select("birthyear").distinct.show

val df1 = dfUsers.withColumn("birthyear", col("birthyear").cast(IntegerType))

val dfAvgAge =  df1.select(avg(col("birthyear")).cast(IntegerType).as("avg_year"))

val df2 = df1.crossJoin(dfAvgAge).withColumn("new_birthyear", when(col("birthyear").isNull, col("avg_year")).otherwise(col("birthyear")))

df2.show
//val df2 = df1.withColumn("birthyear", when(col("birthyear").isNull, lit(1988)).otherwise(col("birthyear")))


 dfUsers.groupBy($"gender").agg(count($"user_id").as("cnt")).show

val df3 = dfUsers.withColumn("gender", when($"gender".isNull, lit("unknown")).otherwise($"gender"))
df3.select("gender").distinct.show
```

```js
val dfEvents = spark.read.format("csv").option("header", "true").load("hdfs:///events/data/events.csv")
dfEvents.cache.count
dfEvents.select("event_id").distinct.count


 dfEvents.createOrReplaceTempView("events")


 select user_id, count(*) as cnt from events group by user_id order by cnt desc limit 10

dfUsers.createOrReplaceTempView("users")

select count(*) from events e inner join users u on u.user_id = e.user_id

select count(*) from events where start_time regexp '^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.*


 dfEvents.filter($"start_time".rlike("^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.*")).count
```



### 二：数据缓冲

#### Kafka：

> **high-throughput**，**distributed**，**publish-subscribe** messaging system

- fast
- scalable
- durable
- real-time

##### kafka architecture：

![image-20200921090124773](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200921090124773.png)

> -  kafka maintains **feeds of messages in called Topics**
> - Producers **publish messages to a kafka topic**
> - consumers **subscribe to topics** and process the feed of published messages
> - **servers in a kafka cluster** are called brokers



##### kafka topic：

- Topics：
- Partitions：
- Logs：
- Retention Period：
- Consumers maintain and track their locations/offsets in each log



```shell
#修改脚本
vi .bashrc


# .bashrc

# User specific aliases and functions

alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Source global definitions
if [ -f /etc/bashrc ]; then
        . /etc/bashrc
fi
export SPARK_MAJOR_VERSION=2
sed -i s/'history -cw'//g .bash_logout
export PATH=/usr/hdp/current/kafka-broker/bin:$PATH
```

```shell
#启动kafka
kafka-server-start.sh /usr/hdp/2.6.4.0-91/kafka/config/server.properties
#创建topic
kafka-topics.sh --zookeeper sandbox-hdp.hortonworks.com:2181 --create --topic test --partition 3 --replication-factor 1


# 查看topic
kafka-topics.sh --zookeeper sandbox-hdp.hortonworks.com:2181  --list

# 查看topic分区
kafka-topics.sh --zookeeper sandbox-hdp.hortonworks.com:2181 --describe --topic test

# 修改主题数据保留时间
kafka-topics.sh --zookeeper sandbox-hdp.hortonworks.com:2181 --alter --topic test --config retention.ms=10000

kafka-topics.sh --zookeeper sandbox-hdp.hortonworks.com:2181 --alter --topic test -delete-config retention.ms
```



![image-20200921093913335](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200921093913335.png)





##### Kafka Message Flow

![image-20200921094507701](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200921094507701.png)

> producer可以控制指定发送到哪个分区（robin）
>
> consumer可以指定我消费哪个分区

##### Kafka High-Throughput & Low-Latency

-  Batching of individual messages
-  Zero copy I/O using sendfile 

##### kafka Broker

-  Each partition has one server acting as a leader, and zero or more servers acting as followers / ISRs

  >  broker数要比分区数大得多, 每个分区的备份最好放在不在leader的其他机器上

- Each server acts as a leader for some partitions and a followers for others, so load is well balanced

  > 每个broker最好只要有一个leader

##### kafka Producer

-  Producers publish data to the topics of their choice

  > 通过分区分配策略来控制我发送哪个分区

-  Async Publishing (less durable)

  > 把ack调成0，数据可靠性最差的情况

-  All nodes can answer metadata requests about: 

  > 所有机器都可以提供位置信息给你作为传送消息的节点

##### kafka Consumer

> 可以定义细粒度：可以去拿topic，也可以去拿partition

- Consumers consume messages through subscriptions

- Multiple Consumers can read from the same topics 

- Consumers are organized into Consumer Groups

  > 一个partition只能被一个group的一个consumer消费，
  >
  > partition数量应该大于consumer数量

- Kafka offers messages to Consumer Groups, not Consumer (instance) directly

  > kafka的offset消息是在消费组层面上的,在组里每个consumer都知道partition读到什么地方，如果有consumer挂掉，下一个consumer会继续从offset之后拿

- Messages remain on Kafka, which are not removed after they are consumed

- **Messaging models**

  >  **Queue:** a message goes to one of the consumers. 
  >
  > ​	⚫ All consumers are in the same Consumer Group
  >
  > **Publish-Subscribe:**  a message goes to all consumers. 
  >
  > ​	⚫ All consumers are assigned to different Consumer Groups;
  >
  > 发布订阅，我多个消费组中的一个消费者去消费一个message时，这样可以并行去消费。

##### kafka ZooKeeper

- Starting from 0.10, Kafka has its own internal topic for the offset storage

##### kafka API

◆ **The Producer API** allows an application to publish a stream of records to one or more Kafka topics. 

◆ **The Consumer API** allows an application to subscribe to one or more topics and process the stream of records produced to them.

 ◆ **The Streams API** allows an application to act as a stream processor , consuming an input stream from one or more topics and producing an output stream to one or more output topics, effectively transforming the input streams to output streams.

 ◆ **The Connector API** allows building and running reusable producers or consumers that connect Kafka topics to existing applications or data systems.

##### Message Ordering

**To ensure global ordering for a topic:**

◼ If all message must be ordered within **one topic, use one partition**

> 全局有序得话，最好把分区数设为一

 ◼ If messages can be ordered by certain properties

​	 ⚫ Group messages in a partition by Key (defined upon the properties in producer) 

​	 ⚫ Configure exactly one consumer instance per partition within a consumer group 

##### Message Replication

◼ 0 – the producer never waits for an ack

◼ 1 – the producer gets an ack after the leader replica has received the data 

◼ -1 / all – the producer gets an ack after all ISRs (in-sync replication) receives the data

##### Data Loss at the Producer

**◆ Kafka Producer API** 

​	◼ Messages are accumulated in buffer in batches

> 批量发送

​	◼ Messages are batched  by partition, retried at batch level

>  

​	◼ Expired batches dropped after retries

> 在重试之后，批处理的消息到期了

**◆ Data Loss at Producer** 

​	◼ Failed to close / flush producer on termination 

> 没有成功刷新最后得消息

​	◼ Dropped batches due to communication or other errors when acks = 0 or retry exhaustion

##### Data Delivered but Loss in the Cluster

![image-20200922084242771](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200922084242771.png)

##### Data Duplication

> consumer和producer都会发生数据重复消费

![image-20200922085116224](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200922085116224.png)

##### Kafka Use Cases

◆ Real-Time Streaming Processing (combined with Spark Streaming) 

◆ General purpose Message Bus 

◆ Collecting User Activity Data 

> 用户行为数据

◆ Collecting Operational Metrics from Applications, Servers or Devices 

◆ Log Aggregation (combined with ELK) 

◆ Change Data Capture

◆ Commit Log for distributed System

#### Flume：



#### SparkStreaming：

