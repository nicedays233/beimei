package com.wyw.ingestion.kafka;

import com.wyw.ingestion.common.HBaseWriter;
import com.wyw.ingestion.common.Persistable;

public class TrainConsumer extends IT21Consumer {
	//kafka topic
	@Override
	protected String getKafkaTopic() {
		return "train";
	}
	//the flag for how to commit the consumer reads
	@Override
	protected Boolean getKafkaAutoCommit() {
		return false;
	}
	//the max # of records polled
	@Override
	protected int getMaxPolledRecords() {
		return 1000;
	}
	//the max # of records polled
	@Override
	protected int getMaxPollIntervalMillis() {
		return 3600;
	}
	//consumer group
	@Override
	protected String getKafkaConsumerGrp() {
		return "grpTrain";
	}

	//constructor
	public TrainConsumer() {
	}

	//writers
	@Override
	protected Persistable[] getWriters() {
		System.out.println("写train");
		return new Persistable[] {
//			new MongoWriter("train", new com.wyw.ingestion.data.mongo.TrainParser()),
			new HBaseWriter("events_db:train", new com.wyw.ingestion.data.hbase.TrainParser())
		};
	}
}
