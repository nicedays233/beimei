## Scala数据结构：

### 稀疏数组--sparsearray数组：

> 二维数组中有很多默认值为0的数据

#### 稀疏数组的处理方法：

- 记录数组一共有**几行几列**，有**多少有效值**
- 把具有**不同值的元素的行列及值，记录在一个小规模的数组**中，从而缩小规模

| row  | col  | val  |                      |
| ---- | ---- | ---- | -------------------- |
| 11   | 11   | 2    | 矩阵大小和有效值个数 |
| 1    | 2    | 1    | 有效值位置和值       |
| 2    | 3    | 3    | 有效值位置和值       |

#### 应用实操：

- 使用稀疏数组，来保留类似前面的二维数组（地图，棋盘等）
- 把稀疏数组存盘，并且可以重新恢复成原来的二维数组数

```js
package com.wyw

import scala.collection.mutable.ArrayBuffer

object SparseArrayDemo2 {
  def main(args: Array[String]): Unit = {
    // 先使用二维数组，映射棋盘
    val rows = 11
    val cols = 11
    val chessMap1 = Array.ofDim[Int](rows, cols)

    // 初始化
    chessMap1(1)(2) = 1 // 表示黑子
    chessMap1(2)(3) = 2 // 表示蓝子

    chessMap1(7)(2) = 1 // 表示黑子
    chessMap1(2)(6) = 2 // 表示蓝子

    println("原始的棋盘")

    for (row <- chessMap1) {
      for (elem <- row) {
        printf("%d  ", elem)
      }
      println()
    }

    // 对原始的二维数据进行压缩
    // 思路
    // 1.创建ArrayBuffer，动态添加数据
    // 2.使用node对象，标识一个数据

    val sparseArray = ArrayBuffer[Node]()
    // 先将第一行数据放入
    sparseArray.append(new Node(rows,cols,0))

    // 遍历棋盘chessMap1，如果发现有非0值，就创建node对象，加入到sparseArray

    for (i <- chessMap1.indices){
      for (j <- chessMap1(i).indices) {
        if (chessMap1(i)(j) != 0){
          sparseArray.append(new Node(i,j,chessMap1(i)(j)))
        }
      }
    }

    println("稀疏数组情况是")
    for (elem <- sparseArray.indices) {
      val node = sparseArray(elem)
      printf("%d %d %d\n", node.row, node.col, node.value)
    }


    // 稀疏数组恢复成原始棋盘
    // 1. 读取稀疏数组的第一行，创建一个二维棋盘
    // 2. 遍历（从稀疏数组的第二行），每读取到一个node，就将对应的值，恢复到chessmap2
    val node = sparseArray(0)
    val chessMap2 = Array.ofDim[Int](node.row, node.col)
    for (elem <- 1 until sparseArray.length) {
      val node1 = sparseArray(elem)
      chessMap2(node1.row)(node1.col) = node1.value // 对应位置带值
    }


    println("恢复后的棋盘是")

    for (row <- chessMap2) {
      for (elem <- row) {
        printf("%d  ", elem)
      }
      println()
    }

  }
}

class Node(val row: Int, val col: Int, val value: Int)

```



### 队列

- 队列为有序列表
- front指针初始化为-1，表示队列头，但不包含头元素
- rear初始为-1，表示队列尾，包含尾元素

`判断非环队列空：front == rear`

`判断非环队列满：rear == MaxSize - 1`

```js

```

创建数组：

| 1    | **def ofDim[T]( n1: Int ): Array[T]**创建指定长度的数组      |
| ---- | ------------------------------------------------------------ |
| 2    | **def ofDim[T]( n1: Int, n2: Int ): Array[Array[T]]**创建二维数组 |
| 3    | **def ofDim[T]( n1: Int, n2: Int, n3: Int ): Array[Array[Array[T]]]**创建三维数组 |