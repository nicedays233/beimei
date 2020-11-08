## Sqoop数据迁移：

### 什么是sqoop？

>  sqoop是用在Hadoop和关系数据库之间传输数据的工具

- 将数据从RDBMS导入到HDFS
- HDFS导出数据RDBMS
- 使用MapReduce导入和导出数据，提供并行操作和容错

### 从RDBMS导入数据到HDFS-1

- 导入表到HDFS

  ```shell
  sqoop import
  	connect jdbc:mysql://localhost:3306/hr
  	driver com.mysql.jdbc.
  ```



### Sqoop安装：

**第一步：**sqoop解压

将sqoop压缩包放到/opt目录文件下

```shell
 tar -zxf sqoop-1.4.6-cdh5.14.2.tar.gz
 mv sqoop-1.4.6-cdh5.14.2 /opt/soft/sqoop146
```

**第二步：**复制hadoop的jar包和连接mysql驱动包到sqoop的lib文件夹下

```shell

cp /opt/soft/hadoop260/share/hadoop/common/hadoop-common-2.6.0-cdh5.14.2.jar /opt/soft/sqoop146/lib/

cp /opt/soft/hadoop260/share/hadoop/hdfs/hadoop-hdfs-2.6.0-cdh5.14.2.jar /opt/soft/sqoop146/lib/

cp /opt/soft/hadoop260/share/hadoop/mapreduce/hadoop-mapreduce-client-core-2.6.0-cdh5.14.2.jar /opt/soft/sqoop146/lib
```

![image-20200722111118128](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200722111118128.png)

![image-20200722111554755](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200722111554755.png)

**第三步：**配置sqoop-env.sh文件

```shell
vi /opt/soft/sqoop146/conf/sqoop-env.sh
```

```shell
export HADOOP_COMMON_HOME=/opt/soft/hadoop260

export HAOOP_MAPRED_HOME=/opt/soft/hadoop260

export HABSE_HOME=/opt/soft/hbase120

export HIVE_HOME=/opt/soft/hive110

export ZOOCFGDIR=/opt/soft/zk345/conf
```

![image-20200626100920830](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200626100920830.png)

**第四步：**配置全局变量

```shell
vi /etc/profile
```

```shell
export SQOOP_HOME=/opt/soft/sqoop146
export PATH=$PATH:$SQOOP_HOME/bin
```

```shell
source /etc/profile
```

完成`Sqoop安装

### Sqoop命令：

`sqoop list命令`--显示数据库名

```shell
sqoop list-databases --username root --password root --connect jdbc:mysql://192.168.43.24:3306/
 
sqoop list-tables --username root --password root --connect jdbc:mysql://192.168.43.24:3306/
```

`sqoop import命令`--将关系型数据导入到HDFS上

- 将整表导入hdfs上

```shell
# 加\是为了多行输入
sqoop import \ 
--connect jdbc:mysql://192.168.56.101:3306/mydemo \
--username root --password 123456 \
--incremental append \ # 增量导入方式append追加数据至已经存在的HDFS数据集上
--check columns
--delete-target-dir \ # 存在文件夹就删除
--table userinfos \
--target-dir /tmp/viewscore6 \  # 导入到hdfs的文件位置
--fields-terminated-by '/' \  # 在hdfs上以对应的空格符
-m 3
```

- 将查询好的数据导入到hdfs上

```shell
sqoop import \
--connect jdbc:mysql://192.168.56.101:3306/mydemo \
--username root --password 123456 \
--query "select * from xxx where xxx and \$CONDITITONS" \
--target-dir /tmp/viewscore4 \
--fields-terminated-by ',' \
--split by usrid \ # 堆某一列进行设定逻辑分片的规则，通过hash值划分逻辑片
-m 3 # 设置mapper的数量,也就是文件分片的数量
--as sequencefile # 将其转化为序列化文件
```



```shell
connect jdbc:oracle:thin:@192.168.56.101:1521:ORCL # oracle 的迁移驱动包名为oracle.jdbc.OracleDriver
```



### 增量将数据迁移到HBase上，并在Hive上做分析:

`写出mysql数据导入HBase的脚本：`

```shell
! /bin/bash
#获取当前日期
nowdate=$(date --date='1 day ago' "+%Y-%m-%d")
echo $nowdate
# 如果存在mydata，就删除没有8位数字的文件夹
hdfs dfs -test -e /mydata1
if [ $? -eq 0 ];then
        files=`hdfs dfs -ls /mydata1 | awk '{print $8}'| cut -d '/' -f3 | grep -v "[0-9]\{4\}"`
        for fl in $files
        do
                hdfs dfs -rmr /mydata1/$fl
        done
else
        hdfs dfs -mkdir -p /mydata1/
fi




#sqoop执行路径
#连接配置
# 将mysql数据导入hdfs
foldername=`echo $nowdate | sed 's/-//g'`

sqoop import \
--connect jdbc:mysql://192.168.56.101:3306/mydemo \
--driver com.mysql.jdbc.Driver \
--username root --password 123456 \
--query "select * from myorder where orderdate="\'${nowdate}\'"  and \$CONDITIONS" 
--incremental append \
--check-column orderdate \
--target-dir /mydata1/$foldername -m 1
```

`从RDB导入数据到HBase`

```shell
 sqoop import \
    --connect jdbc:mysql://192.168.56.101:3306/shop \
    --username root \
    --password 123456 \
    --table products \
    --hbase-table customercontactinfo \
    --column-family CustomerName \
    --columns "customernum, customername" \
    --hbase-row-key customernum \
    -m 1

```

`Hive中建立外部表将地址指向对应地址`

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





`HDFS导入mysql`

```shell
sqoop export  \
--connect jdbc:mysql://localhost:3306/sqoop \
--username root --password hadoop \
--table emp_demo \ # mysql创表
--export-dir /data/sqoop/emp \ 
-m 1

```

`导入数据到Hive中`

```shell
sqoop import \
--connect jdbc:mysql://localhost:3306/sqoop \
--driver com.mysql.jdbc.Driver \
--username root --password hadoop \
--table emp_demo \ # mysql创表
--hive-import
--create-hive-table
--hive-database xxx
--hive-table xxx
--m 3
--as parquetfile
```

