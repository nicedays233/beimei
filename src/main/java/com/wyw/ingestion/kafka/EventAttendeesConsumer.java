package com.wyw.ingestion.kafka;

import com.wyw.ingestion.common.HBaseWriter;
import com.wyw.ingestion.common.Persistable;

public class EventAttendeesConsumer extends IT21Consumer {
	//kafka topic
	@Override
	protected String getKafkaTopic() {
		return "event_attendees";
	}
	//the flag for how to commit the consumer reads
	@Override
	protected Boolean getKafkaAutoCommit() {
		return true;
	}
	//the max # of records polled
	@Override
	protected int getMaxPolledRecords() {
		return 9000;
	}
	//the max # of records polled
	@Override
	protected int getMaxPollIntervalMillis() {
		return 12000;
	}
	//consumer group
	@Override
	protected String getKafkaConsumerGrp() {
		return "grpEventAttendees";
	}

	//constructor
	public EventAttendeesConsumer() {
	}

	//writers
	@Override
	protected Persistable[] getWriters() {
		System.out.println("写event_attendees");
		return new Persistable[] {
//			new MongoWriter("event_attendee", new com.wyw.ingestion.data.mongo.EventAttendeesParser()),

			new HBaseWriter("events_db:event_attendee", new com.wyw.ingestion.data.hbase.EventAttendeesParser())
		};
	}
}
