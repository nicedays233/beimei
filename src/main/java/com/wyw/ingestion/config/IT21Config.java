package com.wyw.ingestion.config;

import java.io.*;
import java.util.Properties;

public class IT21Config {
	//zoo-keeper url
	public final static String zooKeeperUrl = "zookeeperUrl";
	//broker url
	public final static String kafkaBrokerUrl = "brokerUrl";
	//state directory
	public final static String stateDir = "stateDir";

	//core-site
	public final static String coreSite = "coreSite";
	//hdfs-site
	public final static String hdfsSite = "hdfsSite";
	//hbase-site
	public final static String hbaseSite = "hbaseSite";

	//the host of the mongo server
	public final static String mongoHost = "mongoHost";
	//the port of the mongo server for client connection
	public final static String mongoPort = "mongoPort";
	//the target mongo database
	public final static String mongoDatabase = "mongoDatabase";
	//the user used for connecting to mongo
	public final static String mongoUser = "mongoUser";
	//password
	public final static String mongoPwd = "mongoPwd";

	//db jdbc-url
	public final static String dbJdbcUrl = "dbJdbcUrl";
	//user for connecting to db
	public final static String dbUser = "dbUser";
	//user's password
	public final static String dbPassword = "dbPassword";

	//load settings
	public static Properties loadSettings(String settingsFile) throws IOException {
		//the properties
		Properties props = new Properties();
		//open file
		FileInputStream input = new FileInputStream(settingsFile);
		try {
			//reader
			BufferedReader br = new BufferedReader(new InputStreamReader(input));
			try {
				//read first line
				String line = br.readLine();
				//loop for read
			    while ( line != null ) {
			    	//split
			    	String[] kv = line.split("=", -1);
			    	//check
			    	if ( kv != null && kv.length == 2 ) {
			    		//add
			    		props.put(kv[0], kv[1]);
			    	}
			    	//read next
			    	line = br.readLine();
			    }
			} finally {
				//close
				br.close();
			}
		} finally {
			//close
			input.close();
		}
		//extracts
		return props;
	}

	public static void main(String[] args) throws IOException {
/*		Properties props = new Properties();
		File file = new File(IT21Config.class.getResource("application.properties").getPath());
		System.out.println(file);*/
		FileInputStream input = new FileInputStream("application.properties");
		BufferedReader br = new BufferedReader(new InputStreamReader(input));
		System.out.println(br.readLine());


	}
}
