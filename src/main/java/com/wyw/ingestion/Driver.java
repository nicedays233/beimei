package com.wyw.ingestion;



import java.util.Arrays;


public class Driver  {
//	the main entry
	public static void main(String[] args) throws Exception {
		//run
		new Driver().run(args);

	}

	//execute
	public void run(String... args) throws Exception {
		//check
		if ( args == null || args.length < 1 ) {
			//error out
			throw new Exception("Please specify the executor class.");
		}

		//java -jar event-ingestion-1.0.0.jar com.wyw.ingestion.kafka.UserFriendStreamer settings.properties
		//create instance
		Object o = Class.forName(args[0]).newInstance();
		//check
		if ( o instanceof IngestionExecutor) {
			((IngestionExecutor)o).execute(Arrays.copyOfRange(args, 1, args.length));
		}
		else {
			//error out
			throw new Exception("The specified Executor is not an IngestionExecutor.");
		}
	}
}

