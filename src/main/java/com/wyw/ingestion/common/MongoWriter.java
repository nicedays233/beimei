package com.wyw.ingestion.common;

import com.wyw.ingestion.config.IT21Config;
import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.Mongo;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;

import java.util.Properties;

//mongo writer
public class MongoWriter implements Persistable {
    //mongo host
    private String mongoHost = "127.0.0.1";
    //port
    private int mongoPort = 27017;
    //database
    private String mongoDatabase = "events";

    //user
    private String mongoUser = "it21";
    //password
    private String mongoPassword = "password";

    //mongo collection
    private String mongoCollection;

    //the parser
    private Parsable<Tuple<BasicDBObject, BasicDBObject>> parser;

    //constructor
    public MongoWriter(String mongoCollection, Parsable<Tuple<BasicDBObject, BasicDBObject>> parser) {
        //set
        this.mongoCollection = mongoCollection;
        this.parser = parser;
    }

    //initialize to extract the mongo configuration
    @Override
    public void initialize(Properties props) {
        //host
        this.mongoHost = props.getProperty(IT21Config.mongoHost);
        //port
        try {
            this.mongoPort = Integer.parseInt(props.getProperty(IT21Config.mongoPort));
        }
        catch (Exception e){
            //use default
            this.mongoPort = 27017;
        }
        //database
        this.mongoDatabase = props.getProperty(IT21Config.mongoDatabase);

        //user
        this.mongoUser = props.getProperty(IT21Config.mongoUser);
        //password
        this.mongoPassword = props.getProperty(IT21Config.mongoPwd);
    }

    //write
    @Override
	public int write(ConsumerRecords<String, String> records) throws Exception {
        //the # of records puts
        int numDocs = 0;

        //the mongo-client
        Mongo mongo = new Mongo(mongoHost, mongoPort);
        try {
            //database
            DB db = mongo.getDB(mongoDatabase);
            //check
            if (mongoUser != null && !mongoUser.isEmpty()) {
                //authenticate
                db.authenticate(mongoUser, mongoPassword.toCharArray());
            }

            //get the collection
            DBCollection collection = db.getCollection(mongoCollection);
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
                        //add
                        Tuple<BasicDBObject, BasicDBObject> kv = this.parser.parse(elements);
                        //update & insert
                        collection.update(kv.key, new BasicDBObject("$set", kv.value), true, false);

                        //set the counter
                        numDocs++;
                    }
                    else {
                        //print error
                        System.out.println(String.format("ErrorOccured: invalid message found when writing to MongoDB! - %s", record.value()));
                    }
                }
                catch (Exception e ) {
                    //print error
                    System.out.println("ErrorOccured: " + e.getMessage());
                }
            }

        }
        finally {
            //close
            mongo.close();
        }
        return numDocs;
    }
}
