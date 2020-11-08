## RDD算子

### map



### mapPartitions

#### 

```scala

  def toDF(colNames : scala.Predef.String*) : org.apache.spark.sql.DataFrame = { /* compiled code */ }
  def schema : org.apache.spark.sql.types.StructType = { /* compiled code */ }
  def printSchema() : scala.Unit = { /* compiled code */ }
  def explain(extended : scala.Boolean) : scala.Unit = { /* compiled code */ }
  def explain() : scala.Unit = { /* compiled code */ }
  def dtypes : scala.Array[scala.Tuple2[scala.Predef.String, scala.Predef.String]] = { /* compiled code */ }
  def columns : scala.Array[scala.Predef.String] = { /* compiled code */ }
  def isLocal : scala.Boolean = { /* compiled code */ }
  @org.apache.spark.annotation.InterfaceStability.Evolving
  def isStreaming : scala.Boolean = { /* compiled code */ }
  @org.apache.spark.annotation.InterfaceStability.Evolving
  @org.apache.spark.annotation.Experimental

  @org.apache.spark.annotation.InterfaceStability.Evolving
  @org.apache.spark.annotation.Experimental
  def localCheckpoint() : org.apache.spark.sql.Dataset[T] = { /* compiled code */ }
  @org.apache.spark.annotation.InterfaceStability.Evolving
  @org.apache.spark.annotation.Experimental
  def localCheckpoint(eager : scala.Boolean) : org.apache.spark.sql.Dataset[T] = { /* compiled code */ }
  @org.apache.spark.annotation.InterfaceStability.Evolving
  def withWatermark(eventTime : scala.Predef.String, delayThreshold : scala.Predef.String) : org.apache.spark.sql.Dataset[T] = { /* compiled code */ }
  def show(numRows : scala.Int) : scala.Unit = { /* compiled code */ }
  def show() : scala.Unit = { /* compiled code */ }
  def show(truncate : scala.Boolean) : scala.Unit = { /* compiled code */ }
  def show(numRows : scala.Int, truncate : scala.Boolean) : scala.Unit = { /* compiled code */ }
  def show(numRows : scala.Int, truncate : scala.Int) : scala.Unit = { /* compiled code */ }
  def show(numRows : scala.Int, truncate : scala.Int, vertical : scala.Boolean) : scala.Unit = { /* compiled code */ }
  def na : org.apache.spark.sql.DataFrameNaFunctions = { /* compiled code */ }
  def stat : org.apache.spark.sql.DataFrameStatFunctions = { /* compiled code */ }




  def select(cols : org.apache.spark.sql.Column*) : org.apache.spark.sql.DataFrame = { /* compiled code */ }
  @scala.annotation.varargs
  def select(col : scala.Predef.String, cols : scala.Predef.String*) : org.apache.spark.sql.DataFrame = { /* compiled code */ }
  @scala.annotation.varargs
  def selectExpr(exprs : scala.Predef.String*) : org.apache.spark.sql.DataFrame = { /* compiled code */ }
  @org.apache.spark.annotation.InterfaceStability.Evolving
  @org.apache.spark.annotation.Experimental
  def select[U1](c1 : org.apache.spark.sql.TypedColumn[T, U1]) : org.apache.spark.sql.Dataset[U1] = { /* compiled code */ }
  protected def selectUntyped(columns : org.apache.spark.sql.TypedColumn[_, _]*) : org.apache.spark.sql.Dataset[_] = { /* compiled code */ }
  @org.apache.spark.annotation.InterfaceStability.Evolving
  @org.apache.spark.annotation.Experimental
  def select[U1, U2](c1 : org.apache.spark.sql.TypedColumn[T, U1], c2 : org.apache.spark.sql.TypedColumn[T, U2]) : org.apache.spark.sql.Dataset[scala.Tuple2[U1, U2]] = { /* compiled code */ }
  @org.apache.spark.annotation.InterfaceStability.Evolving
  @org.apache.spark.annotation.Experimental
  def select[U1, U2, U3](c1 : org.apache.spark.sql.TypedColumn[T, U1], c2 : org.apache.spark.sql.TypedColumn[T, U2], c3 : org.apache.spark.sql.TypedColumn[T, U3]) : org.apache.spark.sql.Dataset[scala.Tuple3[U1, U2, U3]] = { /* compiled code */ }
  @org.apache.spark.annotation.InterfaceStability.Evolving
  @org.apache.spark.annotation.Experimental
  def select[U1, U2, U3, U4](c1 : org.apache.spark.sql.TypedColumn[T, U1], c2 : org.apache.spark.sql.TypedColumn[T, U2], c3 : org.apache.spark.sql.TypedColumn[T, U3], c4 : org.apache.spark.sql.TypedColumn[T, U4]) : org.apache.spark.sql.Dataset[scala.Tuple4[U1, U2, U3, U4]] = { /* compiled code */ }
  @org.apache.spark.annotation.InterfaceStability.Evolving
  @org.apache.spark.annotation.Experimental
  def select[U1, U2, U3, U4, U5](c1 : org.apache.spark.sql.TypedColumn[T, U1], c2 : org.apache.spark.sql.TypedColumn[T, U2], c3 : org.apache.spark.sql.TypedColumn[T, U3], c4 : org.apache.spark.sql.TypedColumn[T, U4], c5 : org.apache.spark.sql.TypedColumn[T, U5]) : org.apache.spark.sql.Dataset[scala.Tuple5[U1, U2, U3, U4, U5]] = { /* compiled code */ }

  def where(condition : org.apache.spark.sql.Column) : org.apache.spark.sql.Dataset[T] = { /* compiled code */ }
  def where(conditionExpr : scala.Predef.String) : org.apache.spark.sql.Dataset[T] = { /* compiled code */ }
  @scala.annotation.varargs
 
  @scala.annotation.varargs
  def rollup(cols : org.apache.spark.sql.Column*) : org.apache.spark.sql.RelationalGroupedDataset = { /* compiled code */ }
  @scala.annotation.varargs
  def cube(cols : org.apache.spark.sql.Column*) : org.apache.spark.sql.RelationalGroupedDataset = { /* compiled code */ }
  @scala.annotation.varargs
 
 
  def groupByKey[K](func : scala.Function1[T, K])(implicit evidence$3 : org.apache.spark.sql.Encoder[K]) : org.apache.spark.sql.KeyValueGroupedDataset[K, T] = { /* compiled code */ }
  @org.apache.spark.annotation.InterfaceStability.Evolving
  @org.apache.spark.annotation.Experimental
  def groupByKey[K](func : org.apache.spark.api.java.function.MapFunction[T, K], encoder : org.apache.spark.sql.Encoder[K]) : org.apache.spark.sql.KeyValueGroupedDataset[K, T] = { /* compiled code */ }
  @scala.annotation.varargs

  def agg(aggExpr : scala.Tuple2[scala.Predef.String, scala.Predef.String], aggExprs : scala.Tuple2[scala.Predef.String, scala.Predef.String]*) : org.apache.spark.sql.DataFrame = { /* compiled code */ }
  def agg(exprs : scala.Predef.Map[scala.Predef.String, scala.Predef.String]) : org.apache.spark.sql.DataFrame = { /* compiled code */ }
  def agg(exprs : java.util.Map[scala.Predef.String, scala.Predef.String]) : org.apache.spark.sql.DataFrame = { /* compiled code */ }
  @scala.annotation.varargs
  def agg(expr : org.apache.spark.sql.Column, exprs : org.apache.spark.sql.Column*) : org.apache.spark.sql.DataFrame = { /* compiled code */ }
  def limit(n : scala.Int) : org.apache.spark.sql.Dataset[T] = { /* compiled code */ }
  @scala.deprecated("use union()", "2.0.0")

  def except(other : org.apache.spark.sql.Dataset[T]) : org.apache.spark.sql.Dataset[T] = { /* compiled code */ }

  def randomSplitAsList(weights : scala.Array[scala.Double], seed : scala.Long) : java.util.List[org.apache.spark.sql.Dataset[T]] = { /* compiled code */ }

  @scala.deprecated("use flatMap() or select() with functions.explode() instead", "2.0.0")
  def explode[A, B](inputColumn : scala.Predef.String, outputColumn : scala.Predef.String)(f : scala.Function1[A, scala.TraversableOnce[B]])(implicit evidence$5 : scala.reflect.runtime.universe.TypeTag[B]) : org.apache.spark.sql.DataFrame = { /* compiled code */ }
  def withColumn(colName : scala.Predef.String, col : org.apache.spark.sql.Column) : org.apache.spark.sql.DataFrame = { /* compiled code */ }
  private[spark] def withColumns(colNames : scala.Seq[scala.Predef.String], cols : scala.Seq[org.apache.spark.sql.Column]) : org.apache.spark.sql.DataFrame = { /* compiled code */ }
  private[spark] def withColumns(colNames : scala.Seq[scala.Predef.String], cols : scala.Seq[org.apache.spark.sql.Column], metadata : scala.Seq[org.apache.spark.sql.types.Metadata]) : org.apache.spark.sql.DataFrame = { /* compiled code */ }
  private[spark] def withColumn(colName : scala.Predef.String, col : org.apache.spark.sql.Column, metadata : org.apache.spark.sql.types.Metadata) : org.apache.spark.sql.DataFrame = { /* compiled code */ }
  def withColumnRenamed(existingName : scala.Predef.String, newName : scala.Predef.String) : org.apache.spark.sql.DataFrame = { /* compiled code */ }
  def drop(colName : scala.Predef.String) : org.apache.spark.sql.DataFrame = { /* compiled code */ }
  @scala.annotation.varargs
  def drop(colNames : scala.Predef.String*) : org.apache.spark.sql.DataFrame = { /* compiled code */ }
  def drop(col : org.apache.spark.sql.Column) : org.apache.spark.sql.DataFrame = { /* compiled code */ }
  def dropDuplicates() : org.apache.spark.sql.Dataset[T] = { /* compiled code */ }
  def dropDuplicates(colNames : scala.Seq[scala.Predef.String]) : org.apache.spark.sql.Dataset[T] = { /* compiled code */ }
  def dropDuplicates(colNames : scala.Array[scala.Predef.String]) : org.apache.spark.sql.Dataset[T] = { /* compiled code */ }
  @scala.annotation.varargs
  def dropDuplicates(col1 : scala.Predef.String, cols : scala.Predef.String*) : org.apache.spark.sql.Dataset[T] = { /* compiled code */ }
  @scala.annotation.varargs
  def describe(cols : scala.Predef.String*) : org.apache.spark.sql.DataFrame = { /* compiled code */ }
  @scala.annotation.varargs
  def summary(statistics : scala.Predef.String*) : org.apache.spark.sql.DataFrame = { /* compiled code */ }
  def head(n : scala.Int) : scala.Array[T] = { /* compiled code */ }
  def head() : T = { /* compiled code */ }

  def transform[U](t : scala.Function1[org.apache.spark.sql.Dataset[T], org.apache.spark.sql.Dataset[U]]) : org.apache.spark.sql.Dataset[U] = { /* compiled code */ }
  @org.apache.spark.annotation.InterfaceStability.Evolving

  private[sql] def mapPartitionsInR(func : scala.Array[scala.Byte], packageNames : scala.Array[scala.Byte], broadcastVars : scala.Array[org.apache.spark.broadcast.Broadcast[java.lang.Object]], schema : org.apache.spark.sql.types.StructType) : org.apache.spark.sql.DataFrame = { /* compiled code */ }



  def takeAsList(n : scala.Int) : java.util.List[T] = { /* compiled code */ }

  def collectAsList() : java.util.List[T] = { /* compiled code */ }
  def toLocalIterator() : java.util.Iterator[T] = { /* compiled code */ }


  @scala.annotation.varargs
  def repartitionByRange(numPartitions : scala.Int, partitionExprs : org.apache.spark.sql.Column*) : org.apache.spark.sql.Dataset[T] = { /* compiled code */ }
  @scala.annotation.varargs
  def repartitionByRange(partitionExprs : org.apache.spark.sql.Column*) : org.apache.spark.sql.Dataset[T] = { /* compiled code */ }

  def persist() : Dataset.this.type = { /* compiled code */ }
  def cache() : Dataset.this.type = { /* compiled code */ }
  def persist(newLevel : org.apache.spark.storage.StorageLevel) : Dataset.this.type = { /* compiled code */ }
  def storageLevel : org.apache.spark.storage.StorageLevel = { /* compiled code */ }
  def unpersist(blocking : scala.Boolean) : Dataset.this.type = { /* compiled code */ }
  def unpersist() : Dataset.this.type = { /* compiled code */ }
  lazy val rdd : org.apache.spark.rdd.RDD[T] = { /* compiled code */ }
  def toJavaRDD : org.apache.spark.api.java.JavaRDD[T] = { /* compiled code */ }
  def javaRDD : org.apache.spark.api.java.JavaRDD[T] = { /* compiled code */ }
  @scala.deprecated("Use createOrReplaceTempView(viewName) instead.", "2.0.0")
  def registerTempTable(tableName : scala.Predef.String) : scala.Unit = { /* compiled code */ }
  @scala.throws[org.apache.spark.sql.AnalysisException]
  def createTempView(viewName : scala.Predef.String) : scala.Unit = { /* compiled code */ }
  def createOrReplaceTempView(viewName : scala.Predef.String) : scala.Unit = { /* compiled code */ }
  @scala.throws[org.apache.spark.sql.AnalysisException]
  def createGlobalTempView(viewName : scala.Predef.String) : scala.Unit = { /* compiled code */ }
  def createOrReplaceGlobalTempView(viewName : scala.Predef.String) : scala.Unit = { /* compiled code */ }
  def write : org.apache.spark.sql.DataFrameWriter[T] = { /* compiled code */ }
  @org.apache.spark.annotation.InterfaceStability.Evolving
  def writeStream : org.apache.spark.sql.streaming.DataStreamWriter[T] = { /* compiled code */ }
  def toJSON : org.apache.spark.sql.Dataset[scala.Predef.String] = { /* compiled code */ }
  def inputFiles : scala.Array[scala.Predef.String] = { /* compiled code */ }
  private[sql] def javaToPython : org.apache.spark.api.java.JavaRDD[scala.Array[scala.Byte]] = { /* compiled code */ }
  private[sql] def collectToPython() : scala.Array[scala.Any] = { /* compiled code */ }
  private[sql] def collectAsArrowToPython() : scala.Array[scala.Any] = { /* compiled code */ }
  private[sql] def toPythonIterator() : scala.Array[scala.Any] = { /* compiled code */ }
  private[sql] def toArrowPayload(plan : org.apache.spark.sql.execution.SparkPlan) : org.apache.spark.rdd.RDD[org.apache.spark.sql.execution.arrow.ArrowPayload] = { /* compiled code */ }
  private[sql] def toArrowPayload : org.apache.spark.rdd.RDD[org.apache.spark.sql.execution.arrow.ArrowPayload] = { /* compiled code */ }
}
private[sql] object Dataset extends scala.AnyRef with scala.Serializable {
  def apply[T](sparkSession : org.apache.spark.sql.SparkSession, logicalPlan : org.apache.spark.sql.catalyst.plans.logical.LogicalPlan)(implicit evidence$1 : org.apache.spark.sql.Encoder[T]) : org.apache.spark.sql.Dataset[T] = { /* compiled code */ }
  def ofRows(sparkSession : org.apache.spark.sql.SparkSession, logicalPlan : org.apache.spark.sql.catalyst.plans.logical.LogicalPlan) : org.apache.spark.sql.DataFrame = { /* compiled code */ }
}

```

#### DataSet

> 特定领域对象中的强类型集合，它可以使用函数并行的进行转换操作

#### DataFrame

> 最常见的结构化API，包含行和列的数据表，特殊的DataSet

模式（schema）：说明这些列和列类型的一些规则

分布式dataFrame，这种数据集是 **以RDD为基础的**，其被组织成指定的列，**类似于关系数据库的二维表格**

### RDD独有算子：

#### 简单转换算子：

- > 

  

  




- `sortby算子：def sortBy[K](f : Function1[T, K], ascending : Boolean`



- `randomSplit算子：def randomSplit(weights : Array[Double], seed : Long = { /* compiled code */ }) : Array[RDD[T]] `

#### 聚合转换算子：

- 

```scala





  private[spark] def randomSampleWithRange(lb : scala.Double, ub : scala.Double, seed : scala.Long) : org.apache.spark.rdd.RDD[T] = { /* compiled code */ }
  def takeSample(withReplacement : scala.Boolean, num : scala.Int, seed : scala.Long = { /* compiled code */ }) : scala.Array[T] = { /* compiled code */ }
  def union(other : org.apache.spark.rdd.RDD[T]) : org.apache.spark.rdd.RDD[T] = { /* compiled code */ }
  def ++(other : org.apache.spark.rdd.RDD[T]) : org.apache.spark.rdd.RDD[T] = { /* compiled code */ }
  def sortBy[K](f : scala.Function1[T, K], ascending : scala.Boolean = { /* compiled code */ }, numPartitions : scala.Int = { /* compiled code */ })(implicit ord : scala.Ordering[K], ctag : scala.reflect.ClassTag[K]) : org.apache.spark.rdd.RDD[T] = { /* compiled code */ }
  def intersection(other : org.apache.spark.rdd.RDD[T]) : org.apache.spark.rdd.RDD[T] = { /* compiled code */ }
  def intersection(other : org.apache.spark.rdd.RDD[T], partitioner : org.apache.spark.Partitioner)(implicit ord : scala.Ordering[T] = { /* compiled code */ }) : org.apache.spark.rdd.RDD[T] = { /* compiled code */ }
  def intersection(other : org.apache.spark.rdd.RDD[T], numPartitions : scala.Int) : org.apache.spark.rdd.RDD[T] = { /* compiled code */ }
  def glom() : org.apache.spark.rdd.RDD[scala.Array[T]] = { /* compiled code */ }
  def cartesian[U](other : org.apache.spark.rdd.RDD[U])(implicit evidence$5 : scala.reflect.ClassTag[U]) : org.apache.spark.rdd.RDD[scala.Tuple2[T, U]] = { /* compiled code */ }

  def pipe(command : scala.Predef.String) : org.apache.spark.rdd.RDD[scala.Predef.String] = { /* compiled code */ }
  def pipe(command : scala.Predef.String, env : scala.collection.Map[scala.Predef.String, scala.Predef.String]) : org.apache.spark.rdd.RDD[scala.Predef.String] = { /* compiled code */ }
  def pipe(command : scala.Seq[scala.Predef.String], env : scala.collection.Map[scala.Predef.String, scala.Predef.String] = { /* compiled code */ }, printPipeContext : scala.Function1[scala.Function1[scala.Predef.String, scala.Unit], scala.Unit] = { /* compiled code */ }, printRDDElement : scala.Function2[T, scala.Function1[scala.Predef.String, scala.Unit], scala.Unit] = { /* compiled code */ }, separateWorkingDir : scala.Boolean = { /* compiled code */ }, bufferSize : scala.Int = { /* compiled code */ }, encoding : scala.Predef.String = { /* compiled code */ }) : org.apache.spark.rdd.RDD[scala.Predef.String] = { /* compiled code */ }

  private[spark] def mapPartitionsWithIndexInternal[U](f : scala.Function2[scala.Int, scala.Iterator[T], scala.Iterator[U]], preservesPartitioning : scala.Boolean = { /* compiled code */ }, isOrderSensitive : scala.Boolean = { /* compiled code */ })(implicit evidence$7 : scala.reflect.ClassTag[U]) : org.apache.spark.rdd.RDD[U] = { /* compiled code */ }
  private[spark] def mapPartitionsInternal[U](f : scala.Function1[scala.Iterator[T], scala.Iterator[U]], preservesPartitioning : scala.Boolean = { /* compiled code */ })(implicit evidence$8 : scala.reflect.ClassTag[U]) : org.apache.spark.rdd.RDD[U] = { /* compiled code */ }
  def mapPartitionsWithIndex[U](f : scala.Function2[scala.Int, scala.Iterator[T], scala.Iterator[U]], preservesPartitioning : scala.Boolean = { /* compiled code */ })(implicit evidence$9 : scala.reflect.ClassTag[U]) : org.apache.spark.rdd.RDD[U] = { /* compiled code */ }
  def zip[U](other : org.apache.spark.rdd.RDD[U])(implicit evidence$10 : scala.reflect.ClassTag[U]) : org.apache.spark.rdd.RDD[scala.Tuple2[T, U]] = { /* compiled code */ }
  def zipPartitions[B, V](rdd2 : org.apache.spark.rdd.RDD[B], preservesPartitioning : scala.Boolean)(f : scala.Function2[scala.Iterator[T], scala.Iterator[B], scala.Iterator[V]])(implicit evidence$11 : scala.reflect.ClassTag[B], evidence$12 : scala.reflect.ClassTag[V]) : org.apache.spark.rdd.RDD[V] = { /* compiled code */ }
  def zipPartitions[B, V](rdd2 : org.apache.spark.rdd.RDD[B])(f : scala.Function2[scala.Iterator[T], scala.Iterator[B], scala.Iterator[V]])(implicit evidence$13 : scala.reflect.ClassTag[B], evidence$14 : scala.reflect.ClassTag[V]) : org.apache.spark.rdd.RDD[V] = { /* compiled code */ }
  def zipPartitions[B, C, V](rdd2 : org.apache.spark.rdd.RDD[B], rdd3 : org.apache.spark.rdd.RDD[C], preservesPartitioning : scala.Boolean)(f : scala.Function3[scala.Iterator[T], scala.Iterator[B], scala.Iterator[C], scala.Iterator[V]])(implicit evidence$15 : scala.reflect.ClassTag[B], evidence$16 : scala.reflect.ClassTag[C], evidence$17 : scala.reflect.ClassTag[V]) : org.apache.spark.rdd.RDD[V] = { /* compiled code */ }
  def zipPartitions[B, C, V](rdd2 : org.apache.spark.rdd.RDD[B], rdd3 : org.apache.spark.rdd.RDD[C])(f : scala.Function3[scala.Iterator[T], scala.Iterator[B], scala.Iterator[C], scala.Iterator[V]])(implicit evidence$18 : scala.reflect.ClassTag[B], evidence$19 : scala.reflect.ClassTag[C], evidence$20 : scala.reflect.ClassTag[V]) : org.apache.spark.rdd.RDD[V] = { /* compiled code */ }
  def zipPartitions[B, C, D, V](rdd2 : org.apache.spark.rdd.RDD[B], rdd3 : org.apache.spark.rdd.RDD[C], rdd4 : org.apache.spark.rdd.RDD[D], preservesPartitioning : scala.Boolean)(f : scala.Function4[scala.Iterator[T], scala.Iterator[B], scala.Iterator[C], scala.Iterator[D], scala.Iterator[V]])(implicit evidence$21 : scala.reflect.ClassTag[B], evidence$22 : scala.reflect.ClassTag[C], evidence$23 : scala.reflect.ClassTag[D], evidence$24 : scala.reflect.ClassTag[V]) : org.apache.spark.rdd.RDD[V] = { /* compiled code */ }
  def zipPartitions[B, C, D, V](rdd2 : org.apache.spark.rdd.RDD[B], rdd3 : org.apache.spark.rdd.RDD[C], rdd4 : org.apache.spark.rdd.RDD[D])(f : scala.Function4[scala.Iterator[T], scala.Iterator[B], scala.Iterator[C], scala.Iterator[D], scala.Iterator[V]])(implicit evidence$25 : scala.reflect.ClassTag[B], evidence$26 : scala.reflect.ClassTag[C], evidence$27 : scala.reflect.ClassTag[D], evidence$28 : scala.reflect.ClassTag[V]) : org.apache.spark.rdd.RDD[V] = { /* compiled code */ }


  def toLocalIterator : scala.Iterator[T] = { /* compiled code */ }

  def subtract(other : org.apache.spark.rdd.RDD[T]) : org.apache.spark.rdd.RDD[T] = { /* compiled code */ }
  def subtract(other : org.apache.spark.rdd.RDD[T], numPartitions : scala.Int) : org.apache.spark.rdd.RDD[T] = { /* compiled code */ }
  def subtract(other : org.apache.spark.rdd.RDD[T], p : org.apache.spark.Partitioner)(implicit ord : scala.Ordering[T] = { /* compiled code */ }) : org.apache.spark.rdd.RDD[T] = { /* compiled code */ }

  def treeReduce(f : scala.Function2[T, T, T], depth : scala.Int = { /* compiled code */ }) : T = { /* compiled code */ }
  def fold(zeroValue : T)(op : scala.Function2[T, T, T]) : T = { /* compiled code */ }
  def aggregate[U](zeroValue : U)(seqOp : scala.Function2[U, T, U], combOp : scala.Function2[U, U, U])(implicit evidence$30 : scala.reflect.ClassTag[U]) : U = { /* compiled code */ }
  def treeAggregate[U](zeroValue : U)(seqOp : scala.Function2[U, T, U], combOp : scala.Function2[U, U, U], depth : scala.Int = { /* compiled code */ })(implicit evidence$31 : scala.reflect.ClassTag[U]) : U = { /* compiled code */ }

  def countApprox(timeout : scala.Long, confidence : scala.Double = { /* compiled code */ }) : org.apache.spark.partial.PartialResult[org.apache.spark.partial.BoundedDouble] = { /* compiled code */ }
  def countByValue()(implicit ord : scala.Ordering[T] = { /* compiled code */ }) : scala.collection.Map[T, scala.Long] = { /* compiled code */ }
  def countByValueApprox(timeout : scala.Long, confidence : scala.Double = { /* compiled code */ })(implicit ord : scala.Ordering[T] = { /* compiled code */ }) : org.apache.spark.partial.PartialResult[scala.collection.Map[T, org.apache.spark.partial.BoundedDouble]] = { /* compiled code */ }
  def countApproxDistinct(p : scala.Int, sp : scala.Int) : scala.Long = { /* compiled code */ }
  def countApproxDistinct(relativeSD : scala.Double = { /* compiled code */ }) : scala.Long = { /* compiled code */ }
  def zipWithIndex() : org.apache.spark.rdd.RDD[scala.Tuple2[T, scala.Long]] = { /* compiled code */ }
  def zipWithUniqueId() : org.apache.spark.rdd.RDD[scala.Tuple2[T, scala.Long]] = { /* compiled code */ }


  def top(num : scala.Int)(implicit ord : scala.Ordering[T]) : scala.Array[T] = { /* compiled code */ }
  def takeOrdered(num : scala.Int)(implicit ord : scala.Ordering[T]) : scala.Array[T] = { /* compiled code */ }
  def max()(implicit ord : scala.Ordering[T]) : T = { /* compiled code */ }
  def min()(implicit ord : scala.Ordering[T]) : T = { /* compiled code */ }
  def isEmpty() : scala.Boolean = { /* compiled code */ }
  def saveAsTextFile(path : scala.Predef.String) : scala.Unit = { /* compiled code */ }
  def saveAsTextFile(path : scala.Predef.String, codec : scala.Predef.Class[_ <: org.apache.hadoop.io.compress.CompressionCodec]) : scala.Unit = { /* compiled code */ }
  def saveAsObjectFile(path : scala.Predef.String) : scala.Unit = { /* compiled code */ }
  def keyBy[K](f : scala.Function1[T, K]) : org.apache.spark.rdd.RDD[scala.Tuple2[K, T]] = { /* compiled code */ }
  private[spark] def collectPartitions() : scala.Array[scala.Array[T]] = { /* compiled code */ }

  def localCheckpoint() : RDD.this.type = { /* compiled code */ }
  def isCheckpointed : scala.Boolean = { /* compiled code */ }
  private[spark] def isCheckpointedAndMaterialized : scala.Boolean = { /* compiled code */ }
  private[rdd] def isLocallyCheckpointed : scala.Boolean = { /* compiled code */ }
  private[rdd] def isReliablyCheckpointed : scala.Boolean = { /* compiled code */ }
  def getCheckpointFile : scala.Option[scala.Predef.String] = { /* compiled code */ }
  @scala.transient
  private[spark] val creationSite : org.apache.spark.util.CallSite = { /* compiled code */ }
  @scala.transient
  private[spark] val scope : scala.Option[org.apache.spark.rdd.RDDOperationScope] = { /* compiled code */ }
  private[spark] def getCreationSite : scala.Predef.String = { /* compiled code */ }
  private[spark] def elementClassTag : scala.reflect.ClassTag[T] = { /* compiled code */ }
  private[spark] var checkpointData : scala.Option[org.apache.spark.rdd.RDDCheckpointData[T]] = { /* compiled code */ }
  protected[spark] def firstParent[U](implicit evidence$32 : scala.reflect.ClassTag[U]) : org.apache.spark.rdd.RDD[U] = { /* compiled code */ }
  protected[spark] def parent[U](j : scala.Int)(implicit evidence$33 : scala.reflect.ClassTag[U]) : org.apache.spark.rdd.RDD[U] = { /* compiled code */ }
  def context : org.apache.spark.SparkContext = { /* compiled code */ }
  private[spark] def retag(cls : scala.Predef.Class[T]) : org.apache.spark.rdd.RDD[T] = { /* compiled code */ }
  private[spark] def retag(implicit classTag : scala.reflect.ClassTag[T]) : org.apache.spark.rdd.RDD[T] = { /* compiled code */ }
  private[spark] def doCheckpoint() : scala.Unit = { /* compiled code */ }
  private[spark] def markCheckpointed() : scala.Unit = { /* compiled code */ }
  protected def clearDependencies() : scala.Unit = { /* compiled code */ }
  def toDebugString : scala.Predef.String = { /* compiled code */ }
  override def toString() : scala.Predef.String = { /* compiled code */ }
  def toJavaRDD() : org.apache.spark.api.java.JavaRDD[T] = { /* compiled code */ }
  private[spark] final lazy val outputDeterministicLevel : org.apache.spark.rdd.DeterministicLevel.Value = { /* compiled code */ }
  @org.apache.spark.annotation.DeveloperApi
  protected def getOutputDeterministicLevel : org.apache.spark.rdd.DeterministicLevel.Value = { /* compiled code */ }
}
object RDD extends scala.AnyRef with scala.Serializable {
  private[spark] val CHECKPOINT_ALL_MARKED_ANCESTORS : java.lang.String = { /* compiled code */ }
  implicit def rddToPairRDDFunctions[K, V](rdd : org.apache.spark.rdd.RDD[scala.Tuple2[K, V]])(implicit kt : scala.reflect.ClassTag[K], vt : scala.reflect.ClassTag[V], ord : scala.Ordering[K] = { /* compiled code */ }) : org.apache.spark.rdd.PairRDDFunctions[K, V] = { /* compiled code */ }
  implicit def rddToAsyncRDDActions[T](rdd : org.apache.spark.rdd.RDD[T])(implicit evidence$34 : scala.reflect.ClassTag[T]) : org.apache.spark.rdd.AsyncRDDActions[T] = { /* compiled code */ }
  implicit def rddToSequenceFileRDDFunctions[K, V](rdd : org.apache.spark.rdd.RDD[scala.Tuple2[K, V]])(implicit kt : scala.reflect.ClassTag[K], vt : scala.reflect.ClassTag[V], keyWritableFactory : org.apache.spark.WritableFactory[K], valueWritableFactory : org.apache.spark.WritableFactory[V]) : org.apache.spark.rdd.SequenceFileRDDFunctions[K, V] = { /* compiled code */ }
  implicit def rddToOrderedRDDFunctions[K, V](rdd : org.apache.spark.rdd.RDD[scala.Tuple2[K, V]])(implicit evidence$35 : scala.Ordering[K], evidence$36 : scala.reflect.ClassTag[K], evidence$37 : scala.reflect.ClassTag[V]) : org.apache.spark.rdd.OrderedRDDFunctions[K, V, scala.Tuple2[K, V]] = { /* compiled code */ }
  implicit def doubleRDDToDoubleRDDFunctions(rdd : org.apache.spark.rdd.RDD[scala.Double]) : org.apache.spark.rdd.DoubleRDDFunctions = { /* compiled code */ }
  implicit def numericRDDToDoubleRDDFunctions[T](rdd : org.apache.spark.rdd.RDD[T])(implicit num : scala.Numeric[T]) : org.apache.spark.rdd.DoubleRDDFunctions = { /* compiled code */ }
}

```

### RDD操作：

#### Transformation（lazy）：转换算子

- 对于转换操作，RDD的所有转换都不会直接计算结果
  - 仅记录作用于RDD上的操作



### DataSet算子：

### DataFrame&DataSet算子：

##### 常用转换算子：

- `toDF算子: def toDF() : DataFrame`

  > 转换成dataFrame类型

- `isStreaming算子：def isStreaming : scala.Boolean`

  > 判断是否是stream流

- `show算子： def show(numRows : Int, truncate : Boolean) : Unit`

  > 展示表格

- `as算子: def as(alias : String) : Dataset[T]`

  > 重命名列

- `alias算子: def as(alias : String) : Dataset[T]`

  >重命名列

- `na算子：def na : DataFrameNaFunctions`

  > functions包和DataFrameNaFunctions包下

  `ifnull`

  - 如果第一个值为空，则允许第二个值去取代他

  `nullif`

  - 如果两个值相等，则返回null，否则返回第二个值

  `nvl`

  - 如果第一个值为null，则返回第二个值，否则返回第一个值

  `nvl2`

  - 如果第一个不为null，返回第二个指定值，否则返回最后一个指定值

  > 上述4个在sql里有体现，dataframe是另外的API

  `drop`

  - 删除包含null的行

  ```SPARQL
  df.na.drop()
  df.na.drop("any") # 存在null就删除
  df.na.drop("all") # 全部为null才能删除
  df.na.drop("any",Seq("StockCode","InvoiceNo")) # 指定列删除
  ```

  `fill`

  - 用一组值填充一列或者多列

  ```SPARQL
  df.na.fill("value") # 将字符类型列的null值替换
  df.na.fill(5,Seq("store")) # 指定列替换null值
  ```

  `replace`

  - 将当前值替换掉某列的所有值

  ```scala
  df.na.replace("description",Map("" -> "UNKNOWN"))
  ```

  

- `stat算子：def stat : DataFrameStatFunctions`

  

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

  > 两个dataFrame进行笛卡尔积

- `joinWith算子： def joinWith[U](other : Dataset[U], condition : Column, joinType : String) :Dataset[Tuple2[T, U]] `--jointype可省略

  > 当满足你设定的条件时与另一张表的列进行某种连接

- `sortWithPartitions算子：`

  - `def sortWithinPartitions(sortCol : String, sortCols : String*) : Dataset[T]`

    > 类似hive的sort by，只在分区内排序，默认降序

  - ` def sortWithinPartitions(sortExprs : Column*) : Dataset[T]`

    > 按多个列只在分区内排序，默认降序

- `sort算子：`

  - `def sort(sortCol : String, sortCols :String*) : Dataset[T]`
  - 
  - ` def sort(sortExprs : Column*) : Dataset[T]` 

- 

- `order算子:`

  - ` def orderBy(sortCol : String, sortCols : String*) : Dataset[T]`
  - 按某个列排序，
  - ` def orderBy(sortExprs : Column*) : Dataset[T]` 
  - 

- 

- `apply算子：def apply(colName : String) : Column`

- 

- `colRegex算子：colRegex(colName : String) : Column`

  > 通过正则匹配的方式拿到对应列名的列值

- `col算子：def col(colName : String) : Column`

  > 取指定列名的列值

- `rollup算子： def rollup(col1 : String, cols : String*) : RelationalGroupedDataset`

- 

- `hint算子：def hint(name : String, parameters : Any*) : Dataset[T]`

  

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

  > 对两个DataFrame进行组合 去重

- `unionAll算子:def union(other : Dataset[T]) : Dataset[T]`

  > 对两个DataFrame进行组合 不去重

- `unionByName算子:def union(other : Dataset[T]) : Dataset[T]`

- 

- `intersect算子:def intersect(other : Dataset[T]) : Dataset[T]`

  > 计算出两个DataFrame中相同的记录.

- `except算子： def except(other : Dataset[T]) : Dataset[T]`

  > a.except(b)：a获取中有另一个b中没有的记录

- `explode算子：def explode[A, B](inputColumn : String, outputColumn : String)(f : Function1[A, TraversableOnce[B]]): DataFrame`

- 

- `withColumn算子：(colName : String, col : Column) : DataFrame`

  > 添加新列或将原先已经存在的列替换。

- `withColumnRenamed算子：def` `withColumnRenamed(existingName : String, newName : String) : DataFrame`

  > 修改原先存在列的列名

- `drop算子：`

  > 删除指定某列或某几列

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

  >获取第一行记录 | 获取前n行记录

- `transform算子： def transform[U](t : Function1[Dataset[T],Dataset[U]]) : Dataset[U]`

- 

- `collectAsList算子： def collectAsList() : List[T]`

- 

- `takeAsList算子： def takeAsList(n : Int) : List[T] `

  > 获取前n行数据，并以`List`的形式展现 

- `repartitionByRange算子：def repartitionByRange(numPartitions : Int, partitionExprs : Column*) : Dataset[T]`

- 

- `toJSON算子：def toJSON : Dataset[String] `

- 

- `createOrReplaceTempView算子：def createOrReplaceTempView(viewName : String) : Unit`

  



- 

- ` cube算子：def cube(col1 : String, cols : String*) : RelationalGroupedDataset`

- 

- `glom算子`

  > glom函数将每个分区形成一个数组，内部实现是返回的GlommedRDD

  ![image-20200731121424708](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200731121424708.png)

- `subtrat算子`

  > 该函数类似于intersection，但返回在RDD中出现，并且不在otherRDD中出现的元素，**不去重**。

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

  > 接收一个将Row转为别的类型的函数

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

返回Dataset，参数依次为，是否放回，抽取比例，随机种子randomSplit

将Dataset按比例大致分为结果Dataset，返回Array[Dataset]or list

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