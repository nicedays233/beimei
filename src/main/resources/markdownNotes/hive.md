## Hive的作用和优势：

- ### 基于Hadoop的数据仓库解决方案

  >- Hive是基于Hadoop的一个数据仓库工具，将**结构化的数据文件映射为数据库表**。
  >- 提供类sql的查询语言HQL(Hive Query Language)
  >- 数据不放在hive上，放在HDFS上
  >- 由Facebook开源用于**解决海量结构化日志**的数据统计。
  >- 执行程序运行在**Yarn**上

  ---

- ### 优势：

  >- 提供了简单的**优化模型**
  >- HQL类sql语法，简化MR开发
  >- 支持在**HDFS和HBase**上临时查询数据
  >- 支持用户自定义函数，格式
  >- 成熟**JDBC和ODBC**驱动程序，用于ETL和BI
  >- 稳定可靠的**批处理**
  >- 支持在**不同计算框架**运行
  >
  
  ---
  
- ### 缺点：

  >- Hive的**执行延迟比较高**，因此**Hive常用于数据分析**，对实时性要求不高的场合
  >- 迭代式算法无法表达
  >- 数据挖掘方面不擅长
  >
  >- Hive自动生成的**MapReduce作业**，通常情况下不够智能化
  >
  >- Hive调优比较困难，粒度较粗


## Hive的基本架构原理：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20191211152301736.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0JlaWlzQmVp,size_16,color_FFFFFF,t_70#pic_center)

### 1．用户接口：Client

CLI（hive shell）、JDBC/ODBC(java访问hive)、WEBUI（浏览器访问hive）

### 2．元数据：Metastore

元数据包括：表名、表所属的数据库（默认是default）、表的拥有者、列/分区字段、表的类型（是否是外部表）、表的数据所在目录等；
默认存储在自带的derby数据库中，推荐使用MySQL存储Metastore

### 3．Hadoop

使用HDFS进行存储，使用MapReduce进行计算。

### 4．驱动器：Driver

（1）解析器（SQL Parser）：将SQL字符串转换成抽象语法树AST，这一步一般都用第三方工具库完成，比如antlr；对AST进行语法分析，比如表是否存在、字段是否存在、SQL语义是否有误。
（2）编译器（Physical Plan）：将AST编译生成逻辑执行计划。
（3）优化器（Query Optimizer）：对逻辑执行计划进行优化。
（4）执行器（Execution）：把逻辑执行计划转换成可以运行的物理计划。对于Hive来说，就是MR/Spark。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20191211165910975.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0JlaWlzQmVp,size_16,color_FFFFFF,t_70)

Hive通过给用户提供的一系列交互接口，接收到用户的指令(SQL)，使用自己的Driver，结合元数据(MetaStore)，将这些指令翻译成MapReduce，提交到Hadoop中执行，最后，将执行返回的结果输出到用户交互接口。

## Hive的数据类型：

| **类型**    | **示例**                       | **类型**                | **示例**                      |
| ----------- | ------------------------------ | ----------------------- | ----------------------------- |
| **TINYINT** | **10Y**                        | **SMALLINT**            | **10S**                       |
| **INT**     | **10**                         | **BIGINT**              | **100L**                      |
| **FLOAT**   | **1.342**                      | **BINARY**              | **1010**                      |
| **DECIMAL** | **3.14**                       | **STRING**              | **'Book' or "Book"**          |
| **BOOLEAN** | **TRUE**                       | **VARCHAR**             | **'Book' or "Book"**          |
| **CHAR**    | **'YES'or"YES"**               | **TIMESTAMP**           | **'2013-01-31 00:13:00:345'** |
| **DATE**    | **'2013-01-31'**               | **DOUBLE**              | **1.234**                     |
| **ARRAY**   | **['Apple','Orange']**         | **ARRAY<STRING>**       | **a[0] = 'Apple'**            |
| **MAP**     | **{'A':'Apple','0':'Orange'}** | **MAP<STRING, STIRNG>** | **b['A'] = 'Apple'**          |
| **STRUCT**  | **{'Apple',2}**                | **STRUCT<fruit:>**      | **c.weight = 2**              |

## Hive元数据结构：

### 元数据管理:

>**元数据包括：**表名、表所属的数据库（默认是default）、表的拥有者、列/分区字段、表的类型（是否是外部表）、表的数据所在目录等

>- 记录数据仓库中的模型定义
>- 默认存储在自带的derby数据库中，推荐使用MySQL存储Metastore

| 数据结构      | 描述       | 逻辑关系                   | 物理存储           |
| ------------- | ---------- | -------------------------- | ------------------ |
| **Database**  | **数据库** | **表的集合**               | **文件夹**         |
| **Table**     | **表**     | **行数据的集合**           | **文件夹**         |
| **Partition** | **分区**   | **用于分割数据**           | **文件夹**         |
| **Buckets**   | **分桶**   | **用于分布数据**           | **文件**           |
| **Row**       | **行**     | **行记录**                 | **文件中的行**     |
| **Columns**   | **列**     | **列记录**                 | **每行指定的位置** |
| **Views**     | **视图**   | **逻辑概念，可跨越多张表** | **不存储数据**     |
| **Index**     | **索引**   | **记录统计数据信息**       | **文件夹**         |



## Hive的数据库和表操作:

hive interface-命令窗口模式

### 数据表:

- 分为内部表和外部表
- 内部表
  > HDFS中为所属数据库目录下的子文件夹
  > 数据完全由HIve管理,删除表(元数据)会删除数据
- 外部表
  > 数据保存在指定位置的HDFS路径中
  > Hive不完全管理数据,**删除表(元数据)不会删除数据**

java代码



## Hive的数据分区：

## Hive的数据分桶：

## Hive安装：

### 第一步:安装压缩包

```shell
tar -zxf zookeeper-3.4.5-cdh5.14.2.tar.gz
```

```shell
tar -zxf hive-1.1.0-cdh5.14.2.tar.gz
```

```shell
mv zookeeper-3.4.5-cdh5.14.2 soft/zk345
```

```shell
mv hive-1.1.0-cdh5.14.2 soft/hive110
```

---

### 第二步:配置zookeeper

`修改zookeeper的配置文件`

```shell
cd /opt/soft/zk345/conf
cp zoo_sample.cfg zoo.cfg
vi zoo.cfg
```

```shell
# The number of milliseconds of each tick心跳次数
tickTime=2000
# The number of ticks that the initial
# synchronization phase can take
initLimit=10
# The number of ticks that can pass between
# The number of milliseconds of each tick心跳次数
tickTime=2000
# The number of ticks that the initial
# synchronization phase can take
initLimit=10
# The number of ticks that can pass between
# sending a request and getting an acknowledgement异步限制
syncLimit=5
# the directory where the snapshot is stored.
# do not use /tmp for storage, /tmp here is just
# example sakes.文件存放
dataDir=/opt/soft/zk345/tmp
# the port at which the clients will connect端口
clientPort=2181
# the maximum number of client connections.
# increase this if you need to handle more clients
#maxClientCnxns=60
#
# Be sure to read the maintenance section of the
# administrator guide before turning on autopurge.
#
# http://zookeeper.apache.org/doc/current/zookeeperAdmin.html#sc_maintenance
#
# The number of snapshots to retain in dataDir
#autopurge.snapRetainCount=3
# Purge task interval in hours
# Set to "0" to disable auto purge feature
#autopurge.purgeInterval=1
# 2287 领导和跟随者连接用的，传递信息
# 3387 领导挂掉，跟随者之间选领导使用
server.1=192.168.56.101:2287:3387
```

`修改系统配置文件`

```shell
vi /etc/profile
```

`添加全局变量`

```shell
export ZOOKEEPER_HOME=/opt/soft/zk345
export PATH=$PATH:$ZOOKEEPER_HOME/bin
```

``更新配置文件``

```shell
source /etc/profile
```

---

### 第三步:配置hive

`修改hive配置文件`

```shell
cd /opt/soft/hive110/conf
vi hive-site.xml # 没有则添加
```

`添加此配置文件`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
        <!-- 在configuration中加入配置 -->
        <property>
                <name>hive.metastore.warehouse.dir</name>
                <value>/opt/soft/hive110/warehouse</value>
        </property>
        <!--元数据是否在本地，hive和mysql是否在一个服务器上 -->
        <property>
                <name>hive.metastore.local</name>
                <value>false</value>
        </property>
        <!-- 如果是远程mysql数据库的话需要在这里写入远程的IP或hosts -->
        <property>
                <name>javax.jdo.option.ConnectionURL</name>
                <value>jdbc:mysql://192.168.56.101:3306/hive?createDatabaseIfNotExist=true</value>
        </property>
        <property>
                <name>javax.jdo.option.ConnectionDriverName</name>
                <value>com.mysql.jdbc.Driver</value>
        </property>
        <property>
                <name>javax.jdo.option.ConnectionUserName</name>
                <value>root</value>
        </property>
        <property>
                <name>javax.jdo.option.ConnectionPassword</name>
                <value>123456</value>
        </property>
        <property>
                <name>hive.server2.authentication</name>
                <value>NONE</value>
                <description>
                        Expects one of [nosasl, none, ldap, kerberos, pam, custom].
                         Client authentication types.
                         NONE: no authentication check
                         LDAP: LDAP/AD based authentication
                        KERBEROS: Kerberos/GSSAPI authentication
                         CUSTOM: Custom authentication provider
                        (Use with property hive.server2.custom.authentication.class)
                        PAM: Pluggable authentication module
                         NOSASL:  Raw transport
                 </description>
         </property>
         <property>
                <name>hive.server2.thrift.client.user</name>
                <value>root</value>
                <description>Username to use against thrift client</description>
         </property>
         <property>
                <name>hive.server2.thrift.client.password</name>
                <value>root</value>
                <description>Password to use against thrift client</description>
        </property>
</configuration>
```

`修改系统配置文件`

```shell
export HIVE_HOME=/opt/soft/hive110
export PATH=$PATH:$HIVE_HOME/bin
```

`更新配置文件`

```shell
source /etc/profile
```

---

### 第四步:启动HDFS--ZooKeeper--Hive

`启动HDFS`

```shell
start-all.sh
```

`启动zookeeper`

```shell
zkServer.sh start
```

`Hive连接数据库`

> 需将mysql-connector-java-5.1.38.jar复制到/opt/soft/hive110/lib文件夹下

```shell
schematool -dbType mysql initSchema
```

---

### 第五步:启动Hive黑界面

- **beeline黑界面---jdbc黑界面**

  >开两个xshell窗口,分别输入两段命令

	```shell
	hiveserver2
	```
	
	```shell
	beeline -u jdbc:hive2://192.168.56.101:10000 -n root
	```
	
- **mysql黑界面**

  > 开两个xshell窗口,分别输入两段命令 

  `启动Hive元数据存储`
  
  ```shell
  hive --service metastore
  ```
  
  ```shell
  hive
  ```

## Hive基本命令:

> 几乎和mysql一致

- ### 创建数据库:

  ```sql
  create database mydemo;
  ```

  >```sql
  ># 读取数据忽略第一行
  >tblproperties ("skip.header.line.count"="1");
  >```

- ### 创建内部表:

  ```sql
  create table userinfos(
  	userid int,
      username string
  );
  ```

- ### 创建外部表:

  ```sql
  create external table customs(
      cust_id string,
      cust_name string,
      age int
  )
  row format delimited fields terminated by ','
  location '/data';# hdfs 
  ```

- ### 插入表数据:

  ```sql
  insert into userinfos values('1','zs');
  ```

- ### 查询表数据:

  ```sql
  select count(*) from userinfos;
  ```

- ### 修改表元数据:

  ```sql
  ALTER TABLE employee RENAME TO new_employee;
  ALTER TABLE c_employee SET TBLPROPERTIES ('comment'='New name, comments');
  ALTER TABLE employee_internal SET SERDEPROPERTIES ('field.delim' = '$’);
  ALTER TABLE c_employee SET FILEFORMAT RCFILE; -- 修正表文件格式
  -- 修改表的列操作
  ALTER TABLE employee_internal CHANGE old_name new_name STRING; -- 修改列名
  ALTER TABLE c_employee ADD COLUMNS (work string); -- 添加列
  ALTER TABLE c_employee REPLACE COLUMNS (name string); -- 替换列改数据类型
  ```

  

- ### 使用shell命令:

  ```shell
  !hdfs dfs -text /opt/soft/hive110/mydemo.db/userinfos/000000_0
  ```

> **Hive的更新和删除操作需要配置事务**

## Hive建表高阶语句：CTAS-WITH

#### CATS-as select 方式建表

```shell
create table ctas_employee as select * from employee
```

#### CTE(CATS with common table expression )

```sql
# with 得三张表顺序无所谓 
CREATE TABLE cte_employee AS
WITH 
r1 AS  (SELECT name FROM r2 WHERE name = 'Michael'),
r2 AS  (SELECT name FROM employee WHERE sex_age.sex= 'Male'),
r3 AS  (SELECT name FROM employee  WHERE sex_age.sex= 'Female')
SELECT * FROM r1 UNION ALL SELECT * FROM r3;
```

#### `hive和mysql对比`

```sql
# mysql
select r.username,r.classname,r.score,r.score/l.countScore *100 
from(select classname,sum(score) countScore from scores group by classname) l 
inner join(select u.*,s.classname,s.score from userinfos u inner join scores s on u.userid=s.userid) r 
on l.classname = r.classname

# hive
with a1 as(select classname,sum(score) countScore from scores group by classname),a2 as(select u.*,s.classname,s.score from userinfos u inner join scores s on u.userid=s.userid) select a2.username,a2.classname,a2.score,(a2.score/a1.countScore*100) from a1 inner join a2 on a1.classname=a2.classname;
```

#### 创建临时表

> **临时表是应用程序自动管理在复杂查询期间生成的中间数据的方法**

- 表只对当前session有效，session退出后自动删除

- 表空间位于/tmp/hive-<user_name>(安全考虑)

- 如果创建的临时表表名已存在，实际用的是临时表

```sql
CREATE TEMPORARY TABLE tmp_table_name1 (c1 string);
CREATE TEMPORARY TABLE tmp_table_name2 AS..
CREATE TEMPORARY TABLE tmp_table_name3 LIKE..
```

## Hive分区：-partition

- 创建分区表

```sql
CREATE TABLE employee_partitioned(
    name string,
    work_place ARRAY<string>,
    sex_age STRUCT<sex:string,age:int>,
    skills_score MAP<string,int>,
    depart_title MAP<STRING,ARRAY<STRING>> )
PARTITIONED BY (year INT, month INT)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
COLLECTION ITEMS TERMINATED BY ','
MAP KEYS TERMINATED BY ':';

```



- 分区主要用于**提高性能**

  - 分区列的值将表划分为segments（文件夹）
  - 查询时使用分区列和常规列类似
  - 查询Hive自动过滤不用于提高性能的分区

- 分为**静态分区**和**动态分区**

- 

  `静态分区`--相当于**指定手动创建**

  ```sql
  ALTER TABLE employee_partitioned ADD 
  PARTITION (year=2019,month=3) PARTITION (year=2019,month=4); 
  ALTER TABLE employee_partitioned DROP PARTITION (year=2019, 
  ```

  ```sql
  insert into 追加
  
  insert overwrite into覆盖 拉链表 全量表
  ```

  - 添加静态分区的数据

  ```sql
  # 塞值
  insert into mypart partition(gender='male') values(1,'zs');
  
  # 塞表 静态塞值的时候不需要塞分区字段名
  insert overwrite table mypart partition(gender='female')
  select userid,username from userinfos;
  
  # 如果塞的表和分区的分区字段不一致，会强行把表的分区字段变为一致
  # 就是到这个分区，这个分区的字段都变为一致。
  ```

  ---

  `动态分区`--

  - 使用动态分区需设定属性--开启动态分区

  ```sql
  set hive.exec.dynamic.partition=true;
  set hive.exec.dynamic.partition.mode=nonstrict;
  ```

  - 动态分区设置方法

  ```sql
   # 给一张表的对应分区里插入另一张表的数据，静态塞值的时候不需要塞分区字段名
  insert into table employee_partitioned partition(year, month)
  select name,array('Toronto') as work_place,
  named_struct("sex","male","age",30) as sex_age,
  map("python",90) as skills_score,
  map("r&d", array('developer')) as depart_title,
  year(start_date) as year,month(start_date) as month
  from employee_hr eh;
  ```
```
  
  ```sql
   # 给一张表的对应分区里插入另一张表的数据，静态塞值的时候不需要塞分区字段名
   insert into table mypart partition(gender) 
   select userid,username,gender from userinfos;
  
```

- 设置动态分区的个数上限
  
  ```sql
  set hive.exec.max.created.files=600000;
  ```
```
  
- 加载本地数据文件到hive数据库表
  
  ```sql
   load data local inpath '/opt/wyw.xlsx' overwrite into table mydemo.customs2;
```

- 将一张表导入另一张表
  
  ```sql
   # 给一张表的对应分区里插入另一张表的数据，静态塞值的时候不需要塞分区字段名
   insert into table mypart partition(gender) 
   select userid,username,gender from userinfos;
  ```
```
  

  
  ```sql
  insert overwrite table userinfos partition(year,month) select userid,username,age,regexp_replace(birthday,'/','-'),gender,split(birthday,'/')[0] as year, split(birthday,'/')[1] as month from customs3;
```

## Hive分桶：-Buckets

#### 分桶对应于HDFS中的文件

- 更高的查询处理效率
- 使抽样(sampling)更高效
- 根据“桶列”的哈希函数将数据进行分桶

#### 分桶只有动态分桶

- ```sql
  set hive.enforce.bucketing=true;
  ```

#### 定义分桶

- ```sql
  # 分桶列是表中已有列
  # 分桶数是2的n次方
  # 直接分文件，不是分文件夹
  create table xxx()
  clustered by (employee_id) into 2 buckets
  ```

#### 必须用insert方式加载数据



#### 分桶抽样（Sampling）：

- 随机抽样基于整行数据

  ```sql
  
  SELECT * FROM table_name TABLESAMPLE(BUCKET 3 OUT OF 32 ON rand()) s;
  ```
```
  
- 随机抽样基于指定列

  ```sql
  # 3 是指从所有桶中的32个不同种类里的任意3行数据
  SELECT * FROM table_name TABLESAMPLE(BUCKET 3 OUT OF 32 ON id) s;
```

  

- 随机抽样基于block size

  ```sql
  SELECT * FROM table_name TABLESAMPLE(10 PERCENT) s;
  SELECT * FROM table_name TABLESAMPLE(1M) s;
  SELECT * FROM table_name TABLESAMPLE(10 rows) s;
  
  ```

  

```sql
create table customs3(userid int, username string,age int,birthday string,gender string) row format delimited fields terminated by ','
```



## 索引--分区--分桶：

**索引和分区**`最大的区别`就是索引**不分割**数据库，分区**分割**数据库。

> 索引其实就是拿额外的存储空间换查询时间，但分区已经将整个大数据库按照分区列拆分成多个小数据库了。

 

**分区和分桶**`最大的区别`就是分桶**随机**分割数据库，分区是**非随机**分割数据库。

> 因为分桶是按照列的哈希函数进行分割的，相对比较平均；而分区是按照列的值来进行分割的，容易造成数据倾斜。

> 其次两者的另一个区别就是分桶是对应不同的文件（细粒度），分区是对应不同的文件夹（粗粒度）。

注意：普通表（外部表、内部表）、分区表这三个都是对应HDFS上的目录，桶表对应是目录里的文件



## Hive视图操作：

#### **视图概述**

- 通过隐藏子查询、连接和函数来简化查询的逻辑结构

- 虚拟表，从真实表中选取数据

- 只保存定义，不存储数据

- 如果删除或更改基础表，则查询视图将失败

- 视图是只读的，不能插入或装载数据

#### **应用场景**

- 将特定的列提供给用户，保护数据隐私

- 查询语句复杂的场景

#### 视图操作命令：

- 创建表的一种方式

**CREATE VIEW view_name AS SELECT statement from xxx; -- 创建视图**

```sql
CREATE VIEW view_name AS SELECT statement from xxx; -- 创建视图
	-- 创建视图支持 CTE, ORDER BY, LIMIT, JOIN, etc.
SHOW TABLES; -- 查找视图 (SHOW VIEWS 在 hive v2.2.0之后)
SHOW CREATE TABLE view_name; -- 查看视图定义
DROP view_name; -- 删除视图
ALTER VIEW view_name SET TBLPROPERTIES ('comment' = 'This is a view');
--更改视图属性
ALTER VIEW view_name AS SELECT statement; -- 更改视图定义
```

#### Hive侧视图（lateral view）--当列有多个数据又想把其与所对应行一一匹配，则用侧视图

- **常与表生成函数结合使用，将函数的输入和输出连接**

- **OUTER**关键字：**即使**output**为空也会生成结果**

  ```sql
  select name,work_place,loc from employee lateral view outer explode(split(null,',')) a as loc;
  # a是表别名 ，loc是列别名
  ```

- **支持多层级**

  ```sql
  select name,wps,skill,score from employee 
  lateral view explode(work_place) work_place_single as wps
  lateral view explode(skills_score) sks as skill,score;
  ```

- **通常用于规范化行或解析JSON**







beeline黑界面是jdbc 

,mysql黑界面

![image-20200720105559289](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200720105559289.png)

#### Hive执行顺序：

(1)from
(2)on
(3)join
(4)where
(5)group by
(6)having
(7)select
(8)distinct
(9)distribute by /cluster by
(10)sort by
(11) order by
(12) limit
(13) union /union all