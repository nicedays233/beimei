## Hive函数-自定义函数-存储过程

### Hive函数：

#### `从输入输出角度分类：`

- **标准函数**
- **聚合函数**
- **表生成函数**

#### `从实现方式分类：`

- **内置函数：**
- **自定义函数：**
  - **UDF**
  - **UDAF**
  - **UDTF**

### Hive内置函数：

#### 标准函数：

- **字符函数：**

- ![image-20200720105633515](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200720105633515.png)

  ![image-20200615214701410](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200615214701410.png)

  ![image-20200727170347841](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200727170347841.png)

- **类型转换函数：**

  | **返回值** | **类型转换函数**           | **描述**                                                     |
  | ---------- | -------------------------- | ------------------------------------------------------------ |
  | **"type"** | **cast(expr  as <type>)**  | **将expr转换成type类型 如：cast("1" as  BIGINT) 将字符串1转换成了BIGINT类型** |
  | **binary** | **binary(string\|binary)** | **将输入的值转换成二进制**                                   |

- **数学函数：**

  ![](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200615135328005.png)

- **日期函数：**

  unix_timestamp("","yyyyMMdd")给字符串指定时间格式拿到毫秒时间

  ![image-20200615214841039](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200615214841039.png)

- **集合函数：**

  | **返回值**   | **函数**                             | **描述**                                               |
  | ------------ | ------------------------------------ | ------------------------------------------------------ |
  | **int**      | **size(Map<K.V>)**                   | **返回map中键值对个数**                                |
  | **int**      | **size(Array<T>)**                   | **返回数组的长度**                                     |
  | **array<K>** | **map_keys(Map<K.V>)**               | **返回map中的所有key**                                 |
  | **array<V>** | **map_values(Map<K.V>)**             | **返回map中的所有value**                               |
  | **boolean**  | **array_contains(Array<T>,  value)** | **如该数组Array<T>包含value返回true。，否则返回false** |
  | **array**    | **sort_array(Array<T>)**             | **对数组进行排序**                                     |

- **条件函数：**

  | **返回值**  | **函数**                                                     | **描述**                                                     |
  | ----------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
  | **T**       | **if(boolean  testCondition, T valueTrue, T valueFalseOrNull)** | **如果testCondition  为true就返回valueTrue,否则返回valueFalseOrNull** |
  | **T**       | **nvl(T  value, T default_value)**                           | **value为NULL返回default_value,否则返回value**               |
  | **T**       | **COALESCE(T  v1, T v2, ...)**                               | **返回第一非null的值，如果全部都为NULL就返回NULL**           |
  | **T**       | **CASE  a WHEN b THEN c   [WHEN  d THEN e]* [ELSE f] END**   | **如果a=b就返回c,a=d就返回e，否则返回f**                     |
  | **T**       | **CASE  WHEN a THEN b   [WHEN  c THEN d]* [ELSE e] END**     | **如果a=ture就返回b,c= ture就返回d,否则返回e**               |
  | **boolean** | **isnull(  a )**                                             | **如果a为null就返回true，否则返回false**                     |
  | **boolean** | **isnotnull  ( a )**                                         | **如果a为非null就返回true，否则返回false**                   |

#### 聚合函数：



#### 表生成函数：

| **返回值**  | **函数**                              | **描述**                                                     |
| ----------- | ------------------------------------- | ------------------------------------------------------------ |
| **N  rows** | **explode(array<T>)**                 | **对于array中的每个元素生成一行且包含该元素**                |
| **N  rows** | **explode(MAP)**                      | **每行对应每个map键值对  其中一个字段是map的键，另一个字段是map的值** |
| **N  rows** | **posexplode(ARRAY)**                 | **与explode类似，不同的是还返回各元素在数组中的位置**        |
| **N  rows** | **stack(INT  n, v_1, v_2, ..., v_k)** | **把k列转换成n行，每行有k/n个字段，其中n必须是常数**         |
| **tuple**   | **json_tuple(jsonStr,  k1, k2, ...)** | **从一个JSON字符串中获取多个键并作为一个元组返回，与get_json_object不同的是此函数能一次获取多个键值** |

### Hive的UDF：user-defined function

`UDF开发流程`

- **继承UDF类或GenericUDF类**

- **重写**evaluate()**方法并实现函数逻辑**

- **编译打包为jar文件**

- **复制到正确的**HDFS **路径**

- **使用jar创建临时/永久函数**

  - `临时函数`

  ```sql
    -- 临时函数仅对当前session(黑窗口)有效。 
    -- 添加jar包的两种方法 :
      	    临时加入jar包的命令
              方法一： add jar /home/hadoop/lib/hive-1.0-SNAPSHOT.jar; 
              方法二： 在hive的文件夹下面创建auxlib文件夹，将jar包上传到auxlib文件夹下面，重启hive。 
  ```

  ```sql
  语法：
  	CREATE TEMPORARY FUNCTION function_name AS class_name;   
  -- function_name函数名
  -- class_name 类路径，包名+类名 
  ```

  

  - `永久函数`---必须上传到HDFS上，hive是基于hadoop的

  ```sql
  --创建永久函数的语法: 
              CREATE FUNCTION [db_name.]function_name AS class_name 
              [using jar +FILE|ARCHIVE 'file_uri' [, JAR|FILE|ARCHIVE 'file_uri'] ]; 
  --# file_uri:是hdfs上的jar包目录 
  --添加jar包的两种方法: 
              -- hdfs上的根目录下创建lib文件夹  
              [hadoop@hadoop002 lib]$ hadoop fs -mkdir /lib  
  ```

  ```sql
  --创建永久函数：  
              hive> CREATE FUNCTION sayhello AS 'com.ruozedata.bigdata.HelloUDF' USING JAR 'hdfs://hadoop002:9000/lib/hive-1.0-SNAPSHOT.jar'; 
              converting to local hdfs://hadoop002:9000/lib/hive-1.0-SNAPSHOT.jar 
              Added [/tmp/22d50f26-5227-479e-9319-cb28985b8f5d_resources/hive-1.0-SNAPSHOT.jar] to class path 
              Added resources: [hdfs://hadoop002:9000/lib/hive-1.0-SNAPSHOT.jar] 
  ```

  

- **调用函数**

### HiveUDAF:用户自定义聚合函数：user-defined aggregate function

#### JAVA操作过程：

分为map, combiner,reduce三个阶段

#### map有init，iterator,terminatePartial

init初始化处理表格的集合，

iterator将数据处理填充集合并将它放到环状缓冲区里进行聚合，

terminatePartial将小集合发送到combiner阶段



#### combiner有terminatePartial和merge：

merge拿到小集合后进行再一次的聚合，形成一个大集合

terminatePartial将集合发送到reduce阶段

#### reduce有init,merge,terminate：

reduce端init再造集合来接收

merge端拿到各个机器的map集合进行聚合，

terminate将集合输出出去

当执行mapreduce时，我们会将一个表的数据分成多个map，一个map里会执行count聚合，一个map在环形缓冲区后溢出后聚合一次，最后还需要进行一次reduce再聚合统计，

---

### HiveUDTF:用户自定义表生成函数：-user-defined aggregate function

#### JAVA操作过程：

- **写出函数继承GenericUDTF类**，完成--输入一行--输出多行--的功能

- **initialize来确定列名，列数量和列类型。**

  ```java
  @Override
  	public StructObjectInspector initialize(StructObjectInspector argOIs) throws UDFArgumentException {
  		// 设置新列名和列数量
  		List<String> column = new ArrayList<>();
  		column.add("like1");
  		// 设置每列的列类型
  		List<ObjectInspector> columnsType = new ArrayList<>();
  		columnsType.add(PrimitiveObjectInspectorFactory.javaStringObjectInspector);
  		return ObjectInspectorFactory.getStandardStructObjectInspector(column,columnsType);
  	}
  ```

- **process来处理将一列拆成多列或者多行，形成临时表格**

  ```java
  	@Override
  	public void process(Object[] objects) throws HiveException {
  		// 将一列拆成两列  摔回去objects第一个数值是列值，object其他参数是该列的其他参数
  		String [] res = objects[0].toString().split(",");
  		for (String re : res) {
  			forward(new Object[]{re});
  		}
  	}
  ```

> ps:以后我们可以让一列的奇葩数据在java底层割成多个数组,慢慢匹配
>
> 例：zs.23;play,sleep friend

- **close关闭**

```java
	@Override
	public void close() throws HiveException {}
```



>  **explode是特殊的UDTF函数**，一列拆多行

使用UDTF甚至可以做到`一列拆多列  |  一列拆多行  |  一列拆多列多行`

---

### UDF | UDAF | UDTF 区别：

> UDF:返回对应值，**一对一**

> UDAF：返回聚类值，**多对一**

> UDTF：返回拆分值，**一对多**

### Hive宏函数：

> 由于UDF是Java编写的，代码中堆变量的**内存回收完全不受开发者控制**，而UDF程序又是嵌套在Hive SQL中执行的，对规模较大的表，就往往会出现由于**UDF内存回收不及时**造成的out-of-memory错误。因此，在生产环境中，**UDF是严格受限的**

`大多数不需要循环结构的逻辑，基本上都可以用宏来处理`

#### 创建宏函数：

```sql
create temporary macro macro_name([col_name col_type, ...])
expression;
```

#### 宏的局限性：

- **宏只能是临时宏，只在本次会话中可见、有效**

### UDF函数--宏函数--存储过程：

- 宏作为暂时函数
- 存储过程只为做存储过程

### Hive的事务处理：

### Hive的PLSQL：

### Hive的性能调优: