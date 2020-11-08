## SparkSQL和集成数据源-及简单优化：



### SparkSQL优化器--Catalyst Optimizer

> Catalyst是Spark SQL的核心

![image-20200730142150706](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200730142150706.png)

**Catalyst Optimizer**：**Catalyst**优化器，将逻辑计划转为物理计划

#### 具体流程：

- 代码转化为逻辑计划

- 优化
  - 在投影上面查询过滤器
  - 检查过滤是否可下压
- 转化为物理计划

### Spark SQL API ：

- SparkContext
- SQLContext
  - Spark SQL编程入口
- HiveContext
  - SQLContext的子集，包含更多功能
- SparkSession

### 具体优化流程：

#### 原流程：

```sql
select name from
(
	select id,name from people
) p
where p.id = 1
```

1. 先运行子查询
2. 开始scan people
3. 选择字段id，name
4. 运行where，filter掉id字段
5. 选择字段name

#### 优化流程：

> - 在投影（select）上面查询过滤器
> - 检查过滤是否可下压

1. 先运行子查询
2. 开始scan people
3. 运行where，filter掉id字段
4. 选择字段name

![image-20200730150339134](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200730150339134.png)


### DataSet与DataFrame操作

- **DataSet** =  RDD + Schema
  - 特定域对象中的强类型集合

> **createDataset()**的参数可以是：**Seq**、**Array**、**RDD**

```js
case class Point(label:String,x:Double,y:Double)
case class Category(id:Long,name:String)
val pointsRDD=sc.parallelize(List(("bar",3.0,5.6),("foo",-1.0,3.0)))
val categoriesRDD=sc.parallelize(List((1,"foo"),(2,"bar")))
val points=pointsRDD.map(line=>Point(line._1,line._2,line._3)).toDS
val categories=categories.map(line=>Category(line._1,line._2)).toDS
points.join(categories,points("label")===categories("name")).show

```

![image-20200812095024738](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200812095024738.png)

- **DataFrame** = DataSet[Row]

  - 类似二维表格

  - 在RDD基础上加入了Schema数据结构信息

  - DataFrame Schema支持嵌套数据类型

    - struct
    - map
    - array

    

### Spark SQL操作外部数据源

- #### Parquet文件：

  > **是一种流行的列式存储格式，以二进制存储，文件中包含数据与元数据**

  - 写parquet文件

  ```js
  val schema=StructType(Array(StructField("name",StringType),
  					        StructField("favorite_color",StringType),
  					        StructField("favorite_numbers",ArrayType(IntegerType))))
  val rdd=sc.parallelize(List(("Alyssa",null,Array(3,9,15,20)),("Ben","red",null)))
  val rowRDD=rdd.map(p=>Row(p._1,p._2,p._3))
  val df=spark.createDataFrame(rowRDD,schema)
  df.write.parquet("/data/users")	//在该目录下生成parquet文件
  
  ```

  - 读parquet文件

  ```js
  val df=spark.read.parquet("/data/users")	//该目录下存在parquet文件
  df.show
  df.printSchema
  ```

- #### Hive数据源集成：

  - Hive在idea配置：

  > **1**、**hive-site.xml，core-site.xml
  > hdfs-site.xml拷贝至**resource包**下**
  >
  > **2**、导porn.xml依赖包
  >
  > **3**、自行创建**SparkSession**，启用**Hive**支持

  ```xml
      <!-- https://mvnrepository.com/artifact/org.apache.spark/spark-hive -->
      <dependency>
        <groupId>org.apache.spark</groupId>
        <artifactId>spark-hive_2.11</artifactId>
        <version>2.3.4</version>
      </dependency>
  ```

  ```js
  val spark = SparkSession.builder()
  .appName("wyw")
  .master("local[*]")
  .enableHiveSupport()
  .getOrCreate()
  
  ```

- #### Mysql数据源集成：

  ```js
  $spark-shell --jars /opt/spark/ext_jars/mysql-connector-java-5.1.38.jar
  
  val url = "jdbc:mysql://localhost:3306/metastore"
  val tableName = "TBLS"
  // 设置连接用户、密码、数据库驱动类
  val prop = new java.util.Properties
  prop.setProperty("user","hive")
  prop.setProperty("password","mypassword")
  prop.setProperty("driver","com.mysql.jdbc.Driver")
  // 取得该表数据
  val jdbcDF = spark.read.jdbc(url,tableName,prop)
  jdbcDF.show
  //DF存为新的表
  jdbcDF.write.mode("append").jdbc(url,"t1",prop)
  ```

  

### Spark函数UDF使用：

- SparkSession.udf.register()：只在sql()中有效

```js
import spark.implicits._
//注册自定义函数，注意是匿名函数
spark.udf.register("hobby_num", (s: String) => s.split(',').size)
spark.sql("select name, hobbies, hobby_num(hobbies) as hobby_num from hobbies").show

```

- functions.udf()：对DataFrame API均有效

```js
val scoreTransaction = udf{score: String => {
  score.toInt match {
    case x if x > 85 => "A"
    case x if x > 70 => "B"
    case x if x > 60 => "C"
    case _ => "D"
  }
}
```





### Spark性能优化

#### 一：序列化：

> java序列化，spark默认方式

- kryo序列化，比java序列化快约10倍

```js
conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer");
//向Kryo注册自定义类型
conf.registerKryoClasses(Array(classOf[MyClass1], classOf[MyClass2]));

```

> **如果没有注册需要序列化的class，Kyro依然可以照常工作，但会存储每个对象的全类名(full class name)，这样往往比默认的 Java serialization** **更**浪费空间

#### 二：使用对象数组

#### 三：避免嵌套结构

#### 四：**尽量使用数字作为**Key，而非字符串

#### 五：以较大的**RDD**使用MEMORY_ONLY_SER

#### 六：**加载**CSV**、**JSON**时，仅加载所需字段**

#### 七：**仅在需要时持久化中间结果**（**RDD/DS/DF**）

#### 八：避免不必要的中间结果（**RDD/DS/DF**）的生成

#### 九：**DF的执行速度**比**DS快约**3倍

