## DataBase连接封装：

## UML图：

![image-20200625223532211](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200625223532211.png)



## 抽象工厂模式：

抽象数据工厂：

`AbstractDatabaseFactory：`

```java
package org.wyw.commons;

/**
 * @ClassName:AbstractDatabaseFactory
 * @Author WYW
 * @Date23/06/202016:28
 * @Description: TODO 这是一个抽象工厂
 * @Version V1.0
 **/
public abstract class AbstractDatabaseFactory<T> {
	public abstract DatabaseReaderAndWriter<T> buildReaderAndWriter();
}
```

---





建造者模式：

---

`BuilderFactory:`

```java
package org.wyw.commons;

/**
 * @ClassName:BuildeFactory
 * @Author WYW
 * @Date23/06/202016:43
 * @Description: TODO 工厂建造者模式
 * @Version V1.0
 **/
public class BuilderFactory {
	private BuilderFactory(){}
	public static final int HBASE = 0;
	public static final int MYSQL = 1;

	public static AbstractDatabaseFactory builder(Configuration cfg,int databaseType){
		switch (databaseType) {
			case 0:
				return new HbaseDatabaseFactory(cfg);
			case 1:
				return new MySqlDatabaseFactory(cfg);
			default:
				return null;
		}
	}
}
```

---

`DatabaseReaderAndWriter:`

```java
package org.wyw.commons;

import java.io.IOException;
import java.util.List;

/**
* @author WYW
* @date 23/06/2020 16:30
* @param
* @return
* @description 抽象产品接口 主要是对数据库的读写接口
*/
public interface DatabaseReaderAndWriter<T> {
    
	/**
	* @author WYW
	* @date 23/06/2020 16:32
	* @param [t]
	* @return void
	* @description 单项插入
	*/
	public void writer(T t) throws Exception;
    
	/**
	* @author WYW
	* @date 23/06/2020 16:32
	* @param [list]
	* @return void
	* @description 批量插入
	*/
	public void writer(List<T> list);

	/**
	* @author WYW
	* @date 23/06/2020 16:39
	* @param [conn, sql]
	* @return java.util.List<T>
	* @description 读取用户传入的命令或sql语句 完成解析后执行对应的结果 转为list集合
	*/
	public List<T> reader(String sql,Class cls) throws IOException, InstantiationException, IllegalAccessException;

```

---

`BuilderFactory:`

```java
package org.wyw.commons;

/**
 * @ClassName:BuildeFactory
 * @Author WYW
 * @Date23/06/202016:43
 * @Description: TODO 工厂建造者模式
 * @Version V1.0
 **/
public class BuilderFactory {
	private BuilderFactory(){}
	public static final int HBASE = 0;
	public static final int MYSQL = 1;

	public static AbstractDatabaseFactory builder(Configuration cfg,int databaseType){
		switch (databaseType) {
			case 0:
				return new HbaseDatabaseFactory(cfg);
			case 1:
				return new MySqlDatabaseFactory(cfg);
			default:
				return null;
		}
	}
}
```

---

`HbaseDatabaseFactory:`

```java
package org.wyw.commons;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.ConnectionFactory;
import java.io.IOException;

/**
 * @ClassName:HbaseDatabaseFactory
 * @Author WYW
 * @Date23/06/202016:48
 * @Description: TODO hbase 数据库的具体工厂
 * @Version V1.0
 **/
public class HbaseDatabaseFactory<T> extends AbstractDatabaseFactory<T> {
	Configuration config;

	public HbaseDatabaseFactory(Configuration config) {
		this.config = config;
	}

	/**
	* @author WYW
	* @date 23/06/2020 17:22
	* @param
	* @return java.lang.Object
	* @description 创建链接
	**/
	private Connection createConnection() {
		org.apache.hadoop.conf.Configuration conf = HBaseConfiguration.create();
		// 设置HBase专属的配置信息
		//		conf.set("hbase.zookeeper.quorm","niceday");
		//		conf.set("hbase.zookeeper.property.clientPort","2181");
		//		conf.set("hbase.master","192.168.56.110:16010");// 默认60000端口
		conf.set("hbase.zookeeper.quorm",config.get("hbase.zookeeper.quorm"));
		conf.set("hbase.zookeeper.property.clientPort",config.get("hbase.zookeeper.property.clientPort") == null ? "2181" :config.get("hbase.zookeeper.property.clientPort"));
		conf.set("hbase.master",config.get("hbase.master") == null ? config.get("hbase.zookeeper.quorm") + ":60000" : config.get("hbase.master"));

		// 通过配置信息来产生对应的Hbase连接
		Connection connection = null ;
		try {
			 connection = ConnectionFactory.createConnection(conf);
		} catch (IOException e) {
			e.printStackTrace();
		}
		return  connection;

	}

	@Override
	public DatabaseReaderAndWriter<T> buildReaderAndWriter() {
		return new HbaseRWHandler<T>(createConnection());
	}
}
```

---

`HbaseRWHandler:`

```java
package org.wyw.commons;
import com.wyw.Userinfos;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.filter.*;
import org.apache.hadoop.hbase.util.Bytes;
import java.io.IOException;
import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


/**
 * @ClassName:HbaseRWHandler
 * @Author WYW
 * @Date23/06/202017:02
 * @Description: TODO 具体产品Hbase数据库读写操作的具体产品
 * @Version V1.0
 **/
public class HbaseRWHandler<T> implements DatabaseReaderAndWriter<T> {
	private Connection con;
	public HbaseRWHandler(Connection con){

	}
	@Override
	public void writer(T t) throws Exception {
		Class<?> objClazz = t.getClass();
		String tabName = objClazz.getSimpleName();
		TableName tableName = TableName.valueOf(tabName);
		Field[] df = objClazz.getDeclaredFields();
		Table table = con.getTable(tableName);

		Field rowkey = objClazz.getDeclaredField("rowkey");
		if (rowkey == null){
			throw new Exception("no exit rowkey");
		}
		rowkey.setAccessible(true);
		Object o = rowkey.get(t);
		if (o == null) {
			throw new Exception("no exist value");
		}
		Put put = new Put(o.toString().getBytes());
		// 其他值按列簇和修饰符填充2
		for (Field field : df) {
			field.setAccessible(true);
			Object val = field.get(t);
			String valName = field.getName();
			// 用户可能输入为空
			if (val != null) {
				if (!valName.equalsIgnoreCase("rowkey")) {
					// 获取列簇和修饰符
					String columnFamily = valName.split("_")[0];
					String column = valName.split("_")[1];
					put.addColumn(columnFamily.getBytes(), column.getBytes(),val.toString().getBytes());
				}
			}
		}
		table.put(put);
	}

	@Override
	public void writer(List<T> list) {

	}

	// scan 'mydemo:userinfos',Filter => 'ValueFilter(=,'binary:zhangsan')'
	@Override
	public List<T> reader(String sql,Class cls) throws IOException, InstantiationException, IllegalAccessException {
		List<String> rules = regexp_split(sql);
		TableName tn = TableName.valueOf(rules.get(0));
		Table table = con.getTable(tn);
		Scan scan = new Scan();
		if (rules.size() > 1){
			if (rules.get(1).equalsIgnoreCase("ValueFilter")){
				ValueFilter vf = new ValueFilter(change(rules.get(2)),
					rules.get(4).equalsIgnoreCase("binary")? new BinaryComparator(rules.get(4).getBytes()) : new SubstringComparator(rules.get(4)));
				scan.setFilter(vf);

			}else {
				ColumnPrefixFilter cpf = new ColumnPrefixFilter(rules.get(2).getBytes());
				scan.setFilter(cpf);
			}
		}
		ResultScanner scanner = table.getScanner(scan);
		return change(scanner, Userinfos.class);
        
	}

	/**
	* @author WYW
	* @date 24/06/2020 16:21
	* @param
	* @return java.util.List<java.lang.String>
	* @description 符合转换为枚举对象
	*/
	public CompareFilter.CompareOp change(String sql){
		switch (sql){
			case "=":
				return CompareFilter.CompareOp.EQUAL;
			case ">":
				return CompareFilter.CompareOp.GREATER;
			case ">=":
				return CompareFilter.CompareOp.GREATER_OR_EQUAL;
			case "<":
				return CompareFilter.CompareOp.LESS;
			case "<=":
				return CompareFilter.CompareOp.LESS_OR_EQUAL;
			case "!=":
				return CompareFilter.CompareOp.NOT_EQUAL;
			default:
				return null;
		}
	}

	/**
	* @author WYW
	* @date 24/06/2020 16:42
	* @param [results, cla]
	* @return java.util.List<T>
	* @description 将hbase的resultscanner集合利用反射转换为list<T>集合
	*/
	private  <T> List<T> change(ResultScanner results, Class cla) throws IllegalAccessException, InstantiationException {
		//获取类中所有的属性信息
		Field[] fields = cla.getDeclaredFields();
		//根据hbase集合生成n个cla类型的对象
		List<T> list = new ArrayList<>();
		for (Result result : results) {
			//建造一个cla的空对象
			Object o = cla.newInstance();
			//将result中的数据填充到o 对应的属性中
			for (Field field : fields) {
				if (!field.getName().equalsIgnoreCase("rowkey")){
					field.setAccessible(true);
					byte[] cloumn = Bytes.toBytes(field.getName().split("_")[0]);
//					System.out.println(field.getName().split("_")[0]);
					byte[] s = Bytes.toBytes(field.getName().split("_")[1]);
					byte[] value = result.getValue(cloumn, s);
					if (value!=null){
						field.set(o,new String(value));
					}
				}else {
					field.set(o,new String(result.getRow()));
				}
			}
			list.add((T) o);
		}
		return list;
	}

	private List<String> regexp_split(String sql){

		// 分割字符串将对应的元素取出
		// 用正则进行匹配 Pattern类和 Matcher类
		boolean isHas = Pattern.matches(".*FILTER.*", sql.toUpperCase());

		String regex = ".*'([a-zA-Z:]+)'(,.*'(\\w+)\\((.*),([a-z]+):([\\w0-9]+).*)?";
		Pattern p = Pattern.compile(regex);
		Matcher matcher = p.matcher(sql);
		List<String> rule = new ArrayList<>();
		if (matcher.find()){
			rule.add(matcher.group(1));
			if (isHas){
				rule.add(matcher.group(3));
				rule.add(matcher.group(4));
				if (matcher.group(6) != null){
					rule.add(matcher.group(6));
					rule.add(matcher.group(7));
				}
			}
		}
		return rule;
	}
}

```

---

`MySqlDatabaseFactory:`

```java
package org.wyw.commons;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
 * @ClassName:MySqlDatabaseFactory
 * @Author WYW
 * @Date23/06/202016:47
 * @Description: TODO 连接mysql数据库具体工厂
 * @Version V1.0
 **/
public class MySqlDatabaseFactory<T> extends AbstractDatabaseFactory<T> {
	Configuration config;
	public 	MySqlDatabaseFactory(Configuration config){
		this.config = config;
	}

	private Connection createConnection() {
		Connection connection = null;
		// 
		try {
			Class.forName(config.get("driver"));
			 connection = DriverManager.getConnection(config.get("url"), config.get("username"), config.get("password"));
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return connection;
	}
    
	@Override
	public DatabaseReaderAndWriter<T> buildReaderAndWriter() {
		return new MysqlRWHandler<>(createConnection());
	}
}

```

---

`MysqlRWHandler:`

```java
package org.wyw.commons;
import java.sql.Connection;
import java.util.List;


/**
 * @ClassName:MysqlRWHandler
 * @Author WYW
 * @Date23/06/202016:58
 * @Description: TODO mysqlRWHandler是mysql具体实现
 * @Version V1.0
 **/
public class MysqlRWHandler<T> implements DatabaseReaderAndWriter<T> {
	private Connection conn;
	public MysqlRWHandler(Connection conn){
		this.conn = conn;
	}
	@Override
	public void writer(T t) {}

	@Override
	public void writer(List<T> list) {}

	@Override
	public List<T> reader(String sql,Class cls) {
		return null;
	}
}

```

`Configuratuion:`

```java
package org.wyw.commons;
import java.util.HashMap;
import java.util.Map;

/**
 * @ClassName:Configuration
 * @Author WYW
 * @Date23/06/202016:52
 * @Description: TODO
 * @Version V1.0
 **/
public class Configuration {
	private Map<String,String> properties = new HashMap<>();

	public void setDriver(String key, String prop){
		properties.put(key,prop);
	}
	public void setClientPort(String key, String prop){
		properties.put(key,prop);
	}

	public void setMasterIP(String key, String prop){
		properties.put(key,prop);
	}

	public static Configuration create(){
		return new Configuration();
	}

	public String get(String key){
		return properties.get(key);
	}
}

```

## 实体类：

```java
package com.wyw;

/**
 * @ClassName:Userinfos
 * @Author WYW
 * @Date23/06/202011:53
 * @Description: TODO
 * @Version V1.0
 **/
public class Userinfos {
   private String rowkey;
   private String base_stuno;
   private String base_username;
   private String base_age;
   private String externals_likes;

   public String getRowkey() {
      return rowkey;
   }

   public void setRowkey(String rowkey) {
      this.rowkey = rowkey;
   }

   public String getBase_stuno() {
      return base_stuno;
   }

   public void setBase_stuno(String base_stuno) {
      this.base_stuno = base_stuno;
   }

   public String getBase_username() {
      return base_username;
   }

   public void setBase_username(String base_username) {
      this.base_username = base_username;
   }

   public String getBase_age() {
      return base_age;
   }

   public void setBase_age(String base_age) {
      this.base_age = base_age;
   }

   public String getExternals_likes() {
      return externals_likes;
   }

   public void setExternals_likes(String externals_likes) {
      this.externals_likes = externals_likes;
   }
}
```

## 建造者模式：