## Spark写入数据库：

```js
url= jdbc:mysql://192.168.56.101:3306/kdc?useUnicode=true&characterEncoding=utf8
val props = new Properties()
props.put("user","root")
props.put("password", "123456")
dataframe.write.mode("overwrite").jdbc(url,"表名", props)
```

```js
// 不用往mysql建表，直接导入
dataframe.write
      .mode("overwrite")
      .format("jdbc")
      .option("url","jdbc:mysql://192.168.56.101:3306/myex")
      .option("dbtable", "xxx")
      .option("user", "root")
      .option("password", "123456")
      .save()
```

#### spark->hive

##### read

```scala
val spark = SparkSession.builder().master("local[*]").appName("name").enableHiveSupport()
		.config("hive.metastore.uris","thrift://192.168.56.100:9083")
		.config("spark.sql.warehouse.dir","hdfs://192.168.56.100:9000/user/hive/warehouse")
		.getOrCreate()
 val actions = spark.sql("select * from myexam.actions")
```

##### write

```scala
actions.write.option("spark.sql.hive.convertMetastoreParquet",false)
		.mode("append").saveAsTable("myexam.actions")
```





#### spark->hbase

##### read

```scala
val sparkConf = new SparkConf().setAppName("HBaseTest").setMaster("local[*]")
    val sc= new SparkContext(sparkConf)
    val tablename="zjw"
    val conf = HBaseConfiguration.create()

    conf.set("hbase.zookeeper.quorum","hj")
    conf.set("hbase.zookeeper.property.clientPort","2181")
    conf.set(TableInputFormat.INPUT_TABLE,tablename)

    val rdd1= sc.newAPIHadoopRDD(conf,classOf[TableInputFormat],
      classOf[org.apache.hadoop.hbase.io.ImmutableBytesWritable],
      classOf[org.apache.hadoop.hbase.client.Result]
    ).cache()

    println("count="+rdd1.count())
    //遍历输出
    rdd1.foreach({case (_,result) =>
      //通过result.getRow来获取行键
      val key = Bytes.toString(result.getRow)
      //通过result.getValue("列簇","列名")来获取值
      //需要使用getBytes将字符流转化为字节流
      val accuracy = Bytes.toString(result.getValue("sb".getBytes,"name".getBytes))
      val question_count = Bytes.toString(result.getValue("sb".getBytes,"age".getBytes))
      println(accuracy+" "+question_count)
    })
```

##### write

```scala
val spark = SparkSession.builder().appName("SparkHBaseRDD").master("local[*]").getOrCreate()
    val sc = spark.sparkContext
    val tablename = "zjw"
    val hbaseConf = HBaseConfiguration.create()
    hbaseConf.set("hbase.zookeeper.quorum","hj")  //设置zooKeeper集群地址，也可以通过将hbase-site.xml导入classpath，但是建议在程序里这样设置
    hbaseConf.set("hbase.zookeeper.property.clientPort", "2181")       //设置zookeeper连接端口，默认2181
    hbaseConf.set(TableOutputFormat.OUTPUT_TABLE, tablename)

    // 初始化job，TableOutputFormat 是 org.apache.hadoop.hbase.mapred 包下的
    val jobConf = new JobConf(hbaseConf)
    jobConf.setOutputFormat(classOf[TableOutputFormat])

    val indataRDD = sc.makeRDD(Array("2,jack,16", "1,Lucy,15", "5,mike,17", "3,Lily,14"))

    val rdd = indataRDD.map(_.split(',')).map{ arr=>
      /*一个Put对象就是一行记录，在构造方法中指定主键
       * 所有插入的数据 须用 org.apache.hadoop.hbase.util.Bytes.toBytes 转换
       * Put.addColumn 方法接收三个参数：列族，列名，数据*/
      val put = new Put(Bytes.toBytes(arr(0)))
      put.addColumn(Bytes.toBytes("sb"),Bytes.toBytes("name"),Bytes.toBytes(arr(1)))
      put.addColumn(Bytes.toBytes("sb"),Bytes.toBytes("age"),Bytes.toBytes(arr(2)))
      (new ImmutableBytesWritable, put)
    }
    rdd.saveAsHadoopDataset(jobConf)

    spark.stop()
```