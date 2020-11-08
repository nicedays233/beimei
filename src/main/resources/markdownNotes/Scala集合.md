### Scala集合：

- 不可变集合

  - ```scala
    scala.collection.immutable
    ```

  ![image-20200702194909145](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200702194909145.png)

- 可变集合

  - ```scala
    scala.collection.mutable
    ```

  ![image-20200702194917740](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200702194917740.png)



> 常用集合如下：

|  **名称**   |    **可变/不可变**    |                           **示例**                           |
| :---------: | :-------------------: | :----------------------------------------------------------: |
| **Buffer**  |      **mutable**      | **val buffer = scala.collection.mutable.ArrayBuffer[Int](10,  20, 30);  buffer+=(2,3)** |
|  **Array**  |      **mutable**      |                   **val arr=Array(1,2,3)**                   |
|  **List**   |     **immutable**     |                   **val lst=List(1,2,3)**                    |
|   **Map**   |      **mutable**      |    **val stu= Map("name"  -> "Jason",  "age"  -> "18")**     |
|   **Set**   | **mutable/immutable** |                    **val set=Set(1,2,3)**                    |
| **Vector**  |     **immutable**     |             **val v=Vector(1, 3, 5, 7, 11, 13)**             |
|  **Stack**  | **mutable/immutable** | **val  st=scala.collection.mutable.Stack(1,2,3) //堆栈，先进后出** |
|  **Queue**  | **mutable/immutable** | **val  q=scala.collection.mutable.Queue(1,2,3) //队列，先进先出** |
| **BitSet**  | **mutable/immutable** | **val bit=scala.collection.mutable.BitSet(3,2,0)  //位集合** |
| **ListMap** |     **immutable**     | **val map =  scala.collection.immutable.ListMap(1->"one",  2->"two")** |
| **HashSet** |      **mutable**      |    **val set=  scala.collection.mutable.HashSet(1,2,3)**     |
| **HashMap** |      **mutable**      | **val stu= scala.collection.mutable.HashMap("name"  -> "Jason",  "age"  -> "18")** |

## Scala函数编写：



### 分区函数：



### Array方法：

`++`

- 合并数组

```scala
var c = Array(1,2,3)
var b = Array(4,5,6)
b++c
```



`++:`

- 合并数组 并将右边的类型作为最终结果返回

```scala
 val a = List(1,2)
 val b = scala.collection.mutable.LinkedList(3,4)
 val c = a ++: b
// 最后c为LinkList类型
```

`+:与:+: (elem: A): Array[A] `

- 在数组前添加一个元素

```js
val k = 0
val a = List(1,2)
val c = k +: a // c中的内容是 （0,1,2）
val d = a :+ k // d中的内容是 （1,2,0）
数组在哪冒号在哪
```

`/:与:\ (z: B)(op: (B, T) ⇒ B): B `--foldleft的简写

- 对数组中所有的元素进行相同的操作 

```js
val a = List(1,2,3,4)
val c = (10 /: a)(_+_)   // 1+2+3+4+10
val d = (10 /: a)(_*_)   // 1*2*3*4*10
println("c:"+c)   // c:20
println("d:"+d)   // d:240
冒号在哪边，集合就在哪边
```

`addString(b: StringBuilder,sep: String): StringBuilder`

```js
val a = List(1,2,3,4)
val b = new StringBuilder("678")
val c = a.addString(b)   // c中的内容是  1234
val d = a.addString(b,",") // 连接字符串时每个元素按分隔符隔开 
val e = a.addString(b,"shou",",","wei") // 在首尾各加一个字符串，并指定sep分隔符
```

![image-20200701172639737](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200701172639737.png)

`aggregate[B](z: ⇒ B)(seqop: (B, T) ⇒ B, combop: (B, B) ⇒ B): B `

- 聚合计算，aggregate是柯里化方法，参数是**两个方法**

`apply(i: Int): T`

- 取出指定索引处得元素

```js
arr.apply(index)
```

`canEqual(that: Any): Boolean `

- 判断两个对象是否可以进行比较

```js
arr.canEqual()
```

`charAt(index: Int): Char `--字符数组才有



```js
val chars = Array('a','b','c')
c.charAt()
```

`clone(): Array[T] `

- 创建一个副本，不是引用，是深拷贝

```js
val chars = Array('a','b','c')
val newchars = chars.clone()
```

`collect[B](pf: PartialFunction[A, B]): Array[B] `

- 执行一个并行计算，得到一个新的数组对象

```js
   val chars = Array('a','b','c')
   val newchars = chars.collect(fun)
   println("newchars:"+newchars.mkString(","))
  //我们通过下面的偏函数，把chars数组的小写a转换为大写的A
  val fun:PartialFunction[Char,Char] = {
    case 'a' => 'A'
    case x => x
  }
  /**输出结果是 newchars:A,b,c */
```

![image-20200702140954246](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200702140954246.png)



```js
val newchars = Array(22,442,653,3467)
val fun:PartialFunction[Char,Char] = {
	case y if %  2 == 0 =>  y + 5
}
```

![image-20200702143321656](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200702143321656.png)

![image-20200702143330720](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200702143330720.png)

`combinations(n: Int): collection.Iterator[Array[T]] `

- 拿到数组对应长度得所有排列组合

```js
val arr = Array("a","b","c")
val newarr = arr.combinations(2)// 返回了一个迭代器，长度为2得排列组合
newarr.foreach((item) => println(item.mkString(",")))
 /**
    a,b
    a,c
    b,c
 */
```

`contains[A1 >: A](elem: A1): Boolean `

- 序列中是否包含指定对象

```js
arr.contains(2)
```

`containSlice[B](that: GenSeq[B]): Boolean `

- 判断当前序列中是否包含另一个序列

```js
val a = List(1,2,3,4)
val b = List(2,3)
println(a.containsSlice(b))  //true
```

`copyToArray(xs: Array[A]): Unit `

- 数组中的内容拷贝到另外一个数组

```js
// 将a得数组拷贝给b，得从索引2开始拷
a.copyToArray(b,2)
```

![image-20200702144843703](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200702144843703.png)

`copyToBuffer[B >: A](dest: Buffer[B]): Unit `

```js
 val a:ArrayBuffer[Char]  = ArrayBuffer()
    b.copyToBuffer(a)
    println(a.mkString(","))
```

![image-20200702145402729](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200702145402729.png)

![](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200702145331731.png)

`corresponds[B](that: GenSeq[B])(p: (T, B) ⇒ Boolean): Boolean `

- 判断两个序列长度以及对应位置元素是否**符合某个条件**。如果两个序列具有**相同的元素数量并且对应位置得条件都成立**，返回结果为true 

```js
val a = Array(1, 2, 3)
val b = Array(4, 5,6)
println(a.corresponds(b)(_<_))  //true
```

`count(p: (T) ⇒ Boolean): Int `

- 统计符合条件的元素个数，x>2 大于2才做统计
- 下面统计大于 2 的元素个数

```js
val a = Array(1, 2, 3)
println(a.count({x:Int => x > 2}))  // count = 1
```



`diff(that: collection.Seq[T]): Array[T] `

- 返回当前数组与另一个数组比较后独一无二得元素

```js
val a = Array(1, 2, 3,4)
val b = Array(4, 5,6,7)
val c = a.diff(b)
println(c.mkString) //1,2,3
```



`distinct: Array[T] `

- 去除当前集合得重复元素

```js
val a = Array(1, 2, 3,4,4,5,6,6)
val c = a.distinct
println(c.mkString(","))    // 1,2,3,4,5,6
```





`drop(n: Int): Array[T]`

- 当前序列中前 n 个元素去除

```js
val a = Array(1, 2, 3,4)
val c = a.drop(2)
// 3,4
```

`dropRight(n: Int): Array[T]`

- 当前序列中尾部n 个元素去除

`dropWhile(p: (T) ⇒ Boolean): Array[T] `

- 去除符合条件得元素
- 但是有一个条件：从当前数组的第一个元素起，就要满足条件，直到碰到第一个不满足条件的元素结束（即使后面还有符合条件的元素）

```js
//下面去除大于2的，第一个元素 3 满足，它后面的元素 2 不满足，所以返回 2,3,4
val a = Array(3, 2, 3,4)
val c = a.dropWhile( {x:Int => x > 2} )
println(c.mkString(","))
 
//如果数组 a 是下面这样，第一个元素就不满足，所以返回整个数组 1, 2, 3,4
val a = Array(1, 2, 3,4) 
```

`endsWith[B](that: GenSeq[B]): Boolean `

- 判断是否以某个序列结尾

```js
val a = Array(3, 2, 3,4)
val b = Array(3,4)
println(a.endsWith(b))  //true
```

`exists(p: (T) ⇒ Boolean): Boolean `

- 判断当前数组是否包含符合条件的元素

```js
 val a = Array(3, 2, 3,4)
 println(a.exists( {x:Int => x==3} ))   //true
 println(a.exists( {x:Int => x==30} ))  //false
```

`filter(p: (T) ⇒ Boolean): Array[T] `

- 取得当前数组**中符合条件的元素**，组成新的数组返回

```js
val a = Array(3, 2, 3, 4)
val b = a.filter( {x:Int => x > 2} )
println(b.mkString(","))    //3,3,4
```

`find(p: (T) ⇒ Boolean): Option[T] `

- 查找第一个符合条件得某个东西

```js
val a = Array(1, 2, 3,4)
val b = a.find( {x:Int => x>2} )
// val b = a.find( x => x > 2 )
println(b)  // Some(3)
val b = a.find( {x:Int => x>2} ).get // 拿值
```

`flatMap[B](f: (A) ⇒ GenTraversableOnce[B]): Array[B] `

- flat和map，先map后flatten、
- map一般都会形成嵌套集合，需要flat扁平化

```js
val a = Array(1, 2, 3,4)
val b = a.flatMap(x=>1 to x)
println(b.mkString(","))
/**
1,1,2,1,2,3,1,2,3,4
从1开始，分别于集合a的每个元素生成一个递增序列，过程如下
1
1,2
1,2,3
1,2,3,4
*/
```

![image-20200702153758372](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200702153758372.png)

`fold[A1 >: A](z: A1)(op: (A1, A1) ⇒ A1): A1 `

- 对序列中的每个元素进行二元运算

```js
  def seqno(m:Int,n:Int): Int ={
    val s = "seq_exp=%d+%d"
    println(s.format(m,n))
    return m+n
  }
  def combine(m:Int,n:Int): Int ={
    val s = "com_exp=%d+%d"
    println(s.format(m,n))
    return m+n
  }
    val a = Array(1, 2, 3,4)
    val b = a.fold(5)(seqno)
    /** 运算过程
    seq_exp=5+1
    seq_exp=6+2
    seq_exp=8+3
    seq_exp=11+4
    */
    val c = a.par.aggregate(5)(seqno,combine)
    /** 运算过程
    seq_exp=5+1
    seq_exp=5+4
    seq_exp=5+3
    com_exp=8+9
    seq_exp=5+2
    com_exp=6+7
    com_exp=13+17
    */
```

`foldRight[B](z: B)(op: (B, T) ⇒ B): B `

```js
  def seqno(m:Int,n:Int): Int ={
    val s = "seq_exp=%d+%d"
    println(s.format(m,n))
    return m+n
  }
    val a = Array(1, 2, 3,4)
    val b = a.foldRight(5)(seqno)
    /** 运算过程
    seq_exp=4+5
    seq_exp=3+9
    seq_exp=2+12
    seq_exp=1+14
    */
    /**
    简写 (a :\ 5)(_+_)
    */
```

`forall`

- 对集合中的元素进行某个判断，全部为true则返回true，反之返回false

```js
scala> var s = List("hello", "world")
s: List[String] = List(hello, world)

scala> s.forall( f => f.contains("h") )
res34: Boolean = false

scala> s.forall( f => f.contains("o") )
res35: Boolean = true
```

`exist`

- 对集合中的元素进行某个判断，其中之一符合条件则返回true，反之返回false。和forall是一个对应的关系，相当于 and 和 or。

```js
scala> s.exists( f => f.contains("h") )
res36: Boolean = true
```

`foreach(f: (A) ⇒ Unit): Unit `

- 遍历序列中的元素，进行 f 操作,类似迭代器，只能执行一次

```js
    val a = Array(1, 2, 3,4)
    a.foreach(x => println(x*10))
    /**
    10
    20
    30
    40
    */
```

`groupBy[K](f: (T) ⇒ K): Map[K, Array[T]] `

- 按条件分组，条件由 f 匹配，返回值是Map类型，每个key对应一个序列，下面代码实现的是，把小于3的数字放到一组，大于3的放到一组，返回Map[String,Array[Int]]

```js
    val a = Array(1, 2, 3,4)
    val b = a.groupBy( x => x match {
      case x if (x < 3) => "small"
      case _ => "big"
    })
```

`grouped(size: Int): collection.Iterator[Array[T]] `

- 按指定数量分组，每组有 size 数量个元素，返回一个集合迭代器

```js
val a = Array(1, 2, 3,4,5)
val b = a.grouped(3).toList
b.foreach((x) => println("第"+(b.indexOf(x)+1)+"组:"+x.mkString(",")))
/**
第1组:1,2,3
第2组:4,5
*/
```

`hasDefiniteSize: Boolean `

- 检测序列是否存在有限的长度，对应Stream这样的流数据，返回false

```js
val a = Array(1, 2, 3,4,5)
println(a.hasDefiniteSize)  //true
```



`head()`

- 拿头元素

```js
arr.head
```

`last()`

- 拿尾元素

```js
arr.last
```

`indexOf(elem: T, from: Int): Int `

- elem在序列中的索引，找到第一个就返回

```js
val a = Array(1, 3, 2, 3, 4)
println(a.indexOf(3))   // return 1

// 返回elem在序列中的索引，可以指定从某个索引处（from）开始查找，找到第一个就返回
val a = Array(1, 3, 2, 3, 4)
println(a.indexOf(3,2)) // return 3
```

`indexOfSlice[B >: A](that: GenSeq[B], from: Int): Int  `

- 检测当前序列中是否包含另一个序列（that），并返回第一个匹配出现的元素的索引

```js
 val a = Array(1, 3, 2, 3, 4)
 val b = Array(2,3)
 println(a.indexOfSlice(b))  // return 2
```

` indexWhere(p: (T) ⇒ Boolean, from: Int): Int  `

- 返回当前序列中第一个满足 p 条件的元素的索引，可以指定从 from 索引处开始

```js
 val a = Array(1, 2, 3, 4, 5, 6)
 println(a.indexWhere( {x:Int => x>3},4))    // return 4
```

`indices: collection.immutable.Range `

```js
 val a = Array(10, 2, 3, 40, 5)
 val b = a.indices
 println(b.mkString(","))    // 0,1,2,3,4
```

`init: Array[T]`

- 返回当前序列中不包含最后一个元素的序列

```js
val a = Array(10, 2, 3, 40, 5)
val b = a.init
println(b.mkString(","))    // 10, 2, 3, 40
```

`tail()`

- 去头元素

```js
 val a = Array(10, 2, 3, 40, 5)
 val b = a.tail
 println(b.mkString(","))    // 2, 3, 40，5
```

`intersect(that: collection.Seq[T]): Array[T] `

- 取两个集合的交集

```js
  val a = Array(1, 2, 3, 4, 5)
  val b = Array(3, 4, 6)
  val c = a.intersect(b)
  println(c.mkString(","))    //return 3,4
```

`isDefinedAt(idx: Int): Boolean `

- 判断序列中是否存在指定索引

```js
 val a = Array(1, 2, 3, 4, 5)
 println(a.isDefinedAt(1))   // true
 println(a.isDefinedAt(10))  // false
```

`isEmpty: Boolean `

- 判断当前序列是否为空

`isTraversableAgain: Boolean `

- 判断序列是否可以反复遍历

![image-20200707094251969](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200707094251969.png)

`Iterator: collection.Iterator[T] `

- 对序列每个元素产生一个iterator

`lastIndexOf(elem: T, end: Int): Int`

- 取序列最后一个等于ele元素的位置

`lastIndexWhere(p: (T) ⇒ Boolean): Int `

- 从右边往左边找第一个满足条件的索引

`lastOption: Option[T]`

- 返回当前序列最后一个对象（some或者none）

`lengthCompare(len: Int): Int `

- 数组长度减括号里面的值，返回值

`map[B](f: (A) ⇒ B): Array[B] `

- 对序列的元素进行操作

**wordcount：**

![image-20200707105717841](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200707105717841.png)

![image-20200707105649066](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200707105649066.png)

`mkString: String `

- 将所有元素组合成字符串，以xx做分隔符

`nonEmpty: Boolean `

- 判断序列不是空

`padTo(len: Int, elem: A): Array[A] `

- 比设定长度少，就补齐，多就减去

```js
 val a = Array(1, 2, 3, 4, 5)
 val b = a.padTo(7,9)    //需要一个长度为 7  的新序列，空出的填充 9
 println(b.mkString(","))    // return  1,2,3,4,5,9,9
```

`par: ParArray[T] `

`partition(p: (T) ⇒ Boolean): (Array[T], Array[T]) `

- 由于返回的是布尔值，所以只能返回两个区 **(Array[T], Array[T])** 

```js
 val a = Array(1, 2, 3, 4, 5)
 val b:(Array[Int],Array[Int]) = a.partition( {x:Int => x % 2 == 0})
 println(b._1.mkString(","))     // return  2,4
 println(b._2.mkString(","))     // return  1,3,5
```

![image-20200708094502760](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200708094502760.png)

`多分组`

![image-20200708094828532](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200708094828532.png)

`patch(from: Int, that: GenSeq[A], replaced: Int): Array[A] `

- 批量替换，第一个是开始位置，第三个替换数量个元素，第二个是将被替换成某序列

```js
 val a = Array(1, 2, 3, 4, 5)
 val b = Array(3, 4, 6)
 val c = a.patch(1,b,2)
 println(c.mkString(","))    // return 1,3,4,6,4,5
    /**从 a 的第二个元素开始，取两个元素，即 2和3 ，这两个元素被替换为 b的内容*/
```

`permutations: collection.Iterator[Array[T]] `

- 排列组合，他与combinations不同的是，组合中的内容可以相同，但是顺序不能相同，combinations不允许包含的内容相同，即使顺序不一样

```js
    val a = Array(1, 2, 3, 4, 5)
    val b = a.permutations.toList   // b 中将有120个结果，知道排列组合公式的，应该不难理解吧
    /**如果是combinations*/
    val b = a.combinations(5).toList    // b 中只有一个，因为不管怎样排列，都是这5个数字组成，所以只能保留第一个
```

`prefixLength(p: (T) ⇒ Boolean): Int `

- 给定一个条件 p，返回一个前置数列的长度，这个数列中的元素都满足 p

```js
    val a = Array(1,2,3,4,1,2,3,4)
    val b = a.prefixLength( {x:Int => x<3}) // b = 2
```

`product`

- 返回所有元素乘积的值---阶乘

```js
    val a = Array(1,2,3,4,5)
    val b = a.product       // b = 120  （1*2*3*4*5）
```

`reduce[A1 >: A](op: (A1, A1) ⇒ A1): A1 `

- **同 fold，不需要初始值**
- 只处理数据的一部分为偏函数

```js
val a = Array(1,2,3,4,5)
val b = a.reduce(seqno)// 直接聚合
println(b)    // 15
  /**
    seq_exp=1+2
    seq_exp=3+3
    seq_exp=6+4
    seq_exp=10+5
  */
reduce(_+_)// 用拿到的两参数相加`
```

`reverse: Array[T] `

- 反转序列

```js
val a = Array(1,2,3,4,5)
val b = a.reverse
println(b.mkString(","))    //5,4,3,2,1
```

`reserveIterator: collection.Iterator[T] `

- 反向生成迭代

`reserveMap[B](f: (A) ⇒ B): Array[B] `

- 同 map 方向相反

`sameElements(that: GenIterable[A]): Boolean `

- 判断两个序列是否顺序和对应位置上的元素都一样



`scan[B >: A, That](z: B)(op: (B, B) ⇒ B)(implicit cbf: CanBuildFrom[Array[T], B, That]): That `

- 用法同 fold，scan会把每一步的计算结果放到一个新的集合中返回，而 fold 返回的是单一的值

```js
  val a = Array(1,2,3,4,5)
  val b = a.scan(5)(seqno)
  println(b.mkString(","))    // 5,6,8,11,15,20
```

`segmentLength()`

- 从序列的 from 处开始向后查找，所有满足 p 的连续元素的长度

```js
 val a = Array(1,2,3,1,1,1,1,1,4,5)
 val b = a.segmentLength( {x:Int => x < 3},3)        // 5
```

`slice(from: Int, until: Int): Array[T] `

- 取出当前序列中，from 到 until 之间的片段

```js
    val a = Array(1,2,3,4,5)
    val b = a.slice(1,3)
    println(b.mkString(","))    // 2,3
```

`sliding(size: Int): collection.Iterator[Array[T]] `

- 从第一个元素开始，每个元素和它后面的 size - 1 个元素组成一个数组，最终组成一个新的集合返回，当剩余元素不够 size 数，则停止

```js
    val a = Array(1,2,3,4,5)
    val b = a.sliding(3).toList
    for(i<-0 to b.length - 1){
      val s = "第%d个：%s"
      println(s.format(i,b(i).mkString(",")))
    }
      /**
    第0个：1,2,3
    第1个：2,3,4
    第2个：3,4,5
    第3个：4,5
    第4个：5
      */
// 步长为2
a.sliding(3,2).toList
```

`sortBy[B](f: (T) ⇒ B)(implicit ord: math.Ordering[B]): Array[T] `

- 按指定的排序规则排序

- 如果数组里有数字有字符串，排序会报错

```js
    val a = Array(3,2,1,4,5)
    val b = a.sortBy( {x:Int => x})// 升序
	val b1 = a.sortBy( {x:Int => 0-x})// 降序
    println(b.mkString(","))    // 1,2,3,4,5
```

`sortWith(lt: (T, T) ⇒ Boolean): Array[T] `

- 自定义排序方法
- 当数组里有数字有字符串就先转字符在判断

```js
    val a = Array(3,2,1,4,5)
    val b = a.sortWith(_.compareTo(_) > 0)  // 大数在前

    println(b.mkString(","))    // 5,4,3,2,1
```

![image-20200708090534249](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200708090534249.png)

![image-20200708091923925](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200708091923925.png)

`span(p: (T) ⇒ Boolean): (Array[T], Array[T]) `

- 分割序列为两个集合，从第一个元素开始，直到找到`第一个不满足条件的元素`止，之前的元素放到第一个集合，其它的放到第二个集合

```js
    val a = Array(3,2,1,4,5)
    val b = a.span( {x:Int => x > 2})
    println(b._1.mkString(","))     //  3
    println(b._2.mkString(","))     //  2,1,4,5
```

`startWith[B](that: GenSeq[B], offset: Int): Boolean `

- 从指定偏移处，是否以某个序列开始

```js
    val a = Array(0,1,2,3,4,5)
    val b = Array(1,2)
    println(a.startsWith(b,1))      //  true
```

`stringPrefix()`

- 返回` toString `结果的前缀

```js
 val a = Array(0,1,2,3,4,5)
 println(a.toString())       //[I@3daa57fb
 val b = a.stringPrefix
 println(b)      //[I
```

`subSequence(start: Int, end: Int): CharSequence`

- 返回start和end间的字符序列

```js
val chars = Array('a','b','c','d')
val b = chars.subSequence(1,3)
println(b.toString)     //  bc
```

`take(n: Int): Array[T] `

- 返回当前序列中前 n 个元素组成的序列

```js
 val a = Array(1,2,3,4,5)
 val b = a.take(3)       //  1,2,3
```

`takeRight(n: Int): Array[T]`

```js
val a = Array(1,2,3,4,5)
val b = a.takeRight(3)      //  3,4,5
```

`takeWhile(p: (T) ⇒ Boolean): Array[T]`

```js
val a = Array(1,2,3,4,5)
val b = a.takeWhile( {x:Int => x < 3})      //  1,2
```

`transform`



`transpose[U](implicit asArray: (T) ⇒ Array[U]): Array[Array[U]]`

- 矩阵转换，二维数组行列转换

```js
    val chars = Array(Array("a","b"),Array("c","d"),Array("e","f"))
    val b = chars.transpose
    println(b.mkString(","))
```

`update(i: Int, x: T): Unit`

- 将序列中 i 索引处的元素更新为 x

```JS
    val a = Array(1,2,3,4,5)
    a.update(1,9)
    println(a.mkString(","))        //1,9,3,4,5
```

`updated(index: Int, elem: A): Array[A] `

```JS
    val a = Array(1,2,3,4,5)
    a.update(1,9)
    println(a.mkString(","))        //1,9,3,4,5
```

`zip[B](that: GenIterable[B]): Array[(A, B)] `

- 将两个序列对应位置上的元素组成一个pair序列

```JS
    val a = Array(1,2,3,4,5)
    val b = Array(5,4,3,2,1)
    val c = a.zip(b)
    println(c.mkString(","))        //(1,5),(2,4),(3,3),(4,2),(5,1)
```

`zipAll[B](that: collection.Iterable[B], thisElem: A, thatElem: B): Array[(A, B)]`

- 同 zip ，但是允许两个序列长度不一样，不足的自动填充，如果当前序列端，空出的填充为 thisElem，如果 that 短，填充为 thatElem

```JS
    val a = Array(1,2,3,4,5,6,7)
    val b = Array(5,4,3,2,1)
    val c = a.zipAll(b,9,8)         //(1,5),(2,4),(3,3),(4,2),(5,1),(6,8),(7,8)
 
    val a = Array(1,2,3,4)
    val b = Array(5,4,3,2,1)
    val c = a.zipAll(b,9,8)         //(1,5),(2,4),(3,3),(4,2),(9,1)
```

