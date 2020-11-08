## Spark小技巧：

### 去除首尾不需要行数并把两行数据并称一行：

```txt
pioopwirwr
sdfsfdsfsd
seirtoert
ert342
sdfshfhfghfh
wperiwpo234242
sdfsfkjsfkjsf;sk
kjsf;ks;fls
sfsfsdk
sfsdf;klj;lsfsfds
sfsf
...222
2222
23424lksf;lsfsfds
23425353
```

```scala
val rdd = sc.textfile(fileName).zipWithIndex.cache
// 去除首尾不需要行数
val df = rdd.filter(seqo......).toDF

val df1 = df.filter($"seqNo" % 2 = 1)
val df2 = df.filter($"seqNo" % 2 = 0)

val dfresult = df1.join(df12, df1("seqNo") + 1 === df("seqNo"), "inner").select("result", concat(df1.value, df2.value))
```

![image-20200918163817117](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200918163817117.png)



#### 对列填充值

```scala
    val res = usrAction
      .join(buygoods, Seq("cust_id", "good_id"), "left")
      .join(users, Seq("cust_id"),"inner")
      .join(goods, Seq("good_id"), "inner")
//      .withColumn("buynum",nanvl($"buynum",lit("100")))
      .na.fill(Map("buy_time" -> "190001", "buynum" -> "0", "count_price" -> "0"))
    res.na.ensuring()

```



#### 对所有列转换类型

```scala
//     对所有列转换类型
    val cols = res.columns.map(x => col(x).cast(StringType))
    res.select(cols : _*)
    res.columns.mkString(",")
    orders.columns.map(x => println(x))
```

