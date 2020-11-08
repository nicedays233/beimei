## Spark GraphX：

![image-20200804185538779](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200804185538779.png)

### 一：图的概念：

- 图由**顶点集合（vertex）**及顶点间的**关系集合（边edge）** 组成的网状数据结构
  - 表示为二元组： Graph = (V, E)
  - 可以对事物之间的关系建模
- **应用场景：**
  - 在地图应用中寻找最短路径
  - 社交网络关系
  - 网页间超链接关系

#### 1.邻接矩阵—————稠密图的存储（存边多）

#### 2.邻接表　—————稀疏图的存储（存顶点多或者边少）

#### 3.十字链表—————邻接表的升级版

#### 4.邻接多重表————邻接矩阵的升级版

### 二：Spark GraphX 数据模型：

- GraphX是Spark提供分布式图计算API

### 三：GraphX特点：

- 基于内存实现了数据的复用与快速读取
- 通过弹性分布式属性图统一了图视图与表视图
- 与Spark Streaming，SparkSQL和SparkMLib等无缝衔接

### 四：GraphX核心抽象：

- 弹性分布式属性图（Resilient Distributed Property Graph）
  - 顶点和边都带属性的有向多重图
  - 一份物理存储，两种视图

> **对Graph视图的所有操作，最终都会转换成其关联的Table视图的RDD操作来完成**



### 五：Spark GraphX API：

- **Graph[VD,ED]**

- **VertexRDD[VD]**

- **EdgeRDD[ED]**

- **EdgeTriplet[VD,ED]**

- **Edge：样例类**

- **VertexId：long别名**


### 六：构建图的步骤：

- 构建点

```js
 // 建立所有的点, 第二个位置对象或者值通过hash值确定分区id的位置
    val vects: RDD[(VertexId, (String, String))] = sc.makeRDD(Seq((1L,("rxin","student")),(2L,("zs","prof")),(3L,("ll","pst"))))
```

- 构建边

```js
    // 建立所有的边
    val edges: RDD[Edge[String]] = sc.makeRDD(Seq(Edge(1L,2L,"ts"),Edge(2L,3L,"zd"),Edge(1L,3L,"col")))
```

- 构建图

```js
    // 建立图
    val graph: Graph[(String, String), String] = Graph(vects,edges)
```

> 我们得到的graph既可以使用GraphOps类和也可以使用Graph类
>
> 以下是图的结构与方法：

#### GraphOps类：

- **顶点数量**

- **边数量**

- **度、入度、出度**

#### GraphOps类源码：

```js
class GraphOps[VD, ED](graph : org.apache.spark.graphx.Graph[VD, ED])(implicit evidence$1 : scala.reflect.ClassTag[VD], evidence$2 : scala.reflect.ClassTag[ED]) extends scala.AnyRef with scala.Serializable {
  @scala.transient
  lazy val numEdges : scala.Long = { /* compiled code */ }
  @scala.transient
  lazy val numVertices : scala.Long = { /* compiled code */ }
  @scala.transient
  lazy val inDegrees : org.apache.spark.graphx.VertexRDD[scala.Int] = { /* compiled code */ }
  @scala.transient
  lazy val outDegrees : org.apache.spark.graphx.VertexRDD[scala.Int] = { /* compiled code */ }
  @scala.transient
  lazy val degrees : org.apache.spark.graphx.VertexRDD[scala.Int] = { /* compiled code */ }
 
```

#### Graph类：

- **所有顶点信息**

- **所有的边信息**

- **起点信息，终点完整信息，边权重**

#### Graph类源码：

```js
abstract class Graph[VD, ED] protected ()(implicit evidence$1 : scala.reflect.ClassTag[VD], evidence$2 : scala.reflect.ClassTag[ED]) extends scala.AnyRef with scala.Serializable {
  val vertices : org.apache.spark.graphx.VertexRDD[VD]
  val edges : org.apache.spark.graphx.EdgeRDD[ED]
  val triplets : org.apache.spark.rdd.RDD[org.apache.spark.graphx.EdgeTriplet[VD, ED]]

```

#### GraphOps方法：

```js
 def collectNeighborIds(edgeDirection : org.apache.spark.graphx.EdgeDirection) : org.apache.spark.graphx.VertexRDD[scala.Array[org.apache.spark.graphx.VertexId]] = { /* compiled code */ }
  def collectNeighbors(edgeDirection : org.apache.spark.graphx.EdgeDirection) : org.apache.spark.graphx.VertexRDD[scala.Array[scala.Tuple2[org.apache.spark.graphx.VertexId, VD]]] = { /* compiled code */ }
  def collectEdges(edgeDirection : org.apache.spark.graphx.EdgeDirection) : org.apache.spark.graphx.VertexRDD[scala.Array[org.apache.spark.graphx.Edge[ED]]] = { /* compiled code */ }
  def removeSelfEdges() : org.apache.spark.graphx.Graph[VD, ED] = { /* compiled code */ }
  def joinVertices[U](table : org.apache.spark.rdd.RDD[scala.Tuple2[org.apache.spark.graphx.VertexId, U]])(mapFunc : scala.Function3[org.apache.spark.graphx.VertexId, VD, U, VD])(implicit evidence$3 : scala.reflect.ClassTag[U]) : org.apache.spark.graphx.Graph[VD, ED] = { /* compiled code */ }
  def filter[VD2, ED2](preprocess : scala.Function1[org.apache.spark.graphx.Graph[VD, ED], org.apache.spark.graphx.Graph[VD2, ED2]], epred : scala.Function1[org.apache.spark.graphx.EdgeTriplet[VD2, ED2], scala.Boolean] = { /* compiled code */ }, vpred : scala.Function2[org.apache.spark.graphx.VertexId, VD2, scala.Boolean] = { /* compiled code */ })(implicit evidence$4 : scala.reflect.ClassTag[VD2], evidence$5 : scala.reflect.ClassTag[ED2]) : org.apache.spark.graphx.Graph[VD, ED] = { /* compiled code */ }
  def pickRandomVertex() : org.apache.spark.graphx.VertexId = { /* compiled code */ }
  def convertToCanonicalEdges(mergeFunc : scala.Function2[ED, ED, ED] = { /* compiled code */ }) : org.apache.spark.graphx.Graph[VD, ED] = { /* compiled code */ }
  def pregel[A](initialMsg : A, maxIterations : scala.Int = { /* compiled code */ }, activeDirection : org.apache.spark.graphx.EdgeDirection = { /* compiled code */ })(vprog : scala.Function3[org.apache.spark.graphx.VertexId, VD, A, VD], sendMsg : scala.Function1[org.apache.spark.graphx.EdgeTriplet[VD, ED], scala.Iterator[scala.Tuple2[org.apache.spark.graphx.VertexId, A]]], mergeMsg : scala.Function2[A, A, A])(implicit evidence$6 : scala.reflect.ClassTag[A]) : org.apache.spark.graphx.Graph[VD, ED] = { /* compiled code */ }
  def pageRank(tol : scala.Double, resetProb : scala.Double = { /* compiled code */ }) : org.apache.spark.graphx.Graph[scala.Double, scala.Double] = { /* compiled code */ }
  def personalizedPageRank(src : org.apache.spark.graphx.VertexId, tol : scala.Double, resetProb : scala.Double = { /* compiled code */ }) : org.apache.spark.graphx.Graph[scala.Double, scala.Double] = { /* compiled code */ }
  def staticParallelPersonalizedPageRank(sources : scala.Array[org.apache.spark.graphx.VertexId], numIter : scala.Int, resetProb : scala.Double = { /* compiled code */ }) : org.apache.spark.graphx.Graph[org.apache.spark.ml.linalg.Vector, scala.Double] = { /* compiled code */ }
  def staticPersonalizedPageRank(src : org.apache.spark.graphx.VertexId, numIter : scala.Int, resetProb : scala.Double = { /* compiled code */ }) : org.apache.spark.graphx.Graph[scala.Double, scala.Double] = { /* compiled code */ }
  def staticPageRank(numIter : scala.Int, resetProb : scala.Double = { /* compiled code */ }) : org.apache.spark.graphx.Graph[scala.Double, scala.Double] = { /* compiled code */ }
  def connectedComponents() : org.apache.spark.graphx.Graph[org.apache.spark.graphx.VertexId, ED] = { /* compiled code */ }
  def connectedComponents(maxIterations : scala.Int) : org.apache.spark.graphx.Graph[org.apache.spark.graphx.VertexId, ED] = { /* compiled code */ }
  def triangleCount() : org.apache.spark.graphx.Graph[scala.Int, ED] = { /* compiled code */ }
  def stronglyConnectedComponents(numIter : scala.Int) : org.apache.spark.graphx.Graph[org.apache.spark.graphx.VertexId, ED] = { /* compiled code */ }
}
```

---



#### Graph类方法：

```js
  def persist(newLevel : org.apache.spark.storage.StorageLevel = { /* compiled code */ }) : org.apache.spark.graphx.Graph[VD, ED]
  def cache() : org.apache.spark.graphx.Graph[VD, ED]
  def checkpoint() : scala.Unit
  def isCheckpointed : scala.Boolean
  def getCheckpointFiles : scala.Seq[scala.Predef.String]
  def unpersist(blocking : scala.Boolean = { /* compiled code */ }) : org.apache.spark.graphx.Graph[VD, ED]
  def unpersistVertices(blocking : scala.Boolean = { /* compiled code */ }) : org.apache.spark.graphx.Graph[VD, ED]
  def partitionBy(partitionStrategy : org.apache.spark.graphx.PartitionStrategy) : org.apache.spark.graphx.Graph[VD, ED]
  def partitionBy(partitionStrategy : org.apache.spark.graphx.PartitionStrategy, numPartitions : scala.Int) : org.apache.spark.graphx.Graph[VD, ED]
  def mapVertices[VD2](map : scala.Function2[org.apache.spark.graphx.VertexId, VD, VD2])(implicit evidence$3 : scala.reflect.ClassTag[VD2], eq : scala.Predef.=:=[VD, VD2] = { /* compiled code */ }) : org.apache.spark.graphx.Graph[VD2, ED]
  def mapEdges[ED2](map : scala.Function1[org.apache.spark.graphx.Edge[ED], ED2])(implicit evidence$4 : scala.reflect.ClassTag[ED2]) : org.apache.spark.graphx.Graph[VD, ED2] = { /* compiled code */ }
  def mapEdges[ED2](map : scala.Function2[org.apache.spark.graphx.PartitionID, scala.Iterator[org.apache.spark.graphx.Edge[ED]], scala.Iterator[ED2]])(implicit evidence$5 : scala.reflect.ClassTag[ED2]) : org.apache.spark.graphx.Graph[VD, ED2]
  def mapTriplets[ED2](map : scala.Function1[org.apache.spark.graphx.EdgeTriplet[VD, ED], ED2])(implicit evidence$6 : scala.reflect.ClassTag[ED2]) : org.apache.spark.graphx.Graph[VD, ED2] = { /* compiled code */ }
  def mapTriplets[ED2](map : scala.Function1[org.apache.spark.graphx.EdgeTriplet[VD, ED], ED2], tripletFields : org.apache.spark.graphx.TripletFields)(implicit evidence$7 : scala.reflect.ClassTag[ED2]) : org.apache.spark.graphx.Graph[VD, ED2] = { /* compiled code */ }
  def mapTriplets[ED2](map : scala.Function2[org.apache.spark.graphx.PartitionID, scala.Iterator[org.apache.spark.graphx.EdgeTriplet[VD, ED]], scala.Iterator[ED2]], tripletFields : org.apache.spark.graphx.TripletFields)(implicit evidence$8 : scala.reflect.ClassTag[ED2]) : org.apache.spark.graphx.Graph[VD, ED2]
  def reverse : org.apache.spark.graphx.Graph[VD, ED]
  def subgraph(epred : scala.Function1[org.apache.spark.graphx.EdgeTriplet[VD, ED], scala.Boolean] = { /* compiled code */ }, vpred : scala.Function2[org.apache.spark.graphx.VertexId, VD, scala.Boolean] = { /* compiled code */ }) : org.apache.spark.graphx.Graph[VD, ED]
  def mask[VD2, ED2](other : org.apache.spark.graphx.Graph[VD2, ED2])(implicit evidence$9 : scala.reflect.ClassTag[VD2], evidence$10 : scala.reflect.ClassTag[ED2]) : org.apache.spark.graphx.Graph[VD, ED]
  def groupEdges(merge : scala.Function2[ED, ED, ED]) : org.apache.spark.graphx.Graph[VD, ED]
  def aggregateMessages[A](sendMsg : scala.Function1[org.apache.spark.graphx.EdgeContext[VD, ED, A], scala.Unit], mergeMsg : scala.Function2[A, A, A], tripletFields : org.apache.spark.graphx.TripletFields = { /* compiled code */ })(implicit evidence$11 : scala.reflect.ClassTag[A]) : org.apache.spark.graphx.VertexRDD[A] = { /* compiled code */ }
  private[graphx] def aggregateMessagesWithActiveSet[A](sendMsg : scala.Function1[org.apache.spark.graphx.EdgeContext[VD, ED, A], scala.Unit], mergeMsg : scala.Function2[A, A, A], tripletFields : org.apache.spark.graphx.TripletFields, activeSetOpt : scala.Option[scala.Tuple2[org.apache.spark.graphx.VertexRDD[_], org.apache.spark.graphx.EdgeDirection]])(implicit evidence$12 : scala.reflect.ClassTag[A]) : org.apache.spark.graphx.VertexRDD[A]
  def outerJoinVertices[U, VD2](other : org.apache.spark.rdd.RDD[scala.Tuple2[org.apache.spark.graphx.VertexId, U]])(mapFunc : scala.Function3[org.apache.spark.graphx.VertexId, VD, scala.Option[U], VD2])(implicit evidence$13 : scala.reflect.ClassTag[U], evidence$14 : scala.reflect.ClassTag[VD2], eq : scala.Predef.=:=[VD, VD2] = { /* compiled code */ }) : org.apache.spark.graphx.Graph[VD2, ED]
  val ops : org.apache.spark.graphx.GraphOps[VD, ED] = { /* compiled code */ }
}
object Graph extends scala.AnyRef with scala.Serializable {
  def fromEdgeTuples[VD](rawEdges : org.apache.spark.rdd.RDD[scala.Tuple2[org.apache.spark.graphx.VertexId, org.apache.spark.graphx.VertexId]], defaultValue : VD, uniqueEdges : scala.Option[org.apache.spark.graphx.PartitionStrategy] = { /* compiled code */ }, edgeStorageLevel : org.apache.spark.storage.StorageLevel = { /* compiled code */ }, vertexStorageLevel : org.apache.spark.storage.StorageLevel = { /* compiled code */ })(implicit evidence$15 : scala.reflect.ClassTag[VD]) : org.apache.spark.graphx.Graph[VD, scala.Int] = { /* compiled code */ }
  def fromEdges[VD, ED](edges : org.apache.spark.rdd.RDD[org.apache.spark.graphx.Edge[ED]], defaultValue : VD, edgeStorageLevel : org.apache.spark.storage.StorageLevel = { /* compiled code */ }, vertexStorageLevel : org.apache.spark.storage.StorageLevel = { /* compiled code */ })(implicit evidence$16 : scala.reflect.ClassTag[VD], evidence$17 : scala.reflect.ClassTag[ED]) : org.apache.spark.graphx.Graph[VD, ED] = { /* compiled code */ }
  def apply[VD, ED](vertices : org.apache.spark.rdd.RDD[scala.Tuple2[org.apache.spark.graphx.VertexId, VD]], edges : org.apache.spark.rdd.RDD[org.apache.spark.graphx.Edge[ED]], defaultVertexAttr : VD = { /* compiled code */ }, edgeStorageLevel : org.apache.spark.storage.StorageLevel = { /* compiled code */ }, vertexStorageLevel : org.apache.spark.storage.StorageLevel = { /* compiled code */ })(implicit evidence$18 : scala.reflect.ClassTag[VD], evidence$19 : scala.reflect.ClassTag[ED]) : org.apache.spark.graphx.Graph[VD, ED] = { /* compiled code */ }
  implicit def graphToGraphOps[VD, ED](g : org.apache.spark.graphx.Graph[VD, ED])(implicit evidence$20 : scala.reflect.ClassTag[VD], evidence$21 : scala.reflect.ClassTag[ED]) : org.apache.spark.graphx.GraphOps[VD, ED] = { /* compiled code */ }
}
```

---



### 七：图算子：

- **控制属性的算子**
  - 类似map的map操作来修改点边的属性并将修改返回
- **控制结构的算子**
  - **reverse**：改变变得方向
  - **subgraph**：生成满足顶点与边的条件的子图
- **JOIN算子**
  - join算子：从外部的RDDs加载数据，修改顶点属性

```js
// join操作
    val newPoint: RDD[(VertexId, String)] = sc.parallelize(Array((3L,"HEHE"),(4L,"WYW")))
    // 与新节点inner join操作，相符合的id 进行一定的操作（点id,点id属性，替换新点值） 返回修改后的src点
    graph.joinVertices(newPoint)((id,src,newval) => {
      (src._1 +"@" + newval, src._2)
    }).vertices.foreach(x => println(x._2))


    graph.outerJoinVertices(newPoint)((id,src,newval) => {
      (src._1 +"@" + newval, src._2)
    }).vertices.foreach(x => println(x._2))
```

### 八：粉丝网络实例：

> **需求说明**

1. 数据：((User47,86566510),(User63,15647839))

   ​			((User67,86566510),(User77,15647839))

   ​			((User77,86566510),(User87,15647839))

   ​			((User87,86566510),(User47,15647839))

   ​			....

2. 格式：((User*, *),(User*,*))

   - (User*, *)=(用户名,用户ID)
   - 第一个用户表示被跟随者（followee）
   - 第二个用户表示跟随者（follower）

3. 创建图并计算每个用户的粉丝数量

4. 找出网络红人

```js
object FansNetwork {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("wyw").setMaster("local[*]")
    val sc = new SparkContext(conf)

    // 1.读文件
    val lines: RDD[String] = sc.textFile("E:\\大数据\\构建网络红人\\twitter_graph_data.txt").cache()
    // 2. 分割所有的点，并去重
    // val str = "((User47,86566510),(User83,15647839))"
    val pattern = "([a-zA-Z0-9]+),([0-9]+)".r
    val vects: RDD[(VertexId, String)] = lines.flatMap(str => {
      pattern.findAllIn(str).map(e => {
        val strings = e.split(",")
        (strings(1) toLong, strings(0))
      })
    }).distinct()

    // 3. 分割所有的边，权重设置为1
    val pattern1 = """\(\([a-zA-Z0-9]+,([0-9]+)\),\([a-zA-Z0-9]+,([0-9]+)\)\)""".r
    val edges = lines.flatMap(str => {
      val matches: Iterator[Regex.Match] =  pattern1.findAllMatchIn(str)
      matches.map(e => {
        Edge(e.group(1).toLong, e.group(2).toLong, 1)
      })
    })

    // 4.构成图
    val graph: Graph[String, Int] = Graph(vects, edges)

    // 5.查看所有点的入度，按入度排序，前N名就是网络红人
    val tuples: Array[(VertexId, Int)] = graph.inDegrees repartition 1 sortBy(-_._2) take 3

    // 键值对有join连接方法
    sc.makeRDD(tuples).join(vects).foreach(println)


  }

}
```



#### 