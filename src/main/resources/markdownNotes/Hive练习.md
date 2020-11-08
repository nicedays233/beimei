#### 查询订单表中共有多少不同顾客下单？

```sql
# 大表在前 ，小表在后
select concat(customer_fname,customer_lname) name 
from customers as c 
inner join (select order_customer_id from orders  group by order_customer_id) as a 
on a.order_customer_id=c.customer_id; 
```

```sql
# orders小表在前，大表在后
with
	t1 as (select order_customer_id from orders group by order_customer_id)
	select c.customer_id,concat(customer_fname,'.',customer_lname) as name
	from t1 t innner join customers c on t.order_customer_id = c.customer_id;
```

```sql
# exist 性能更快
# 先拿外面的表，然后触发exists函数检查有没有这个值，有就显示，没有就不显示
select c.customer_id,concat(customer_fname,'.',customer_lname) as name
from customers c 
where exists(select order_customer_id from orders s where s.order_customer_id = c.customer_id)
```



#### 使用关联查询获取没有订单的所有顾客

```sql
# exist
select c.customer_id,concat(customer_fname,'.',customer_lname) as name 
from customers c 
where not exists(select order_customer_id from orders s where s.order_customer_id = c.customer_id);
```

```sql
# 左外联查null，拿表值
select l.username,r.score from userinfos l left join scores r 
on 1.userid = userid where r.score is null;
```

