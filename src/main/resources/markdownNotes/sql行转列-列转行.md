### sql列转行：

> **核心思想：列值转列名**：往往列值是几个类别不是数值型

> **核心方法：case...when... |  collect_list(列名)**

**案例一：**

![image-20200616184418675](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200616184418675.png)

将上图列值将其转化为下图列名

| country | male | female |
| :-----: | :--: | :----: |
|  china  |  24  |   38   |

---

通常情况下：列值多为类别型，转换为列名后需要记数

**法一：case...when...**

```sql
select 
sum(case when gender='Female' then 1 else 0 end) as female,
sum(case when gender='Male' then 1 else 0 end) as male, country
from customer_details_copy group by country
```

**法二：collect_list()**

```sql
with
t1 as (select size(collect_list(gender)) as female,country from customer_details_copy where gender='Female' group by country),
t2 as (select size(collect_list(gender)) as male,country from customer_details_copy where gender='Male' group by country)
select t1.country,t2.male,t1.female from t1 join t2 on t1.country = t2.country
```



### sql行转列：

> 核心思想：列名转列值
>
> `将多个列名变成列值，那么那一列需要起一个统一的列名，同时将列名对应的值变成新的列`



> 核心方法：union  |   explode(split(列名))（单列名的列值有多个数据，将每个数据打散成行）往往列名没有列值



**法一：union**往往是**多列名想要转为列值**，除了explode的打散成行，还需要将**多个列名对应的值也合起来抽象成新的列名**

![image-20200617011617003](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200617011617003.png)

![image-20200617011633247](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200617011633247.png)



**法二：explode(split(列名))：**

通常是应用在单列有多个数据，将其打散到对应每一行上进行输出

- **常与表生成函数结合使用，将函数的输入和输出连接**

- **OUTER**关键字：**即使**output**为空也会生成结果**

  ```sql
  select name,work_place,loc from employee lateral view outer explode(split(null,',')) a as loc;
  # a是表别名 ，loc是列别名
  ```