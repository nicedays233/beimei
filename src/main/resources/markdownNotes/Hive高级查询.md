## Hive高级查询：

### Hive数据查询：

`SELECT`：略

`CTE(Common Table Expression)`

- CTE

```sql

```

`进阶语句`

- 列名匹配正则表达式

```sql
SET hive.support.quoted.identifiers
select `o.*` from 
```



- 虚拟列

`关联查询`

- **内联**--inner join

- **左外联**--left  outer join

- **右外联**--right outer join

- **全联**--full outer join

- **交叉连接**--cross join

  笛卡尔积：向量乘积

- **隐式连接**--implicit join

### Hive数据关联：

### Hive数据合并：

### Hive数据加载与交换：

### Hive数据排序：

`order by`

- 只使用一个Reducer执行全局数据排序

- 速度慢，应提前做好数据过滤

- 支持使用case when或表达式

- 支持按位置编号排序

  ```sql
  set hive.groupby.orderby.position.alias=true
  ```

  >  **如何把null排最后？：降序null自动在最后，升序null自动在最前** 或者用case when

  

`sort by ~ （distribute by 相同列名）sort by 相同列名 ` 

设置reduce数量

```sql
set.mapred.reduce.tasks=2
```

- 当reducer数量设置为1时，等于order by 
- 排序列**必须出现在 select column 列表中**

`distribute by`--相当于partition分区--mapreduce

- 确保具有匹配列值的行被分区到**相同的Reducer**
- **不会**对每个reducer的输出进行排序
- 通常使用**sort by之前**





`cluster by = distribute by + sort by`

- **排序只能是升序排序（默认排序规则），不能指定排序规则为asc 或者desc。**
- 



coll

### Hive聚合运算-基础聚合

#### 行转列：行变竖，列值转列名

- ​	collect_set,collect_list返回每个组列中的对象集/列表--**转行**
- inner join
- case when

#### 列转行：竖变行，列名转列值

- **侧视图**

- union

  > 将**分组中的某列转为一个数组返回**

```sql
select classname,collect_list(score)[1] from scores;
```

#### 多重group：

- 本质是对多个GROUP BY进行UNION ALL操作

| grouping sets语句                                            | 等价于group by语句                                           |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| select a,b,sum(c) from tab1 <br /> group by a,b<br /> grouping sets ((a,b),a,b,()) | SELECT a, b, SUM( c ) FROM tab1 GROUP BY a, b s<br /><br />UNION SELECT a, null, SUM( c ) FROM tab1 GROUP BY a, null<br /> UNION SELECT null, b, SUM( c ) FROM tab1 GROUP BY null, b<br /> UNION SELECT null, null, SUM( c ) FROM tab1 |

### Hive窗口函数：

#### 聚合函数+over：  // 全局一个窗口

```sql
# 之前的字段名先执行，然后窗口将聚合的结果一一匹配到对应得元组
select distinct name,count(*) over ()
from t_window
where substring(orderdate,1,7) = '2015-04'
```

#### 聚合函数+over（partition by ）  // 自己选择分窗口

#### 聚合函数+over（partition by order by ）  // 窗口强制排序

#### row_number + over（order by ）  // 无重复排序 1,2,3,4

#### rank() + over（order by ）  // 并列名次 跳 1,1,1,3

#### dense_rank() + over（order by ）  // 并列名次 不跳 1,2,3,4

#### LAG和LEAD函数

 `lag`---设置指定列查看之前得字段值--lag(列，x)找上x笔数据，没有就用null补

```sql

```

`lead`---设置指定列查看之后得字段值--lead(列，x)找下x笔数据，没有就用null补

#### first_value 和 last_value

`first_value`---在分组排序后，**截至当前窗口当前行指针**，**获取指定得列得第一个值**，动态计算

```sql

```

`last_value`---在分组排序后，**截至当前窗口当前行指针 ， **获取 **指定得列得最后一个值** ，动态计算

#### sum|max...() over(partition by ... order by ... between x and y)

x| y => UNBOUNDED PRECEDING（**窗口首行**） UNBOUNDED FOLLING（**窗口最后一行**）

​			n PRECEDING （**向前N行**）n FOLLOWING （**向后N行**）			CURRENT ROW（**当前行**）

`游标winodow子句`：

### ps:解决csv的逗号问题(表格里不解析)

```sql
create external table if not exists transaction_details (
    transaction_id string,
    customer_id string,
    store_id string,
    price string,
    product string,
    date string,
    time string
)
-- 解决csv中有逗号的情况
row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    "separatorChar" = ",",
    "quoteChar" = "\"",
    "escapeChar" = "\\"
)
STORED AS TEXTFILE
tblproperties ("skip.header.line.count"="1")

load data local inpath '/opt/shop/transaction_details.csv' overwrite into table transaction_details
```

