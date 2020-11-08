## Hive分区简介：

### 分区的方式：

- `动态分区`
- `静态分区`

### 分区的作用：

`分区主要用于提高性能`

> **没有分区的存在，那么每次查询Hive将会进行全表扫描**

---

- 分区列的值将表划分为**segments（文件夹）**
- 查询时使用**分区列和常规列**类似
- 查询Hive自动过滤不用于提高性能的分区

---

> **主要是以缩小数据查询范围，提高查询速度和性能的**

### 分区的配置：

```sql
-- Hive默认配置值
-- 开启或关闭动态分区 true 为开启
hive.exec.dynamic.partition=true;

-- 设置为nonstrict模式，让所有分区都动态配置，否则至少需要指定一个分区值
hive.exec.dynamic.partition.mode=nonstrict;

-- 能被mapper或reducer创建的最大动态分区数，超出而报错
hive.exec.max.dynamic.partitions.pernode=100;

-- 一条带有动态分区SQL语句所能创建的最大动态分区总数，超过则报错
hive.exec.max.dynamic.partitions=1000;

-- 全局能被创建文件数目的最大值，通过Hadoop计数器跟踪，若超过则报错
hive.exec.max.created.files=100000;


```

## 分区的具体过程：

### 创建分区：

> 一般来说外部表是ods层的数据原始层，内部表是dwd层的细节数据层
>
> 分区表一般是内部表。

- `创建分区表`--动态和静态的创建方式一样

```sql
# 数据原始层的外部表
CREATE external TABLE employee_partitioned(
    name string,
    work_place ARRAY<string>,
    sex_age STRUCT<sex:string,age:int>,
    skills_score MAP<string,int>,
    depart_title MAP<STRING,ARRAY<STRING>> 
)
# 导入表时以|为分隔符
ROW FORMAT DELIMITED FIELDS TERMINATED BY '|'
# 集合以,为分割符
COLLECTION ITEMS TERMINATED BY ','
# map以：为分割符
MAP KEYS TERMINATED BY ':';


# 近源层的细节数据层
CREATE TABLE employee_partitioned_copy(
    name string,
    work_place ARRAY<string>,
    sex_age STRUCT<sex:string,age:int>,
    skills_score MAP<string,int>,
    depart_title MAP<STRING,ARRAY<STRING>> 
)
# 创表时先设分区
PARTITIONED BY (year INT, month INT)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '|'
COLLECTION ITEMS TERMINATED BY ','
MAP KEYS TERMINATED BY ':';

```

### 设置分区：

`静态分区`--相当于**指定手动创建**

```sql
ALTER TABLE employee_partitioned_copy ADD 
PARTITION (year=2019,month=3) PARTITION (year=2019,month=4); 
ALTER TABLE employee_partitioned_copy DROP PARTITION (year=2019, month=4)
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

- 设置动态分区的个数上限

```sql
set hive.exec.max.dynamic.partitions.pernode=600000;
set hive.exec.max.dynamic.partitions=6000000;
set hive.exec.max.created.files=600000;
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



```sql
insert overwrite table userinfos partition(year,month) select userid,username,age,regexp_replace(birthday,'/','-'),gender,split(birthday,'/')[0] as year, split(birthday,'/')[1] as month from customs3;
```

### 向分区插入数据：

- `建表时：插入数据`

  - 创建表时本地插入

  ```sql
  create table customs(
      cust_id string,
      cust_name string,
      age int
  )
  row format delimited fields terminated by ','
  ```

  - 创建表时HDFS插入

  ```sql
  -- 内部分区表的HDFS创建导入
  create table customs(
      cust_id string,
      cust_name string,
      age int
  )
  row format delimited fields terminated by ','
  location '/data';# hdfs 
  ```

  

- `建表后：HDFS插入数据`

```sql
-- 此路径填写hdfs路径
 load data inpath '/mydemo/wyw.xlsx' overwrite into table mydemo.customs2;
```

- `建表后：本地插入数据`

  - **插入文件**

  ```sql
   # 本地全量插入
   load data local inpath '/opt/wyw.xlsx' overwrite into table mydemo.customs2;
  ```

- `建表后：表数据导入另一张表`

```sql
 # 给一张表的对应分区里插入另一张表的数据，动态塞值的时候需要塞分区字段名
 #  给一张表的对应分区里插入另一张表的数据，静态塞值的时候不需要塞分区字段名
insert into table mypart 
select userid,username,gender 
from userinfos;
```

- `建表后：直接插入语句插入数据`

```sql
 insert into table mypart 
 values(1,'zs');
```

### 