### hive常见语法总结

```
CH1
(1).Hive不支持join的非等值连接,不支持or
分别举例如下及实现解决办法。
  不支持不等值连接
       错误:select * from a inner join b on a.id<>b.id
       替代方法:select * from a inner join b on a.id=b.id and a.id is null;
 不支持or
       错误:select * from a inner join b on a.id=b.id or a.name=b.name
       替代方法:select * from a inner join b on a.id=b.id
                union all
                select * from a inner join b on a.name=b.name
  两个sql union all的字段名必须一样或者列别名要一样。
		
(2).分号字符:不能智能识别concat(‘;’,key)，只会将‘；’当做SQL结束符号。
	•分号是SQL语句结束标记，在HiveQL中也是，但是在HiveQL中，对分号的识别没有那么智慧，例如：
		•select concat(key,concat(';',key)) from dual;
	•但HiveQL在解析语句时提示：
        FAILED: Parse Error: line 0:-1 mismatched input '<EOF>' expecting ) in function specification
	•解决的办法是，使用分号的八进制的ASCII码进行转义，那么上述语句应写成：
		•select concat(key,concat('\073',key)) from dual;

(3).不支持INSERT INTO 表 Values（）, UPDATE, DELETE等操作.这样的话，就不要很复杂的锁机制来读写数据。
	INSERT INTO syntax is only available starting in version 0.8。INSERT INTO就是在表或分区中追加数据。

(4).HiveQL中String类型的字段若是空(empty)字符串, 即长度为0, 那么对它进行IS NULL的判断结果是False，使用left join可以进行筛选行。

(5).不支持 ‘< dt <’这种格式的范围查找，可以用dt in(”,”)或者between替代。

(6).Hive不支持将数据插入现有的表或分区中，仅支持覆盖重写整个表，示例如下：
    INSERT OVERWRITE TABLE t1 SELECT * FROM t2;
	
(7).group by的字段,必须是select后面的字段，select后面的字段不能比group by的字段多.
	如果select后面有聚合函数,则该select语句中必须有group by语句
	而且group by后面不能使用别名
	
(8).hive的0.13版之前select , where 及 having 之后不能跟子查询语句(一般使用left join、right join 或者inner join替代)

(9).先join(及inner join) 然后left join或right join

(10).hive不支持group_concat方法,可用 concat_ws('|', collect_set(str)) 实现

(11).not in 和 <> 不起作用,可用left join tmp on tableName.id = tmp.id where tmp.id is null 替代实现
... ...


CH2
(1).不支持非等值连接，一般使用left join、right join 或者inner join替代。
	•SQL中对两表内联可以写成：
		select * from dual a,dual b where a.key = b.key;
	•Hive中应为:
		select * from dual a join dual b on a.key = b.key; 
	而不是传统的格式：
		SELECT t1.a1 as c1, t2.b1 as c2 FROM t1, t2 WHERE t1.a2 = t2.b2	
		
(2).分号字符:不能智能识别concat(‘;’,key)，只会将‘；’当做SQL结束符号。
	•分号是SQL语句结束标记，在HiveQL中也是，但是在HiveQL中，对分号的识别没有那么智慧，例如：
		•select concat(key,concat(';',key)) from dual;
	•但HiveQL在解析语句时提示：
        FAILED: Parse Error: line 0:-1 mismatched input '<EOF>' expecting ) in function specification
	•解决的办法是，使用分号的八进制的ASCII码进行转义，那么上述语句应写成：
		•select concat(key,concat('\073',key)) from dual;

(3).不支持INSERT INTO 表 Values（）, UPDATE, DELETE等操作.这样的话，就不要很复杂的锁机制来读写数据。
	INSERT INTO syntax is only available starting in version 0.8。INSERT INTO就是在表或分区中追加数据。

(4).HiveQL中String类型的字段若是空(empty)字符串, 即长度为0, 那么对它进行IS NULL的判断结果是False，使用left join可以进行筛选行。

(5).不支持 ‘< dt <’这种格式的范围查找，可以用dt in(”,”)或者between替代。

(6).Hive不支持将数据插入现有的表或分区中，仅支持覆盖重写整个表，示例如下：
    INSERT OVERWRITE TABLE t1 SELECT * FROM t2;
	
(7).group by的字段,必须是select后面的字段，select后面的字段不能比group by的字段多.
	如果select后面有聚合函数,则该select语句中必须有group by语句;
	而且group by后面不能使用别名;
	有聚合函数存在就必须有group by.
	
(8).select , where 及 having 之后不能跟子查询语句(一般使用left join、right join 或者inner join替代)

(9).先join(及inner join) 然后left join或right join

(10).hive不支持group_concat方法,可用 concat_ws('|', collect_set(str)) 实现

(11).not in 和 <> 不起作用,可用left join tmp on tableName.id = tmp.id where tmp.id is null 替代实现

(12).hive 中‘不等于’不管是用！ 或者<>符号实现，都会将空值即null过滤掉，此时要用
		where （white_level<>'3' or  white_level is null） 
	或者 where (white_level!='3' or white_level is null )  来保留null 的情况。

(13).union all 后面的表不加括号,不然执行报错;
	hive也不支持顶层的union all，使用子查询来解决;
	union all 之前不能有DISTRIBUTE BY | SORT BY| ORDER BY | LIMIT 等查询条件
	
	
	
	
	
CH3	
1.case when ... then ... else ... end

2.length(string)

3.cast(string as bigint)

4.rand()       返回一个0到1范围内的随机数

5.ceiling(double)    向上取整

6.substr(string A, int start, int len)

7.collect_set(col)函数只接受基本数据类型，它的主要作用是将某字段的值进行去重汇总，产生array类型字段

8.concat()函数
	1、功能：将多个字符串连接成一个字符串。
	2、语法：concat(str1, str2,...)
	返回结果为连接参数产生的字符串，如果有任何一个参数为null，则返回值为null。

	9.concat_ws()函数
	1、功能：和concat()一样，将多个字符串连接成一个字符串，但是可以一次性指定分隔符～（concat_ws就是concat with separator）
	2、语法：concat_ws(separator, str1, str2, ...)
	说明：第一个参数指定分隔符。需要注意的是分隔符不能为null，如果为null，则返回结果为null。

	10.nvl(expr1, expr2)：空值转换函数  nvl(x,y)    Returns y if x is null else return x

11.if(boolean testCondition, T valueTrue, T valueFalse)

12.row_number()over()分组排序功能,over()里头的分组以及排序的执行晚于 where group by  order by 的执行。

13.获取年、月、日、小时、分钟、秒、当年第几周
	select 
		year('2018-02-27 10:00:00')       as year
		,month('2018-02-27 10:00:00')      as month
		,day('2018-02-27 10:00:00')        as day
		,hour('2018-02-27 10:00:00')       as hour
		,minute('2018-02-27 10:00:00')     as minute
		,second('2018-02-27 10:00:00')     as second
		,weekofyear('2018-02-27 10:00:00') as weekofyear
  获取当前时间:
		1).current_timestamp
		2).unix_timestamp()
		3).from_unixtime(unix_timestamp())
		4).CURRENT_DATE


```

