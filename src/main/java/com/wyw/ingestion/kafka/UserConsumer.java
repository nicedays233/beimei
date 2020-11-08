package com.wyw.ingestion.kafka;

import com.wyw.ingestion.common.HBaseWriter;
import com.wyw.ingestion.common.Persistable;

public class UserConsumer extends IT21Consumer {
	//kafka topic
	@Override
	protected String getKafkaTopic() {
		return "users";
	}
	//the flag for how to commit the consumer reads
	@Override
	protected Boolean getKafkaAutoCommit() {
		return false;
	}
	//the max # of records polled
	@Override
	protected int getMaxPolledRecords() {
		return 2000;
	}
	//the max # of records polled
	@Override
	protected int getMaxPollIntervalMillis() {
		return 6000;
	}
	//consumer group
	@Override
	protected String getKafkaConsumerGrp() {
		return "grpUsers";
	}

	//constructor
	public UserConsumer() {
	}

	//writers
	@Override
	protected Persistable[] getWriters() {
		System.out.println("写users");
		return new Persistable[] {
//			new MongoWriter("users", new com.wyw.ingestion.data.mongo.UserParser()),
			new HBaseWriter("events_db:users", new com.wyw.ingestion.data.hbase.UserParser())
		};
	}
}
