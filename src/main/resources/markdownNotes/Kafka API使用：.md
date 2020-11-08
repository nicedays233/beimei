## Kafka API使用：

### Producer API

> Producer 是 Kafka 三大组件（Producer、Consumer、Broker）之一，用于发送消息给 kafka 集群。 



```java
package com.wyw.myKafka;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;

import java.util.Properties;

/**
 * @ClassName:MyProduct
 * @Author WYW
 * @Date07/08/202014:04
 * @Description: TODO
 * @Version V1.0
 **/
public class MyProduct {
	public static void main(String[] args) {
		Properties properties = new Properties();
		properties.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG,"192.168.56.101:9092");
		properties.put(ProducerConfig.ACKS_CONFIG,"all");
		properties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG,"org.apache.kafka.common.serialization.StringSerializer");
		properties.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,"org.apache.kafka.common.serialization.StringSerializer");
		Producer<String, String> producer = new KafkaProducer<>(properties);

		for (int i = 0; i < 10 ; i++) {
			producer.send(new ProducerRecord<String,String>("mytest","key:"+i,"value:"+i));
		}
		producer.close();

	}

}

```

（1）构造 Properties 对象， “bootstrap.servers、key.serializer、value.serializer”是必须指定的。 
（2）使用 Properties 构造 KafkaProducer 对象。 
（3）构造 ProducerRecord 指定 Topic、Partition、Key、Value。 
（4）使用 KafkaProducer 的 send()方法发送消息。 
（5）关闭 KafkaProducer。 

#### 下面对 ProducerReord、KafkaProducer 进行剖析

##### 1.ProductRecord用于封装发送给Broker的key-value对。内部数据结构包括：

Topic、PartitionID（可选）、Key（可选）、Value。可使用三种构造方法创建其实例：

```java
ProducerRecord(topic, partition, key, value) 
ProducerRecord(topic, key, value) 
ProducerRecord(topic, value) 
```

##### 2.KafkaProducer 实现了 Producer 接口，主要方法包括： 

➢ send()：实现消息发送主逻辑  
➢ close()：关闭 Producer  
➢ metrics()：获取 producer 的实时监控指标数据，比如发送消息的速率 
前面提到，Producer 可以以同步和异步的方式发送消息，便是通过
KafkaProducer 相应操作实现。

（1） Fire and Forget（发送后不再理会结果）

```java
 producer.send(new ProducerRecord<String, String>("topic1", Integer.toString(i), "dd:"+i));  
```

（2）同步发送，以阻塞方式发送。 

通过 producer.send(record)返回 Future 对象，通过调用 Future.get()进行无限等待结果返回

```java
producer.send(record).get() 
```



```java
package com.wyw.myKafka;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.producer.ProducerConfig;

import java.time.Duration;
import java.util.Arrays;
import java.util.Properties;

/**
 * @ClassName:MyConsumer
 * @Author WYW
 * @Date07/08/202015:08
 * @Description: TODO
 * @Version V1.0
 **/
public class MyConsumer {
	public static void main(String[] args) {
		Properties prop = new Properties();
		prop.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG,"192.168.56.101:9092");
		// 选定一组消费者去读数据，
		prop.put(ConsumerConfig.GROUP_ID_CONFIG,"test2");
		prop.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG,"true");
		prop.put(ConsumerConfig.AUTO_COMMIT_INTERVAL_MS_CONFIG,"1000");
		// 每组消费者读完会把指针读到末尾无法返回，这个配置将指针放到开头
		prop.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG,"earliest");
		prop.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG,"org.apache.kafka.common.serialization.StringDeserializer");
		prop.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG,"org.apache.kafka.common.serialization.StringDeserializer");
		KafkaConsumer<String,String> cons = new KafkaConsumer<>(prop);
		cons.subscribe(Arrays.asList("mytest"));
		while (true) {
			ConsumerRecords<String, String> records = cons.poll(Duration.ofSeconds(1));
			for (ConsumerRecord<String, String> record: records) {
				System.out.println(record.partition() + ":" + record.offset() + ":" + record.key() + " :" + record.value());
			}
		}
	}
}

```

