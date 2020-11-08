### DataFrame&DataSet算子：

##### 常用转换算子：

- `toDF算子: def toDF() : DataFrame`
- 

- `isStreaming算子：def isStreaming : scala.Boolean`

- 

- `show算子： def show(numRows : Int, truncate : Boolean) : Unit`

  ```js
  show()//默认显示20行，字段值超过20，默认截断
  show(numRows: Int)//指定显示行数
  show(truncate: Boolean)//指定是否截断超过20的字符
  show(numRows: Int, truncate: Boolean)//指定行数，和是否截断
  show(numRows: Int, truncate: Int)//指定行数，和截断的字符长度
  ```

  

- `as算子: def as(alias : String) : Dataset[T]`
- 
- `alias算子: def as(alias : String) : Dataset[T]`
- 

- `na算子：def na : DataFrameNaFunctions`
- 

- `stat算子：def stat : DataFrameStatFunctions`

- 

- `join算子：`

  - `def join(right : Dataset[_], joinExprs : Column, joinType : String) : DataFrame`
  - 
  - `def join(right : Dataset[_], joinExprs : Column) : DataFrame`
  - 
  - `def join(right : Dataset[_],  usingColumns : Seq[String]) : DataFrame`
  - 
  - `def join(right : Dataset[_],  usingColumns : Seq[String], joinType : String) : DataFrame`
  - 
  - `def join(right : Dataset[_],  usingColumn : String) : DataFrame`
  - 
  - `def join(right : Dataset[_]) : DataFrame`
  - 

- `crossJoin算子： def crossJoin(right : Dataset[_]) : DataFrame `

- 

- `joinWith算子： def joinWith[U](other : Dataset[U], condition : Column, joinType : String) :Dataset[Tuple2[T, U]] `--jointype可省略

- 

- `sortWithPartitions算子：`

  > 类似hive的sort by，只在分区内排序，默认降序

  - `def sortWithinPartitions(sortCol : String, sortCols : String*) : Dataset[T]`
  - 
  - ` def sortWithinPartitions(sortExprs : Column*) : Dataset[T]`

- `sort算子：`

  - `def sort(sortCol : String, sortCols :String*) : Dataset[T]`
  - 
  - ` def sort(sortExprs : Column*) : Dataset[T]` 

- 

- `order算子:`

  - ` def orderBy(sortCol : String, sortCols : String*) : Dataset[T]`
  - 
  - ` def orderby(sortExprs : Column*) : Dataset[T]` 

- 

- `apply算子：def apply(colName : String) : Column`

- 

- `colRegex算子：colRegex(colName : String) : Column`

- 

- `col算子：def col(colName : String) : Column`

- 

- `rollup算子： def rollup(col1 : String, cols : String*) : RelationalGroupedDataset`

- 

- `hint算子：def hint(name : String, parameters : Any*) : Dataset[T]`

  ```js
  df1.join(df2.hint("broadcast"))//将df2广播
  ```

  

- `groupByKey算子：def groupByKey[K](func : Function1[T, K]) : KeyValueGroupedDataset[K, T]`

- `limit算子：def limit(n : Int) : Dataset[T]`

- `agg算子：`

  - ` def agg(aggExpr : Tuple2[String, String], aggExprs : Tuple2[String, String]*) : DataFrame` 
  - 
  - `def agg(exprs : Map[String, String]) : DataFrame`
  - 
  - `def agg(exprs : Map[String, String]) : DataFrame`
  - 
  - ` def agg(expr : Column, exprs : Column*) : DataFrame` 
  - 

- `union算子:def union(other : Dataset[T]) : Dataset[T]`

- 

- `unionAll算子:def union(other : Dataset[T]) : Dataset[T]`

- 

- `unionByName算子:def union(other : Dataset[T]) : Dataset[T]`

- 

- `intersect算子:def intersect(other : Dataset[T]) : Dataset[T]`

- 

- `except算子： def except(other : Dataset[T]) : Dataset[T]`

- 

- `explode算子：def explode[A, B](inputColumn : String, outputColumn : String)(f : Function1[A, TraversableOnce[B]]): DataFrame`

- 

- `withColumn算子：`

- `withColumnRenamed算子：def` `withColumnRenamed(existingName : String, newName : String) : DataFrame`

- 

- `drop算子：`

  - ` def drop(colName : String) : DataFrame`
  - ` def drop(colNameS : String*) : DataFrame`
  - `def drop(col : Column) : DataFrame`

- 

- `dropDuplicates算子：`

  - ` def dropDuplicates() : Dataset[T] `
  - ` def dropDuplicates(colNames : Seq[String]) : Dataset[T]`
  - `def dropDuplicates(colNames : Array[String]) : Dataset[T]`
  - `def dropDuplicates(col1 : String, cols : String*) : Dataset[T]`

- 

- `head算子： def head(n : Int) : Array[T]`

- 

- `transform算子： def transform[U](t : Function1[Dataset[T],Dataset[U]]) : Dataset[U]`

- 

- `collectAsList算子： def collectAsList() : List[T]`

- 

- `takeAsList算子： def takeAsList(n : Int) : List[T] `

- 

- `repartitionByRange算子：def repartitionByRange(numPartitions : Int, partitionExprs : Column*) : Dataset[T]`

- 

- `toJSON算子：def toJSON : Dataset[String] `

- 

- `createOrReplaceTempView算子：def createOrReplaceTempView(viewName : String) : Unit`

  



- 

- ` cube算子：def cube(col1 : String, cols : String*) : RelationalGroupedDataset`

- 

- `glom算子`

- 

- `subtrat算子`

- 

- `mapPartitions算子:def mapPartitions[U](func : Function1[scala.Iterator[T], scala.Iterator[U]]) : Dataset[U]`

- `mapPartitionWithIndex算子`

- `zip算子`

- `zipPartitions算子`

- `zipWithIndex算子`

- `join算子`

- 

- `mapValues算子`

  - key不变，只对值操作，适用于PairRDD

- > 

- `reduceByKey算子`

- `groupByKey算子`

- `sortByKey算子`

- `combineByKey算子`

- `foldByKey算子`

- `flatMapValues算子`

### RDD&DataSet&DataFrame共有算子：

- `distinct算子： def distinct() : RDD[T]`

- `distinct(x)`

  > x的数量为因子，去重后数组里的元素会去%因子，将其分成对应数量的分区，

- `filter算子：def filter(func : Function1[T, Boolean]) : Dataset[T]`



- `map算子：def map[U](func : Function1[T, U]): Dataset[U]`、



- `flatmap算子：def flatMap[U](func : Function1[T, TraversableOnce[U]]) : Dataset[U]`

filter
map
flatmap
mappartitions
foreach
foreachpartitions
distinct
coalesce
sample
randomSplit
groupby
collect
reduce
repartition
checkpoint
count
first
take
union

#### Actions（non-lazy）：动作算子

##### 常用动作算子：

- `first算子`
- `collect算子`
- `take算子`
- `reduce算子`
- `saveAsTextFile算子`
- `saveAsSequenceFile算子`
- `countByKey算子`
- `foreach算子`
- `saveAsObjectFile算子`

`sort算子`

`orderby算子`

`alias算子`

`select算子`

`rollup算子`

`cube算子`

`agg算子`

`intersect算子`

`union算子`

`randomSplit`

`except算子`

`apply算子`

`drop算子`

`repartition算子`

`persist算子`

`cache算子`

`storagelevel算子`

`unpersist算子`

`toJavaRDD算子`

`hint算子`

`colRegex算子`

`na算子`

`stat算子`

`schema算子`

`dtypes算子`

`isStreaming算子`

`checkpoint算子`



`na.fill(value)`