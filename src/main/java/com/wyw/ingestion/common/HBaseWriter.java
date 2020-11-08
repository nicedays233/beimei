package com.wyw.ingestion.common;

import com.wyw.ingestion.config.IT21Config;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.ConnectionFactory;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Table;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;

import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

public class HBaseWriter implements Persistable {
	//core-site xml file
	private String coreSite = null;
	//hdfs-site xml file
	private String hdfsSite = null;
	//hbase-site xml file
	private String hbaseSite = null;

	//the hbase table
	private String hbTable = null;

	//the parser kafka传过来的record转义成hbase的record
	private Parsable<Put> parser = null;

	//constructor
	public HBaseWriter(String hbTable, Parsable<Put> parser) {
		//set
		this.hbTable = hbTable;
		this.parser = parser;
	}

	//initialize to extract the hbase-site configuration
	@Override
	public void initialize(Properties props) {
		//core-site
		this.coreSite = props.getProperty(IT21Config.coreSite);
		//hdfs-site
		this.hdfsSite = props.getProperty(IT21Config.hdfsSite);
		//hbase
		this.hbaseSite = props.getProperty(IT21Config.hbaseSite);
	}

	//write
	@Override
	public int write(ConsumerRecords<String, String> records) throws Exception {
		//the # of records puts
		int numPuts = 0;
		//check
		if ( this.hbaseSite == null || this.hbaseSite.isEmpty() ) {
			//error out
			throw new Exception("The hbase-site.xml is not initialized.");
		}
		//configuration 工作中最好这样，不太赞同master什么什么连接
		Configuration cfg = HBaseConfiguration.create();
		//check
		if ( this.coreSite != null ) {
			//set resource
			cfg.addResource( new Path(this.coreSite) );
		}
		if ( this.hdfsSite != null ) {
			//set resource
			cfg.addResource( new Path(this.hdfsSite) );
		}
		//the hbase-site
		cfg.addResource( new Path(this.hbaseSite) );

		//establish a connection
		Connection conn = ConnectionFactory.createConnection( cfg );
		try {
			//HTable
			Table tbl = conn.getTable( TableName.valueOf(this.hbTable) );
			try {
				//collection
				List<Put> puts = new ArrayList<Put>();
				//flags
				long passHead = 0;
				//loop
				for ( ConsumerRecord<String, String> record : records ) {
					try {
						//parse event record
						String[] elements = record.value().split(",", -1);
						//check if the head has been passed
						if ( passHead == 0 && this.parser.isHeader(elements) ) {
							//flag
							passHead = 1;
							//skip
							continue;
						}

						//parse
						if ( this.parser.isValid(elements) ) {
							//add 解析record变成put
							puts.add( this.parser.parse(elements) );
						}
						else {
							//print error
							System.out.println(String.format("ErrorOccured: invalid message found when writing to HBase! - %s", record.value()));
						}
					}
					catch (Exception e ) {
						//print error
						System.out.println("ErrorOccured: " + e.getMessage());
					}
				}
				//check
				if ( puts.size() > 0 ) {
					//save
					tbl.put( puts );
				}

				//set
				numPuts = puts.size();
			}
			finally {
				//close the table
				tbl.close();
			}
		}
		finally {
			//close the connection
		    conn.close();
	    }
		return numPuts;
	}
}
