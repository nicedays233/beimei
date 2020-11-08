package com.wyw.ingestion;

import com.wyw.ingestion.kafka.*;
import com.wyw.ingestion.kafka.streaming.EventAttendeesStreamer;
import com.wyw.ingestion.kafka.streaming.UserFriendsStreamer;

public class AnyConsumer implements IngestionExecutor {
	//runnable
	class ConsumeExecutor implements Runnable {
		//the it21 consumer
		private IngestionExecutor executor = null;
		//the arguments
		private String[] args = null;

		//constructor
		public ConsumeExecutor(IngestionExecutor executor, String[] args) {
			//set
			this.executor = executor;
			this.args = args;
		}

		//run
		public void run() {
			//check
			if ( executor != null ) {
				//run consumer
				try {
					//run
					executor.execute(args);
				}
				catch (Exception e) {
					//print
					e.printStackTrace();
				}
			}
		}

		//start
		public void start() {
			//check
			if ( executor != null ) {
				//start a new thread
				(new Thread(this, executor.getClass().getName())).start();
			}
		}
	}

	//main entry
	@Override
	public void execute(String[] args) throws Exception {
		//check
		if (args.length < 1) {
			System.out.println(String.format("Usage: %s <settings-file>", this.getClass().getName()));
			System.out.println("<settings-file>: the configuration settings");
		}
		else {
			System.out.println("启动streamer");
			//user-friends streamer
			(new ConsumeExecutor(new UserFriendsStreamer(), args)).start();
			//user-friends streamer
			(new ConsumeExecutor(new EventAttendeesStreamer(), args)).start();

			//the # of executors
			int numExecutors = 3;
			try {
				for ( int i = 0; i < numExecutors; i++ ) {
					System.out.println("启动consumer第" + i + "次");
					//users consumer
					(new ConsumeExecutor(new UserConsumer(), args)).start();
					//user-friends consumer
					(new ConsumeExecutor(new UserFriendsConsumer(), args)).start();

					//events consumer
					(new ConsumeExecutor(new EventConsumer(), args)).start();
					//event-attendees consumer
					(new ConsumeExecutor(new EventAttendeesConsumer(), args)).start();

					//train consumer
					(new ConsumeExecutor(new TrainConsumer(), args)).start();
				}
			}
			catch ( Exception e ) {
				//print error
				e.printStackTrace();
			}
		}
	}
}
