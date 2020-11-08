

二级查询：

```sql
SELECT * FROM STSCORE where course='English' ${if(len(classno) == 0,"","and classno='" + classno + "'")} ${if(len(studentno)==0,"","and studentno='" + studentno + "'")}
order by grade ${if(len(sj) == 0, "asc", "")}
```



班级总分及平均分查询

```sql
SELECT classno,studentno,name,
sum(case course when 'English'  then grade else 0 end) as english,
sum(case course when 'Math'  then grade else 0 end) as math,
sum(case course when 'French'  then grade else 0 end) as french,
sum(case course when 'Chemistry'  then grade else 0 end) as chemistry,
sum(case course when 'Physics'  then grade else 0 end) as physics
FROM STSCORE group by classno,studentno,name
```





查询所有，不选默认查询所有

```sql
SELECT studentno FROM STSCORE where 1=1 ${if(len(classno) == 0, "", "and classno='" + classno + "'")}
```







```sql
SELECT * FROM STSCORE where course='English' ${if(len(classno) == 0,"","and classno='" + classno + "'")} ${if(len(studentno) == 0,"","and studentno in (" + studentno + ")")}
${if(len(sj) == 0, "order by grade", "order by grade asc")}
```





```sql
select 地区,sum(销量) from sales_basic group by 地区
```

