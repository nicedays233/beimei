- #### 将HBase作为Hive数据源

  - 让hbase实现类sql语句

- #### 将Hive ETL数据存入HBase

- #### 构建低延时得数据仓库

  - 利用HBase快速读写能力
  - 实现数据实时查询

### hive与hbase集成原理：

## Shell导入到HBase：

```shell
##通过hbase shell导入文档数据
hbase org.apache.hadoop.hbase.mapreduce.ImportTsv \
-Dimporttsv.separator=','  \
-Dimporttsv.columns="HBASE_ROW_KEY,order:numb,order:date" \
customer file:///home/vagrant/hbase_import_data.csv
```



## Hive与HBase集成：

```sql
create external table myhbtab(
    kw string, 
    stuno string, 
    username string,
    age string, 
    likes string) 
    stored by 'org.apache.hadoop.hive.hbase.HBaseStorageHandler' 
    with serdeproperties("hbase.columns.mapping"=":key,base:stuno,base:username,base:age,externals:likes") 
    tblproperties("hbase.table.name"="mydemo:userinfos");
    
    // key为rowkey 剩下来表字段，和列族列名一一对应
```



## Sqoop将Mysql移到HBase：

```shell
 sqoop import 
    --connect jdbc:mysql://localhost:3306/retail_db 
    --username root 
    --password hadoop 
    --table products 
    --columns "customernum, customername" 
    --hbase-table customercontactinfo 
    --column-family CustomerName 
    --hbase-row-key customernum
    -m 1
```



## JavaAPI控制HBase：

```java
package com.wyw;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.*;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.util.Bytes;

import javax.ws.rs.GET;
import java.io.IOException;

/**
 * @ClassName:HBaseClient
 * @Author WYW
 * @Date20/07/202011:38
 * @Description: TODO
 * @Version V1.0
 **/
public class HBaseClient {
	// 创建表操作

	public void createTable() throws Exception{
		// 1.创建配置
		Configuration conf = HBaseConfiguration.create();
		// 配置zk集群和端口
		conf.set("hbase.zookeeper.quorum","niceday");
		conf.set("hbase.zookeeper.property.clientPort","2181");
		// 2.创建连接
		Connection conn = ConnectionFactory.createConnection(conf);

		// 创建admin
		Admin admin = conn.getAdmin();

		// 3.创建表描述信息
		HTableDescriptor student = new HTableDescriptor(TableName.valueOf("student"));

		// 4.添加列簇
		student.addFamily(new HColumnDescriptor("info"));
		student.addFamily(new HColumnDescriptor("score"));

		// 5.调用api进行建表操作
		admin.createTable(student);

	}

	// 判断表是否存在
	public void isTableExists() throws IOException {
		// 1.创建配置，配置zk集群和端口
		Configuration conf = HBaseConfiguration.create();
		// 配置zk集群和端口
		conf.set("hbase.zookeeper.quorum","niceday");
		conf.set("hbase.zookeeper.property.clientPort","2181");
		// 2.创建连接
		Connection conn = ConnectionFactory.createConnection(conf);

		// 创建admin
		Admin admin = conn.getAdmin();
		System.out.println(admin.tableExists(TableName.valueOf("student")));
	}


	// 像表插入数据

	public void putDataTable() throws IOException {
		Configuration conf = HBaseConfiguration.create();
		// 配置zk集群和端口
		conf.set("hbase.zookeeper.quorum","niceday");
		conf.set("hbase.zookeeper.property.clientPort","2181");
		// 2.创建连接
		Connection conn = ConnectionFactory.createConnection(conf);

		// 3.创建table类
		Table student = conn.getTable(TableName.valueOf("student"));

		// 4.创建put类,放入rowkey
		Put put = new Put(Bytes.toBytes("1001"));
		// 5.向put中添加列簇，列名，值，注意转换成字节数组
		put.addColumn(Bytes.toBytes("info"),Bytes.toBytes("name"),Bytes.toBytes("zahngsan"));
		// 6. 调用api进行插入数据
		student.put(put);

	}


	// 查看一条数据
	public void getDataFromTable() throws Exception {
		Configuration conf = HBaseConfiguration.create();
		// 配置zk集群和端口
		conf.set("hbase.zookeeper.quorum","niceday");
		conf.set("hbase.zookeeper.property.clientPort","2181");
		// 2.创建连接
		Connection conn = ConnectionFactory.createConnection(conf);

		// 3.创建table类
		Table student = conn.getTable(TableName.valueOf("student"));
		// 4. 创建get类
		Get get = new Get(Bytes.toBytes("1001"));
		// 5.调用api进行获取数据
		Result result = student.get(get);

		// 6.将返回的结果进行遍历输出
		Cell[] cells = result.rawCells();
		for (Cell cell : cells) {
			System.out.println("rowkey ：" + Bytes.toString(CellUtil.cloneRow(cell)));
			System.out.println("列簇 ：" + Bytes.toString(CellUtil.cloneFamily(cell)));
			System.out.println("列名 ：" + Bytes.toString(CellUtil.cloneQualifier(cell)));
			System.out.println("值 ：" +Bytes.toString(CellUtil.cloneValue(cell)));
		}

	}


	// 删除表操作
	public void dropTable() throws Exception {
		// 1.创建配置，配置zk集群和端口
		Configuration conf = HBaseConfiguration.create();
		// 配置zk集群和端口
		conf.set("hbase.zookeeper.quorum","niceday");
		conf.set("hbase.zookeeper.property.clientPort","2181");
		// 2.创建连接
		Connection conn = ConnectionFactory.createConnection(conf);

		// 3.创建admin
		Admin admin = conn.getAdmin();

		// 4.调用Api禁用表
		admin.disableTable(TableName.valueOf("student"));
		// 5.删除表
		admin.deleteTable(TableName.valueOf("student"));
	}



	public static void main(String[] args) throws Exception {
//		new HBaseClient().createTable();
//		new HBaseClient().isTableExists();
//		new HBaseClient().putDataTable();
		new HBaseClient().getDataFromTable();
	}
}

```



