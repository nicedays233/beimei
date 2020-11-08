## 文件存储方式：

### Text文件格式

- 文本文件通常采用csv，JSON等固定长度的纯文本格式
- **优点**
  - 便于与其他应用程序或脚本进行数据交换
  - 易读性好，便于理解
- **缺点**
  - 数据存储量非常庞大
  - 查询效率不高
  - 不支持块压缩

![image-20200723083913968](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200723083913968.png)

### SequenceFile--不适合Hive

- **SequenceFile按行存储二进制键值对数据，HDFS自带**

  - 二进制文件直接将<K,V>序列化到文件
  - 常用于在MapReduce作业之间传输数据
  - 可用作Hadoop小文件的打包存档（小文件合并）
  - 即使在压缩数据时也支持分割

- 键值对类型

  - SequenceFile中的Key和Value可以是任意类型的Writable

- **JAVA  API**

  - org.apache.hadoop.io.SequenceFile

  #### s

![image-20200723084549483](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200723084549483.png)

#### 压缩：

- 记录级（RECORD）

  - 仅压缩Value

  ```js
  io.seqfile.compression.type=RECORD
  ```

  

- 块级（BLOCK）：

  - 一次压缩多条记录，利用记录间的相似性进行压缩，效率更高

  ```js
  io.seqfile.compression.type=BLOCK
  ```

#### 

#### Hive中使用序列化格式

![image-20200723090900339](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200723090900339.png)

```java
// 方式一
STORED AS sequenceFile

// 方式二 显示指定 可以指定输入一个格式，输出一个格式
STORED AS INPUTFORMAT 'org.apache.hadoop.mapred.SequevceFileInputFormat'
STORED AS OUTPUTFORMAT 'org.apache.hadoop.mapred.SequevceFileOutputFormat'
    
```

#### JAVA控制SequenceFile

```java
package com.wyw.dataModel;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.util.ReflectionUtils;

import java.io.IOException;
import java.net.URI;

/**
 * @Author Leo
 * @Date 2019/5/6 9:49
 **/
public class SequenceFileOps {
    private static Configuration conf=new Configuration();

    private static String url="hdfs://niceday:9000";

    private static String[] data={"a,b,c,d,e,f,g","e,f,g,h,j,k","l,m,n,o,p,q,r,s","t,u,v,w,x,y,z"};

    public static void main(String[] args) throws IOException {
        write();
        read();
    }

    public static void write() throws IOException {
        // io.seqfile.compression.type=RECORD  记录压缩
        // io.seqfile.compression.type=BLOCK  块压缩
        conf.set("io.seqfile.compression.type","BLOCK");
        // 获取文件系统
        FileSystem fs= FileSystem.get(URI.create(url),conf);
        // 定义输出路径
        Path output=new Path("/tmp/myseqfile.seq");
        // 定义key和value
        IntWritable key=new IntWritable();
        Text value=new Text();
        // 创建写入流
        SequenceFile.Writer writer=SequenceFile.createWriter(fs,conf,output,IntWritable.class, Text.class);
        // 循环将数据写入
        for (int i=0;i<10;i++){
            key.set(i);
            // 不断将data的0-4放入writer中， 随便写点文件写入
            value.set(data[i%data.length]);
            writer.append(key,value);
        }
        // 关闭资源
        IOUtils.closeStream(writer);
    }
    private static void read() throws IOException {
        // 获取文件系统
        FileSystem fs= FileSystem.get(URI.create(url),conf);
        // 定义读取路径
        Path input=new Path("/tmp/myseqfile.seq");
        // 定义一个读入流
        SequenceFile.Reader reader=new SequenceFile.Reader(fs,input,conf);
        // 定义一个读入的key和value
        Writable key= (Writable) ReflectionUtils.newInstance(reader.getKeyClass(),conf);
        Writable value= (Writable) ReflectionUtils.newInstance(reader.getValueClass(),conf);

        while(reader.next(key,value)){
            System.out.println("key:"+key);
            System.out.println("value:"+value);
            System.out.println("position:"+reader.getPosition());// 偏移量

        }
    }
}

```



### Avro格式：适合读

- Avro File
  - **以JSON格式数据定义**
  - 以**二进制格式存储**数据
- 特点
  - 丰富的数据结构
  - 快速可压缩的二进制数据格式
  - 容器文件用于持久化数据
  - 自带远程过程调用RPC
  - 动态语言可以方便处理Avro数据



#### Avro数据类型

- 基本
  - null,boolean,int,long,float,double,bytes,string
- 复杂
  - record
  - enum
  - array
  - map
  - union
  - fixed

```json
{
    "namespace":"example.avro",
    "type":"record",
    "name":"User",
    "fields":[
        {"name":"name","type":"string"},
        {"name":"f_number","type":"int"}
    ]
}
```

![image-20200723095321577](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200723095321577.png)



#### avro-tools应用

- 使用schema+data生成avro文件

```js
java -jar avro-tools-1.8.2.jar fromjson --schema-file user.avsc user.json > user.avro
java -jar avro-tools-1.8.2.jar fromjson --codec snappy --schema-file user.avsc user.json > user.avro

```

- avro转json

```js
java -jar avro-tools-1.8.2.jar tojson user.avro
java -jar avro-tools-1.8.2.jar tojson user.avro --pretty
```

- 获取avro元数据

```js
java -jar avro-tools-1.8.2.jar getmeta user.avro
```

#### Avro文件存储结构：

![image-20200723101317333](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200723101317333.png)

### Parquet列式存储格式：-SparkSQL默认数据源

#### 行列存储差异：

![image-20200723103248969](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200723103248969.png)

- 列式存储的优点
  - 按需读取列
  - 压缩编码可以降低磁盘存储空间

#### Parquet文件结构-先行组再列块



> **按照行将数据物理上划分为多个组**，每一个行组包含一定的行数，通常行组大小等于HDFS块大小

![image-20200723104215503](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200723104215503.png)

- 行组row group

- 列块column chunk

  ![image-20200723104437880](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200723104437880.png)

- 页page

#### Java读写Parquet文件

```java
package com.wyw.dataModel;

import org.apache.hadoop.fs.Path;
import org.apache.parquet.example.data.Group;
import org.apache.parquet.example.data.simple.SimpleGroup;
import org.apache.parquet.example.data.simple.SimpleGroupFactory;
import org.apache.parquet.hadoop.ParquetFileWriter;
import org.apache.parquet.hadoop.ParquetReader;
import org.apache.parquet.hadoop.ParquetWriter;
import org.apache.parquet.hadoop.example.ExampleParquetWriter;
import org.apache.parquet.hadoop.example.GroupReadSupport;
import org.apache.parquet.schema.MessageType;
import org.apache.parquet.schema.MessageTypeParser;


import java.io.IOException;

/**
 * @Author Leo
 * @Date 2019/5/7 11:49
 **/
public class ParquetOps {

    public static void main(String[] args) {
        try {
//            write();
            read();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void write() throws IOException {
        // 定义输出路径
        Path file = new Path("/tmp/user-parquet/1.parquet");
        // 定义schema信息
        String schemaStr="message User{\n" +
                "    required binary name (UTF8);\n" +
                "    required int32 age;\n" +
                "    repeated group family{\n" +
                "        repeated binary father (UTF8);\n" +
                "        repeated binary mother (UTF8);\n" +
                "        optional binary sister (UTF8);\n" +
                "    }\n" +
                "}\n";
        // 解析schema信息，将我们定义的schema信息解析成系统能看懂的schema信息
        MessageType schema=MessageTypeParser.parseMessageType(schemaStr);
        // 创建一个写入流
        ParquetWriter<Group> writer= ExampleParquetWriter.builder(file)
                .withWriteMode(ParquetFileWriter.Mode.OVERWRITE)
                .withType(schema).build();
        // 创建一个组
        SimpleGroupFactory groupFactory = new SimpleGroupFactory(schema);
        Group group1=groupFactory.newGroup();
        // 向组中添加列和值
        group1.add("name","jason");
        group1.add("age",9);
        // 嵌套组，列簇
        Group cGroup1=group1.addGroup("family");
        cGroup1.add("father","XXX");
        cGroup1.add("mother","XXX");

        Group group2=groupFactory.newGroup();
        group2.add("name","tom");
        group2.add("age",18);
        //添加子组
        group2.addGroup("family")
                .append("father","ZZZ")
                .append("mother","ZZZ");//append与add返回值不同
        writer.write(group1);
        writer.write(group2);
        writer.close();

    }
    private static void read() throws IOException {
        // 创建一个读入路径
        Path file = new Path(
                "hdfs://192.168.56.101:9000/tmp/parquet");
        // 创建一个读取流
        ParquetReader.Builder<Group> builder = ParquetReader.builder(new GroupReadSupport(), file);
        ParquetReader<Group> reader = builder.build();
        // 读入数据
        SimpleGroup group =(SimpleGroup) reader.read();
        System.out.println("schema:" + group.getType().toString());
        while(group!=null) {
            // fieldindex=0 第一列 ，index 第一列的第一个元素，确定了一个单元格
            System.out.println("username:" + group.getString(0, 0));
            System.out.println("age:" + group.getInteger(1, 0));
//            System.out.println("family.father:" + group.getGroup(2, 0).getString(0, 0));
            System.out.println(group.toString());
            group =(SimpleGroup) reader.read();
        }
    }
}

```

### RC&ORC：--Hive主流

#### RC存储结构：

- 集行存储与列存储优点于一身
- 设计思想与Parquet类似，先按行水平切割为多个行组，再对每个行组内的数据按列存储】

![image-20200723113931866](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200723113931866.png)



#### ORCFile存储结构：

- Stripe
  - 每个ORC文件首先会被横向切分成多个Stripe
  - 每个stripe默认的大小是250MB
  - 每个stripe由多组（Row Groups）行数据组成

- IndexData
  - 保存了该stripe上数据的位置，总行数

- RowData
  - 以stream的形式保存数据

- Stripe Footer
  - 包含该stripe统计结果：Max，Min，count等信息

- FileFooter
  - 该表的统计结果
  - 各个Stripe的位置信息

- Postscript
  - 该表的行数，压缩参数，压缩大小，列等信息

![image-20200723113919549](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200723113919549.png)

#### JAVA读写ORC文件

```java
package com.wyw.dataModel;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.hive.ql.io.orc.OrcSerde;
import org.apache.hadoop.hive.serde2.objectinspector.ObjectInspectorFactory;
import org.apache.hadoop.hive.serde2.objectinspector.StructObjectInspector;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.OutputFormat;
import org.apache.hadoop.mapred.RecordWriter;
import org.apache.hadoop.mapred.Reporter;
import org.apache.orc.mapred.OrcOutputFormat;

/**
 * @author kgc
 */
public class ORCFileOps {

    public static void main(String[] args) throws Exception {
        JobConf conf = new JobConf();
        FileSystem fs = FileSystem.get(conf);
        Path outputPath = new Path("/tmp/orcoutput/user.orc");
        // 定义schema信息
        StructObjectInspector inspector =
                (StructObjectInspector) ObjectInspectorFactory
                        .getReflectionObjectInspector(MyRow.class,
                                ObjectInspectorFactory.ObjectInspectorOptions.JAVA);
        OrcSerde serde = new OrcSerde();
        OutputFormat<NullWritable, Writable> outFormat = new OrcOutputFormat<>();
        // 创建写出流
        RecordWriter<NullWritable, Writable> writer = outFormat.getRecordWriter(fs, conf,
                outputPath.toString(), Reporter.NULL);
        // 写入数据
        writer.write(NullWritable.get(),
                serde.serialize(new MyRow("张三", 20), inspector));
        writer.write(NullWritable.get(),
                serde.serialize(new MyRow("李四", 22), inspector));
        writer.write(NullWritable.get(),
                serde.serialize(new MyRow("王五", 30), inspector));
        writer.close(Reporter.NULL);
        fs.close();
        System.out.println("write success .");
    }

    static class MyRow implements Writable {
        String name;
        int age;

        MyRow(String name, int age) {
            this.name = name;
            this.age = age;
        }

        @Override
        public void readFields(DataInput arg0) throws IOException {
            throw new UnsupportedOperationException("no write");
        }

        @Override
        public void write(DataOutput arg0) throws IOException {
            throw new UnsupportedOperationException("no read");
        }
    }
//    CREATE EXTERNAL TABLE user_orc(
//            name STRING,
//            age INT
//    ) stored AS ORC
//    location '/tmp/orcoutput';
}

```

### 文件存储比较：

| **File Type** | **Splittable** | **Block Compressible** | **Schema Evolution******* | **Hive** | **Spark** | **Remark**       |
| ------------- | -------------- | ---------------------- | ------------------------- | -------- | --------- | ---------------- |
| Text/CSV      | Yes            | No                     | No                        | Yes      | Yes       |                  |
| XML/JSON      | No             | No                     | Yes                       | ?        | Yes       |                  |
| AvroFile      | Yes            | Yes                    | Yes                       | Yes      | Yes       |                  |
| SequenceFile  | Yes            | Yes                    | Yes                       | Yes      | Yes       |                  |
| RCFile        | Yes            | Yes                    | No                        | Yes      | Yes       | Columnar Storage |
| ORCFile       | Yes            | Yes                    | No                        | Yes      | Yes       | Columnar Storage |
| ParquetFile   | Yes            | Yes                    | Yes                       | Yes      | Yes       | Columnar Storage |

### 存储格式的选择

- **写：一般写入时间并不是最重要**

- **读**
  - Avro——查询随时间变化的数据集
  - Parquet ——适合在宽表上查询少数列
  - Parquet & ORC以牺牲写性能为代价优化读取性能
  - TextFile读起来很慢

- **Hive** **查询（快->慢**）
  - ORC -> Parquet -> Text -> Avro -> SequenceFile