## Pregel框架：

### Spark GraphX Pregel：

- **Pregel是google提出的用于大规模分布式图计算框架**
  - 图遍历(bfs)
  - 单源最短路径（sssp）
  - pageRank计算
- **Pregel的计算有一系列迭代组成**
- **Pregel迭代过程**
  - 每个顶点从上一个superstep接收入站消息
  - 计算顶点新的属性
  - 在下一个superstep中向相邻的顶点发送消息
  - 当没有剩余消息时，迭代结束

### Pregel计算过程：

#### Pregel函数源码及各个参数解析：

```js
def pregel[A: ClassTag](
    // 图节点的初始信息
      initialMsg: A,
    // 最大迭代次数
      maxIterations: Int = Int.MaxValue,
    // 
      activeDirection: EdgeDirection = EdgeDirection.Either)(
      vprog: (VertexId, VD, A) => VD,
      sendMsg: EdgeTriplet[VD, ED] => Iterator[(VertexId, A)],
      mergeMsg: (A, A) => A)
    : Graph[VD, ED] = {
    Pregel(graph, initialMsg, maxIterations, activeDirection)(vprog, sendMsg, mergeMsg)
  }

```



| 参数            | 说明                                                         |
| --------------- | ------------------------------------------------------------ |
| initialMsg      | 图初始化的时候，开始模型计算的时候，所有节点都会先收到一个消息 |
| maxIterations   | 最大迭代次数                                                 |
| activeDirection | 规定了发送消息的方向                                         |
| vprog           | 节点调用该消息将聚合后的数据和本节点进行属性的合并           |
| sendMsg         | 激活态的节点调用该方法发送消息                               |
| mergeMsg        | 如果一个节点接收到多条消息，先用mergeMsg 来将多条消息聚合成为一条消息，如果节点只收到一条消息，则不调用该函数 |

### 案例：单源最短路径

**首先要清楚关于 顶点 的两点知识：**

1. 顶点 的状态有两种：
   (1)、钝化态【类似于休眠，不做任何事】
   (2)、激活态【干活】
2. 顶点 能够处于激活态需要有条件：
   (1)、成功收到消息 或者
   (2)、成功发送了任何一条消息

#### 第一步：调用pregel方法：

从5出发，除自身顶点外所有顶点都将接收一条初始消息initialMsg，使所有顶点处于激活态，并将属性改成无穷大。自身顶点为0。

#### 第二步：第一次迭代：

所有顶点以**EdgeDirection.Out**的边方向调用**sendMsg方法**发送消息给目标顶点，如果 **源顶点的属性+边的属性<目标顶点的属性**，则发送消息。否则不发送。

之后只有两条边的信息发送成功了

5—>3(0+8<Double.Infinity , 成功),
5—>6(0+3<Double.Infinity , 成功)

此时只有5，3，6处于激活态了，3，6调用vprog方法，将属性合并。



#### 第三步：第二次迭代：

处于激活态的3，6调用sendMsg方法发送消息。

最后只有3—>2(8+4<Double.Infinity,成功)

此时只有3，2处于激活态，2调用vprog方法将属性合并。

#### 第四步：不断迭代，直至所有顶点处于钝化态

每个顶点的属性，就是顶点5到达各个顶点的最短距离。

#### 案例代码如下：

```js
package com.wyw
  import org.apache.spark.{SparkConf, SparkContext}
  import org.apache.spark.graphx._
  import org.apache.spark.rdd.RDD
object Pregel {

    //1、创建SparkContext
    val sparkConf = new SparkConf().setAppName("GraphxHelloWorld").setMaster("local[*]")
    val sparkContext = new SparkContext(sparkConf)

    //2、创建顶点
    val vertexArray = Array(
      (1L, ("Alice", 28)),
      (2L, ("Bob", 27)),
      (3L, ("Charlie", 65)),
      (4L, ("David", 42)),
      (5L, ("Ed", 55)),
      (6L, ("Fran", 50))
    )
    val vertexRDD: RDD[(VertexId, (String,Int))] = sparkContext.makeRDD(vertexArray)

    //3、创建边，边的属性代表 相邻两个顶点之间的距离
    val edgeArray = Array(
      Edge(2L, 1L, 7),
      Edge(2L, 4L, 2),
      Edge(3L, 2L, 4),
      Edge(3L, 6L, 3),
      Edge(4L, 1L, 1),
      Edge(2L, 5L, 2),
      Edge(5L, 3L, 8),
      Edge(5L, 6L, 3)
    )
    val edgeRDD: RDD[Edge[Int]] = sparkContext.makeRDD(edgeArray)


    //4、创建图（使用aply方式创建）
    val graph1 = Graph(vertexRDD, edgeRDD)

    /* ************************** 使用pregle算法计算 ，顶点5 到 各个顶点的最短距离 ************************** */

    //被计算的图中 起始顶点id,初始化把点属性全部换成正无穷
    val srcVertexId = 5L
    val initialGraph = graph1.mapVertices{
      case (vid,(name,age)) =>
        if (vid==srcVertexId)
          0.0
        else
          Double.PositiveInfinity
    }

    //5、调用pregel柯里化函数
    val pregelGraph: Graph[Double, PartitionID] = initialGraph.pregel(
      Double.PositiveInfinity,
      Int.MaxValue,
      EdgeDirection.Out
    )(
      // 传三个匿名函数参数
      // 我收到消息后与本节点判断
      (vid: VertexId, vd: Double, distMsg: Double) => {
        // 比较两者值
        val minDist = math.min(vd, distMsg)
        println(s"顶点$vid，属性$vd，收到消息$distMsg，合并后的属性$minDist")
        // 把小数据发送出去
        minDist
      },
      // 是不是要向下个点发数据
      (edgeTriplet: EdgeTriplet[Double,PartitionID]) => {
        // 检查起点+权重的值 和终点的值判断，小于才发送
        if (edgeTriplet.srcAttr + edgeTriplet.attr < edgeTriplet.dstAttr) {
          println(s"顶点${edgeTriplet.srcId} 给 顶点${edgeTriplet.dstId} 发送消息 ${edgeTriplet.srcAttr + edgeTriplet.attr}")

          Iterator[(VertexId, Double)]((edgeTriplet.dstId, edgeTriplet.srcAttr + edgeTriplet.attr))
        } else {
          Iterator.empty
        }
      },
      // 多个消息进行判断，取最小的消息发送，每次都处理2个
      (msg1: Double, msg2: Double) => math.min(msg1, msg2)
    )

    //6、输出结果
    //  pregelGraph.triplets.collect().foreach(println)
    //  println(pregelGraph.vertices.collect.mkString("\n"))

    //7、关闭SparkContext
    sparkContext.stop()
    
}

```

