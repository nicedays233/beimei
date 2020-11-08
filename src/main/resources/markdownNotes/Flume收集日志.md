## Flume简介和基本使用：

> 一种可靠、可用的高效分布式数据收集服务。
>
> **Flume**拥有基于数据流上的简单灵活架构，支持容错、故障转移与恢复

### Flume架构：

- **Client**：客户端，数据产生的地方，如**Web服务器**

- **Event**：事件，指通过**Agent**传输的单个数据包，如日志数据通常对应一行数据

- **Agent**：代理，一个独立的JVM**进程**
  - Flume以一个或多个Agent部署运行
  - Agent包含三个组件
    - `Source`
    - `Channel`
    - `Sink`



### Flume工作流程：

![image-20200806094349152](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200806094349152.png)

>  Flume的本质分为三大块：输入源，管道，输出地

### Source输入源：

#### http source：

- 用于接收HTTP的get和post请求

| **属性** | **缺省值**                               | **描述**           |
| -------- | ---------------------------------------- | ------------------ |
| **type** | **-**                                    | **http**           |
| **port** | **-**                                    | **监听端口**       |
| bind     | 0.0.0.0                                  | 绑定IP             |
| handler  | org.apache.flume.source.http.JSONHandler | 数据处理程序类全名 |



#### avro source：

- 监听Avro端口，并从外部Avro客户端接收events

| **属性** | **缺省值** | **描述**               |
| -------- | ---------- | ---------------------- |
| **type** | **-**      | **avro**               |
| **bind** | **-**      | **绑定****IP****地址** |
| **port** | **-**      | **端口**               |
| threads  | -          | 最大工作线程数量       |

#### Spooling Directory Source：

> This source lets you ingest data by placing files to be ingested into a “spooling” directory on disk. This source will watch the specified directory for new files, and will parse events out of new files as they appear. The event parsing logic is pluggable. After a given file has been fully read into the channel, completion by default is indicated by renaming the file or it can be deleted or the trackerDir is used to keep track of processed files.
>
> Unlike the Exec source, this source is reliable and will not miss data, even if Flume is restarted or killed. In exchange for this reliability, only immutable, uniquely-named files must be dropped into the spooling directory. Flume tries to detect these problem conditions and will fail loudly if they are violated:
>
> 1. If a file is written to after being placed into the spooling directory, Flume will print an error to its log file and stop processing.
> 2. If a file name is reused at a later time, Flume will print an error to its log file and stop processing.
>
> To avoid the above issues, it may be useful to add a unique identifier (such as a timestamp) to log file names when they are moved into the spooling directory.
>
> Despite the reliability guarantees of this source, there are still cases in which events may be duplicated if certain downstream failures occur. This is consistent with the guarantees offered by other Flume components.

| Property Name            | Default     | Description                                                  |
| :----------------------- | :---------- | :----------------------------------------------------------- |
| **channels**             | –           |                                                              |
| **type**                 | –           | The component type name, needs to be `spooldir`.             |
| **spoolDir**             | –           | The directory from which to read files from.                 |
| fileSuffix               | .COMPLETED  | Suffix to append to completely ingested files                |
| deletePolicy             | never       | When to delete completed files: `never` or `immediate`       |
| fileHeader               | false       | Whether to add a header storing the absolute path filename.  |
| fileHeaderKey            | file        | Header key to use when appending absolute path filename to event header. |
| basenameHeader           | false       | Whether to add a header storing the basename of the file.    |
| basenameHeaderKey        | basename    | Header Key to use when appending basename of file to event header. |
| includePattern           | ^.*$        | Regular expression specifying which files to include. It can used together with`ignorePattern`. If a file matches both `ignorePattern` and `includePattern` regex, the file is ignored. |
| ignorePattern            | ^$          | Regular expression specifying which files to ignore (skip). It can used together with`includePattern`. If a file matches both `ignorePattern` and `includePattern` regex, the file is ignored. |
| trackerDir               | .flumespool | Directory to store metadata related to processing of files. If this path is not an absolute path, then it is interpreted as relative to the spoolDir. |
| trackingPolicy           | rename      | The tracking policy defines how file processing is tracked. It can be “rename” or “tracker_dir”. This parameter is only effective if the deletePolicy is “never”. “rename” - After processing files they get renamed according to the fileSuffix parameter. “tracker_dir” - Files are not renamed but a new empty file is created in the trackerDir. The new tracker file name is derived from the ingested one plus the fileSuffix. |
| consumeOrder             | oldest      | In which order files in the spooling directory will be consumed `oldest`, `youngest` and `random`. In case of `oldest` and `youngest`, the last modified time of the files will be used to compare the files. In case of a tie, the file with smallest lexicographical order will be consumed first. In case of `random` any file will be picked randomly. When using `oldest` and `youngest` the whole directory will be scanned to pick the oldest/youngest file, which might be slow if there are a large number of files, while using `random` may cause old files to be consumed very late if new files keep coming in the spooling directory. |
| pollDelay                | 500         | Delay (in milliseconds) used when polling for new files.     |
| recursiveDirectorySearch | false       | Whether to monitor sub directories for new files to read.    |
| maxBackoff               | 4000        | The maximum time (in millis) to wait between consecutive attempts to write to the channel(s) if the channel is full. The source will start at a low backoff and increase it exponentially each time the channel throws a ChannelException, upto the value specified by this parameter. |
| batchSize                | 100         | Granularity at which to batch transfer to the channel        |
| inputCharset             | UTF-8       | Character set used by deserializers that treat the input file as text. |
| decodeErrorPolicy        | `FAIL`      | What to do when we see a non-decodable character in the input file. `FAIL`: Throw an exception and fail to parse the file. `REPLACE`: Replace the unparseable character with the “replacement character” char, typically Unicode U+FFFD. `IGNORE`: Drop the unparseable character sequence. |
| deserializer             | `LINE`      | Specify the deserializer used to parse the file into events. Defaults to parsing each line as an event. The class specified must implement `EventDeserializer.Builder`. |
| deserializer.*           |             | Varies per event deserializer.                               |
| bufferMaxLines           | –           | (Obselete) This option is now ignored.                       |
| bufferMaxLineLength      | 5000        | (Deprecated) Maximum length of a line in the commit buffer. Use deserializer.maxLineLength instead. |
| selector.type            | replicating | replicating or multiplexing                                  |
| selector.*               |             | Depends on the selector.type value                           |
| interceptors             | –           | Space-separated list of interceptors                         |
| interceptors.*           |             |                                                              |

```properties
a1.channels = ch-1
a1.sources = src-1

a1.sources.src-1.type = spooldir
a1.sources.src-1.channels = ch-1
a1.sources.src-1.spoolDir = /var/log/apache/flumeSpool
a1.sources.src-1.fileHeader = true
```



#### Netcat Source：

> A netcat-like source that listens on a given port and turns each line of text into an event. Acts like `nc -k -l [host] [port]`. In other words, it opens a specified port and listens for data. The expectation is that the supplied data is newline separated text. Each line of text is turned into a Flume event and sent via the connected channel.

Required properties are in **bold**.

| Property Name   | Default     | Description                                   |
| :-------------- | :---------- | :-------------------------------------------- |
| **channels**    | –           |                                               |
| **type**        | –           | The component type name, needs to be `netcat` |
| **bind**        | –           | Host name or IP address to bind to            |
| **port**        | –           | Port # to bind to                             |
| max-line-length | 512         | Max line length per event body (in bytes)     |
| ack-every-event | true        | Respond with an “OK” for every event received |
| selector.type   | replicating | replicating or multiplexing                   |
| selector.*      |             | Depends on the selector.type value            |
| interceptors    | –           | Space-separated list of interceptors          |
| interceptors.*  |             |                                               |

```properties
# agent为实例名
# agent实例的三部分组成源，管道，输出槽
agent.sources = s1    
agent.channels = c1  
agent.sinks = sk1 

#设置Source为netcat 端口为5678，使用的channel为c1  接收端
agent.sources.s1.type = netcat  
agent.sources.s1.bind = localhost  
agent.sources.s1.port = 5678  
# 源和和管道连
agent.sources.s1.channels = c1    

#设置Sink为logger模式，使用的channel为c1  发送端
agent.sinks.sk1.type = logger  
# 槽和管道连
agent.sinks.sk1.channel = c1  


#设置channel为capacity 存内存
agent.channels.c1.type = memory
agent.channels.c1.capacity = 1000 # 最多容纳1000条
agent.channels.c1.transactionCapacity = 100 # 一次接100条数据

```



#### Exec Source：

- 执行linux指令，并消费指令返回的结果，如“tail -f”

| **属性**      | **缺省值** | **描述**                           |
| ------------- | ---------- | ---------------------------------- |
| **type**      | **-**      | **exec**                           |
| **command**   | **-**      | **如“tail  -f xxx.log”**           |
| **shell**     | **-**      | **选择系统Shell程序，如“/bin/sh”** |
| **batchSize** | **20**     | **发送给channel的最大行数**        |

#### Kafka Source：

> Kafka Source is an Apache Kafka consumer that reads messages from Kafka topics. If you have multiple Kafka sources running, you can configure them with the same Consumer Group so each will read a unique set of partitions for the topics. This currently supports Kafka server releases 0.10.1.0 or higher. Testing was done up to 2.0.1 that was the highest avilable version at the time of the release.

| Property Name                    | Default   | Description                                                  |
| :------------------------------- | :-------- | :----------------------------------------------------------- |
| **channels**                     | –         |                                                              |
| **type**                         | –         | The component type name, needs to be `org.apache.flume.source.kafka.KafkaSource` |
| **kafka.bootstrap.servers**      | –         | List of brokers in the Kafka cluster used by the source      |
| kafka.consumer.group.id          | flume     | Unique identified of consumer group. Setting the same id in multiple sources or agents indicates that they are part of the same consumer group |
| **kafka.topics**                 | –         | Comma-separated list of topics the kafka consumer will read messages from. |
| **kafka.topics.regex**           | –         | Regex that defines set of topics the source is subscribed on. This property has higher priority than `kafka.topics` and overrides `kafka.topics` if exists. |
| batchSize                        | 1000      | Maximum number of messages written to Channel in one batch   |
| batchDurationMillis              | 1000      | Maximum time (in ms) before a batch will be written to Channel The batch will be written whenever the first of size and time will be reached. |
| backoffSleepIncrement            | 1000      | Initial and incremental wait time that is triggered when a Kafka Topic appears to be empty. Wait period will reduce aggressive pinging of an empty Kafka Topic. One second is ideal for ingestion use cases but a lower value may be required for low latency operations with interceptors. |
| maxBackoffSleep                  | 5000      | Maximum wait time that is triggered when a Kafka Topic appears to be empty. Five seconds is ideal for ingestion use cases but a lower value may be required for low latency operations with interceptors. |
| useFlumeEventFormat              | false     | By default events are taken as bytes from the Kafka topic directly into the event body. Set to true to read events as the Flume Avro binary format. Used in conjunction with the same property on the KafkaSink or with the parseAsFlumeEvent property on the Kafka Channel this will preserve any Flume headers sent on the producing side. |
| setTopicHeader                   | true      | When set to true, stores the topic of the retrieved message into a header, defined by the `topicHeader` property. |
| topicHeader                      | topic     | Defines the name of the header in which to store the name of the topic the message was received from, if the `setTopicHeader` property is set to `true`. Care should be taken if combining with the Kafka Sink `topicHeader` property so as to avoid sending the message back to the same topic in a loop. |
| kafka.consumer.security.protocol | PLAINTEXT | Set to SASL_PLAINTEXT, SASL_SSL or SSL if writing to Kafka using some level of security. See below for additional info on secure setup. |
| *more consumer security props*   |           | If using SASL_PLAINTEXT, SASL_SSL or SSL refer to [Kafka security](http://kafka.apache.org/documentation.html#security) for additional properties that need to be set on consumer. |
| Other Kafka Consumer Properties  | –         | These properties are used to configure the Kafka Consumer. Any consumer property supported by Kafka can be used. The only requirement is to prepend the property name with the prefix `kafka.consumer`. For example: `kafka.consumer.auto.offset.reset` |

```properties
tier1.sources.source1.type = org.apache.flume.source.kafka.KafkaSource
tier1.sources.source1.channels = channel1
tier1.sources.source1.batchSize = 5000
tier1.sources.source1.batchDurationMillis = 2000
tier1.sources.source1.kafka.bootstrap.servers = localhost:9092
tier1.sources.source1.kafka.topics = test1, test2
tier1.sources.source1.kafka.consumer.group.id = custom.g.id
```





### Channel管道：

- **Memory Channel**
  - event保存在Java Heap中。如果允许数据小量丢失，推荐使用

- **File Channel**
  - event保存在本地文件中，可靠性高，但吞吐量低于Memory Channel

- **JDBC Channel**
  - event保存在关系数据中，一般不推荐使用

- **Kafka Channel**



### Sink输出地：

#### Avro sink：

- 作为avro客户端向avro服务端发送avro事件

| **属性**     | **缺省值** | **描述**             |
| ------------ | ---------- | -------------------- |
| **type**     | **-**      | **avro**             |
| **hostname** | **-**      | **服务端**IP**地址** |
| **post**     | **-**      | **端口**             |
| batch-size   | 100        | 批量发送事件数量     |



#### HDFS sink：

- 将事件写入Hadoop分布式文件系统（HDFS）

| **属性**        | **缺省值** | **描述**     |
| --------------- | ---------- | ------------ |
| **type**        | **-**      | **hdfs**     |
| **hdfs.path**   | **-**      | **hdfs**目录 |
| hfds.filePrefix | FlumeData  | 文件前缀     |
| hdfs.fileSuffix | -          | 文件后缀     |

```properties
a2.channels = c2
a2.sources = s2
a2.sinks = k2


a2.sources.s2.type = spooldir
a2.sources.s2.spoolDir = /opt/datas
a2.sources.s2.channels = c2

a2.channels.c2.type = memory
a2.channels.c2.capacity = 10000
a2.channels.c2.transactionCapacity = 1000


a2.sinks.k2.type = hdfs
a2.sinks.k2.hdfs.path = hdfs://192.168.56.101:9000/flume/customs
a2.sinks.k2.hdfs.filePrefix = events-
a2.sinks.k2.rollCount = 5000
a2.sinks.k2.rollSize = 600000
a2.sinks.k2.batchSize = 500

a2.sinks.k2.channel = c2
```



#### Hive sink：

- 包含分隔文本或JSON数据流事件直接进入Hive表或分区

- 传入的事件数据字段映射到Hive表中相应的列

|      **属性**      | **缺省值** |                           **描述**                           |
| :----------------: | :--------: | :----------------------------------------------------------: |
|      **type**      |   **-**    |                           **hive**                           |
| **hive.metastore** |   **-**    |                   **Hive  metastore URI**                    |
| **hive.database**  |   **-**    |                    **Hive****数据库名称**                    |
|   **hive.table**   |   **-**    |                        **Hive****表**                        |
|   **serializer**   |   **-**    | **序列化器负责从事件中**分析出字段**并将它们映射为**Hive表中的列。序列化器的选择取决于数据的格式。支持序列化器:DELIMITED和JSON |

#### HBase sink：

|         **属性**         |                       **缺省值**                       |          **描述**          |
| :----------------------: | :----------------------------------------------------: | :------------------------: |
|         **type**         |                         **-**                          |         **hbase**          |
|        **table**         |                         **-**                          |  **要写入的  Hbase 表名**  |
|     **columnFamily**     |                         **-**                          |  **要写入的  Hbase 列族**  |
|     zookeeperQuorum      |                           -                            | 对应hbase.zookeeper.quorum |
|       znodeParent        |                         /hbase                         |   zookeeper.znode.parent   |
|        serializer        | org.apache.flume.sink.hbase.SimpleHbaseEventSerializer |      一次事件插入一列      |
| serializer.payloadColumn |                           -                            |          列名col1          |



#### Kafka sink：

> This is a Flume Sink implementation that can publish data to a [Kafka](http://kafka.apache.org/) topic. One of the objective is to integrate Flume with Kafka so that pull based processing systems can process the data coming through various Flume sources.

> This currently supports Kafka server releases 0.10.1.0 or higher. Testing was done up to 2.0.1 that was the highest avilable version at the time of the release.

Required properties are marked in bold font.

| Property Name                    | Default             | Description                                                  |
| :------------------------------- | :------------------ | :----------------------------------------------------------- |
| **type**                         | –                   | Must be set to `org.apache.flume.sink.kafka.KafkaSink`       |
| **kafka.bootstrap.servers**      | –                   | List of brokers Kafka-Sink will connect to, to get the list of topic partitions This can be a partial list of brokers, but we recommend at least two for HA. The format is comma separated list of hostname:port |
| kafka.topic                      | default-flume-topic | The topic in Kafka to which the messages will be published. If this parameter is configured, messages will be published to this topic. If the event header contains a “topic” field, the event will be published to that topic overriding the topic configured here. Arbitrary header substitution is supported, eg. %{header} is replaced with value of event header named “header”. (If using the substitution, it is recommended to set “auto.create.topics.enable” property of Kafka broker to true.) |
| flumeBatchSize                   | 100                 | How many messages to process in one batch. Larger batches improve throughput while adding latency. |
| kafka.producer.acks              | 1                   | How many replicas must acknowledge a message before its considered successfully written. Accepted values are 0 (Never wait for acknowledgement), 1 (wait for leader only), -1 (wait for all replicas) Set this to -1 to avoid data loss in some cases of leader failure. |
| useFlumeEventFormat              | false               | By default events are put as bytes onto the Kafka topic directly from the event body. Set to true to store events as the Flume Avro binary format. Used in conjunction with the same property on the KafkaSource or with the parseAsFlumeEvent property on the Kafka Channel this will preserve any Flume headers for the producing side. |
| defaultPartitionId               | –                   | Specifies a Kafka partition ID (integer) for all events in this channel to be sent to, unless overriden by `partitionIdHeader`. By default, if this property is not set, events will be distributed by the Kafka Producer’s partitioner - including by `key` if specified (or by a partitioner specified by `kafka.partitioner.class`). |
| partitionIdHeader                | –                   | When set, the sink will take the value of the field named using the value of this property from the event header and send the message to the specified partition of the topic. If the value represents an invalid partition, an EventDeliveryException will be thrown. If the header value is present then this setting overrides `defaultPartitionId`. |
| allowTopicOverride               | true                | When set, the sink will allow a message to be produced into a topic specified by the `topicHeader` property (if provided). |
| topicHeader                      | topic               | When set in conjunction with `allowTopicOverride` will produce a message into the value of the header named using the value of this property. Care should be taken when using in conjunction with the Kafka Source `topicHeader`property to avoid creating a loopback. |
| kafka.producer.security.protocol | PLAINTEXT           | Set to SASL_PLAINTEXT, SASL_SSL or SSL if writing to Kafka using some level of security. See below for additional info on secure setup. |
| *more producer security props*   |                     | If using SASL_PLAINTEXT, SASL_SSL or SSL refer to [Kafka security](http://kafka.apache.org/documentation.html#security) for additional properties that need to be set on producer. |
| Other Kafka Producer Properties  | –                   | These properties are used to configure the Kafka Producer. Any producer property supported by Kafka can be used. The only requirement is to prepend the property name with the prefix `kafka.producer`. For example: kafka.producer.linger.ms |

Note

 

Kafka Sink uses the `topic` and `key` properties from the FlumeEvent headers to send events to Kafka. If `topic` exists in the headers, the event will be sent to that specific topic, overriding the topic configured for the Sink. If `key` exists in the headers, the key will used by Kafka to partition the data between the topic partitions. Events with same key will be sent to the same partition. If the key is null, events will be sent to random partitions.

The Kafka sink also provides defaults for the key.serializer(org.apache.kafka.common.serialization.StringSerializer) and value.serializer(org.apache.kafka.common.serialization.ByteArraySerializer). Modification of these parameters is not recommended.

Deprecated Properties

| Property Name | Default             | Description                 |
| :------------ | :------------------ | :-------------------------- |
| brokerList    | –                   | Use kafka.bootstrap.servers |
| topic         | default-flume-topic | Use kafka.topic             |
| batchSize     | 100                 | Use kafka.flumeBatchSize    |
| requiredAcks  | 1                   | Use kafka.producer.acks     |

> An example configuration of a Kafka sink is given below. Properties starting with the prefix `kafka.producer` the Kafka producer. The properties that are passed when creating the Kafka producer are not limited to the properties given in this example. Also it is possible to include your custom properties here and access them inside the preprocessor through the Flume Context object passed in as a method argument.

```properties
a1.sinks.k1.channel = c1
a1.sinks.k1.type = org.apache.flume.sink.kafka.KafkaSink
a1.sinks.k1.kafka.topic = mytopic
a1.sinks.k1.kafka.bootstrap.servers = localhost:9092
a1.sinks.k1.kafka.flumeBatchSize = 20
a1.sinks.k1.kafka.producer.acks = 1
a1.sinks.k1.kafka.producer.linger.ms = 1
a1.sinks.k1.kafka.producer.compression.type = snappy
```

![image-20200804171250274](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200804171250274.png)

```properties
a2.channels = c2
a2.sources = s2
a2.sinks = k2


a2.sources.s2.type = spooldir
a2.sources.s2.spoolDir = /opt/datas
a2.sources.s2.channels = c2

a2.channels.c2.type = memory
a2.channels.c2.capacity = 10000
a2.channels.c2.transactionCapacity = 1000


a2.sinks.k2.type = hdfs
a2.sinks.k2.hdfs.path = hdfs://192.168.56.101:9000/flume/customs
a2.sinks.k2.hdfs.filePrefix = events-
a2.sinks.k2.rollCount = 5000
a2.sinks.k2.rollSize = 600000
a2.sinks.k2.batchSize = 500

a2.sinks.k2.channel = c2
```

#### 



