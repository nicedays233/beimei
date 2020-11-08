package com.wyw.ingestion.kafka;

import com.wyw.ingestion.common.HBaseWriter;
import com.wyw.ingestion.common.Persistable;

public class EventConsumer extends IT21Consumer {
	//kafka topic
	@Override
	protected String getKafkaTopic() {
		return "events";
	}
	//the flag for how to commit the consumer reads
	@Override
	protected Boolean getKafkaAutoCommit() {
		return true;
	}
	//the max # of records polled
	@Override
	protected int getMaxPolledRecords() {
		return 3000;
	}
	//the max # of records polled
	@Override
	protected int getMaxPollIntervalMillis() {
		return 9000;
	}
	//consumer group
	@Override
	protected String getKafkaConsumerGrp() {
		return "grpEvents";
	}

	//constructor
	public EventConsumer() {
	}

	//writers
	@Override
	protected Persistable[] getWriters() {
		System.out.println("写events");
		return new Persistable[] {
//			new MongoWriter("events", new com.wyw.ingestion.data.mongo.EventParser()),
			new HBaseWriter("events_db:events", new com.wyw.ingestion.data.hbase.EventParser())
		};
	}
}
