## Phoenix应用场景：

- Phoenix适合场景
  - 快速构建基于HBase得应用程序
  - 需要极大规模，性能和并发性得sql应用程序
  - 转换hadoop时重用已有sql技能
  - BI工具
- 不适合场景：
  - 涉及大型join操作或高级sql特性的复杂sql查询
  - full-table scans
  - ETL jobs

### PhoenixSQL语法：

| **Java API Code**                                            | **Phoenix** **DDL**                                          |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| HBaseAdmin hbase = new HBaseAdmin(conf);  HTableDescriptor desc = new HTableDescriptor("us_population");  HColumnDescriptor state = new HColumnDescriptor("state".getBytes());  HColumnDescriptor city = new HColumnDescriptor("city".getBytes());  HColumnDescriptor population = new HColumnDescriptor("population".getBytes());  desc.addFamily(state);  desc.addFamily(city);  desc.addFamily(population);  hbase.createTable(desc); | CREATE TABLE us_population (  state CHAR(2) NOT NULL,  city VARCHAR NOT NULL,  population BIGINT  CONSTRAINT my_pk PRIMARY KEY (state, city)  );  • |
| •使用更灵活  •可与其他应用集成                               | •常用的SQL语法  •提供附加约束检查                            |

### Phoenix支持关键字类型：

>Standard SQL Data Types --标准SQL 数据类型
>
>SELECT, UPSERT, DELETE --UPSERT与标准SQL不同
>
>JOINs: Inner and Outer
>
>Subqueries
>
>Secondary Indexes
>
>GROUP BY, ORDER BY, HAVING
>
>AVG, COUNT, MIN, MAX, SUM
>
>Primary Keys, Constraints
>
>CASE, COALESCE
>
>VIEWs
>
>PERCENT_RANK, LAST|FIRST VALUE
>
>UNION ALL
>
>Cross Joins
>
>Windowing Functions --窗口函数
>
>Transactions --事务
>
>Authorization
>
>Replication Management





## Phoenix安装步骤：

### 第一步：解压tar，并创建文件夹

```shell
tar zxvf apache-phoenix-4.14.0-cdh5.14.2-bin.tar.gz
mv apache-phoenix-4.14.0-cdh5.14.2-bin /opt/soft/phoenix414
```

### 第二步：复制server.jar到hbase上,并重启hbase

```shell
cp phoenix-4.14.0-cdh5.14.2-server.jar /opt/soft/hbase120/lib/
stop-hbase.sh
start-hbase.sh
```

### 第三步：去phoenix得bin目录启动

```shell
cd /opt/soft/phoenix414/bin
./sqlline.py 
```

![image-20200721131905283](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200721131905283.png)

## Phoenix操作hbase：

### 查看表：

```shell
!table
```

### 创建表：

```sql
CREATE TABLE company (
    COMPANY_ID INTEGER PRIMARY KEY,
    NAME VARCHAR(225)
); 
```

### 插入数据：

```sql
UPSERT INTO company VALUES(1, 'Microsoft');  
```

### 查看数据：

```sql
SELECT * FROM Company;
```

### join表：

```sql
SELECT s.COMPANY_ID,c.NAME,s.PRICE
FROM stock s 
JOIN company c
ON c.COMPANY_ID=s.COMPANY_ID
```

