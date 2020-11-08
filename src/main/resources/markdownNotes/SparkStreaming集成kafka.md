## SparkStreaming集成kafka：

> SparkStreaming提供了两种方式对接kafka数据源:Receiver,Direct

> streaming-kafka0.10之后已经不在支持receiver

### Direct方式：

> Spark1.3之后引入

- `周期性的查询kafka`，获取每个partition的最新的offset，从而定义每个batch的offset范围。当处理数据的 job 启动时，就会使用 Kafka 的简单 consumer api来获取 Kafka 指定 offset 范围的数据。 

- `采用kafka的consumer api方式读取数据`：当batch任务触发时，由executor读取数据，并参与到其他executor的数据计算过程中去，driver来决定读取多少offsets，并将offsets交由checkpoints来维护。将触发下次batch任务，再由executor读取kafka数据并计算。

### Direct优点：

1. `简化并行读取`：

   > 读取多个partition，不需要**创建多个DStream**，然后对他们进行union操作，**spark会自动创建和kafka partition一样多的RDD partition**，且并行的从Kafka中读取。

2. `高性能`：

   > 由于kafka本身就有高可靠的机制，会对数据复制，所以只要从kafka中通过kafka的副本进行恢复即可。

3. `一次且仅一次的事务机制`：

   > 基于 direct 的方式，使用 kafka 的简单 api，Spark Streaming 自己就负责追踪消费的 offset，并保存在 checkpoint 中。Spark 自己一定是同步的，因此可以保证数据是消费一次且仅消费一次。 

### KafkaUtils.createDirectStream()三个参数：

1. `ssc : StreamingContext`：流处理上下文类

2. `LocationStrategies `： Consumer 调度分区的位置策略

   - `LocationStrategies.PreferConsistent` ：

     > **每个 Spark Executor 作 为 一 个Consumer**，**Executor 与 Kafka Partition 一对一** 。**大多数情况下使用**，主要是为了均匀分布。

   - `LocationStrategies.PreferBrokers`：

     > 每个 Spark Executor 与 Kafka Broker 在相同 HOST 上。也就是说 Spark Executor 优先分配到 Kafka Broker 上。 

   - `LocationStrategies.PreferFixed`：

     > Spark Executor 与 Kafka Partition 使用固定的映射（fixed mapping）。如果负载不均衡，可以通过这种方式来手动指定分配方式，当其他没有在 fixed mapping 中指定的，均采用 
     > PreferConsistent 方式分配。

3. `ConsumerStrategies`: 指消费策略。

   -  `ConsumerStrategies.Subscribe`：允许订阅固定的主题集合 
   -  `ConsumerStrategies.Assign`：指定固定的分区集合。 

### 集成kafka实战代码（scala语言）

> sparkstreaming从kafka中拉取数据进行流处理后再放入Kafka分区中

> 应用程序是部署在**YARN群集**上的长时间运行的Spark Streaming作业。该job从Kafka中接收数据，校验数据，将其转换成Avro二进制格式，并将其发送到另一个Kafka的topic

#### Producer发送问题：

>  producer是在driver上创建，但消息被发送到executor。**这个producer与Kafka的brokers保持套接字连接**，以至于它不能被序列化和在网络中发送

##### 解决办法一：

把创建producer的方法写在每个分区里，也就是在executor上都各自发送消息的时候创建和关闭producer，就逃避了序列化，

>  **缺陷：**每个消息都会创建和关闭producer。与集群建立连接是需要时间的，由于Kafka procuder需要在所有的分区中查找leaders，所以它比打开一个普通的套接字连接更耗时

##### 解决办法二：

使用foreachpartition进行一个个的分区处理，相比之前一个个消息都创建一个，这个方法创建的producer对象更少，因为同一个分区在同一个executor上，同样避免了序列化，而且分区内消息相互之间共享一个producer，节省创建关闭的连接大开销。

##### 解决办法三：

> 优化：广播和懒加载

方法二在大数据量下，仍然要创建很多producer，

1. 我们对此使用**广播**的方式，让所有的executor都只用一个producer实例变量。
2. 同时我们要避免序列化producer，所以我们**广播的是创建producer的方法**，具体的对象可以在executor执行端创建，这样就避免了序列化复杂的producer对象。
3. 而且我们同时再使用**懒加载的方式**，不用再dirver端就广播，让它延迟加载在运行到发送数据代码的再开始创建。
4. 如果我们在driver端有**多个流需要我们进行处理和发送**，我们此时只需要一个创建producer的方法实例即可，我们需要这里开一个单例工厂去完成更复杂的情景。
5. 在executor的JVM关闭之前，我们**必须关闭Kafka procuder**。缺少这一步，Kafka procuder内部缓冲的所有消息都将丢失

进化到第三步我们开始写代码：

`KafkaSinks：`

```js
package com.wyw.test1
import java.util.Properties
import org.apache.kafka.clients.producer.{KafkaProducer, ProducerRecord}


// 多线程产生连接
class KafkaSinks[K,V](fc: () => KafkaProducer[K,V]) extends Serializable {

 //延迟到exectuor端创建producer对象
  lazy val producer: KafkaProducer[K, V] = fc()

  def send(topic: String, key: K,value: V) = {
    producer.send(new ProducerRecord[K,V](topic, key, value))
  }

  def send(topic: String,value: V) = {
    producer.send(new ProducerRecord[K,V](topic, value))

  }
}


object KafkaSinks {
  import scala.collection.JavaConversions._
  def apply[K,V](conf: Map[String,Object]): KafkaSinks[K,V] = {
    // 创建一个new类需要得匿名函数
    val func = () => {
      val prod = new KafkaProducer[K, V](conf)
      // executorJVM关闭时，producer也得关闭
      sys.addShutdownHook{
        prod.close()
      }
      prod
    }
    // new 创建producer对象方法的类
    new KafkaSinks[K,V](func)
  }

  def apply[K,V](conf: Properties): KafkaSinks[K,V] = apply(conf.toMap)



}
```

`ProducerMethodSingleDAO`：

driver端单例创建producer的方法，防止广播多次

```js
package com.wyw.test1

import java.util.Properties
import org.apache.spark.broadcast.Broadcast
import org.apache.spark.sql.SparkSession
import org.codehaus.jackson.map.ser.std.StringSerializer

object MySingleBaseDAO {
  @volatile private var  instance: Broadcast[KafkaSinks[String, String]] = null

  def getInstance() = {
    // 多线程有的会判空，有的不会判空
    if (instance == null) {
      val sc = SparkSession.builder().appName("kafka").master("local[*]").getOrCreate().sparkContext
      synchronized {
        if (instance == null) {
          val p = new Properties()
          p.setProperty("bootstrap.servers", "192.168.56.101:9092")
          p.setProperty("key.serializer", classOf[StringSerializer].getName)
          p.setProperty("value.serializer", classOf[StringSerializer].getName)

          instance = sc.broadcast(KafkaSinks[String,String](p))
        }
        instance
      }
    }
    instance
  }
}

```

`KafkaStreamKafkaConsumer:`

> 处理接收和发送的主代码

```js
package com.wyw.test1

import com.google.gson.Gson
import org.apache.kafka.clients.consumer.{ConsumerConfig, ConsumerRecord}
import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.streaming.dstream.InputDStream
import org.apache.spark.streaming.kafka010.{ConsumerStrategies, HasOffsetRanges, KafkaUtils, LocationStrategies}
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.{SparkConf, SparkContext}
import shaded.parquet.org.slf4j.LoggerFactory

object FlumeKafkaStreamConsumer {
  private val LOG = LoggerFactory.getLogger("Kafka2KafkaStreaming")
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("local[2]").setAppName("mykafka")
    val sc: SparkContext = new SparkContext(conf)
    // 流处理上下文类
    val ssc: StreamingContext = new StreamingContext(sc, Seconds(5))

    // 因为有状态DStream，所以必须要有记录
//    ssc.checkpoint("e:\\大数据\\mykafka-log")

    // 创建连接kafka服务器参数
    val kafkaParam = Map(
      ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG -> "192.168.56.101:9092",
      // 选定一组消费者去读数据，
      ConsumerConfig.GROUP_ID_CONFIG -> "flumeKafkaStream5",
      ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG -> "true",
      ConsumerConfig.AUTO_COMMIT_INTERVAL_MS_CONFIG -> "20000",
      // 每组消费者读完会把指针读到末尾无法返回，这个配置将指针放到开头
      ConsumerConfig.AUTO_OFFSET_RESET_CONFIG -> "earliest",
      ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG -> classOf[StringDeserializer],
      ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG -> classOf[StringDeserializer]
    )



    // 创建Direct流, 
    val streams: InputDStream[ConsumerRecord[String, String]] = KafkaUtils.createDirectStream(ssc, LocationStrategies.PreferConsistent,
      ConsumerStrategies.Subscribe[String, String](Set("flumeKafkaStream5"), kafkaParam))

    val kafkaProducer = MySingleBaseDAO.getInstance()
// 非单例代码
//    val kafkaProducer: Broadcast[KafkaSinks[String, String]] = {
//      val kafkaProducerConfig = {
//        val p = new Properties()
//        p.setProperty("bootstrap.servers", "192.168.56.101:9092")
//        p.setProperty("key.serializer", classOf[StringSerializer].getName)
//        p.setProperty("value.serializer", classOf[StringSerializer].getName)
//        p
//      }
//      if (LOG.isInfoEnabled)
//        LOG.info("kafka producer init done!")
//      ssc.sparkContext.broadcast(KafkaSinks[String, String](kafkaProducerConfig))
//    }




    streams.foreachRDD(rdd => {
      val offsetRanges = rdd.asInstanceOf[HasOffsetRanges].offsetRanges

      // 如果rdd有数据
      if (!rdd.isEmpty()) {
        // 代码在将会在每个executor里执行处理数据
        rdd
          .map(_.value())
          .filter(_.split(",").size > 1)
          .flatMap(line => {
            val ids = line.split(",")
            ids(1).split(" ").map(word => (ids(0), word))
          })
          .foreachPartition(partition => {
            // 使用广播变量发送到Kafka
            partition.foreach(record => {
              kafkaProducer.value.send("flumeKafkaStream6", new Gson().toJson(record))
            })
          })
      }
    })


    ssc.start()
    ssc.awaitTermination()
  }

}

```

