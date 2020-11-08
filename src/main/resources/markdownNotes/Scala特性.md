##  函数:

> def定义的都为方法，不是函数

### 懒值：

> 初始化推迟，第一次调用变量时才会被初始化

```js
//  
lazy val word = scala.id.Source.fromFile("").mkString
```

- 解决初始化开销很大的语句

### 闭包（closure）：

`肉眼看到效果：在函数内部可以访问到函数体外的变量或者是其他函数的变量`

`实际操作：将函数能访问的变量（如果这个变量是其他函数的，它会复制一份出来）和这个函数都封装成了只有一个方法的对象`

`最后导致效果：看上去让两个函数都可以拥有相同的变量名，但是操作变量时，双方互不影响`



### 柯里化：

> 把接受多个参数的函数变换成接受一个单一参数(最初函数的第一个参数)的函数，并且返回接受余下的参数且返回结果的新函数的技术

其实这很好理解，柯里化的本质就是揭示了任何函数哪怕是多参数的，都可以转化成单参数的叠加。

`def定义柯里化方法`

```js
// 实现过程
def mulOne(x: Int) = { (y: Int) => x * y }

def mulOne(x: Int) = (y: Int) => x * y 

def mulOne(x: Int)(y: Int) = x　* y
//方法类型 mulOne: (x: Int)(y: Int) Int 
```

`val定义函数时`

```js
// val 可以定义匿名函数，这下面相当于嵌套了两层匿名函数
val mulOne = (x: Int) => (y: Int) => x * y
// 函数类型： Int => (Int => Int)
```



### 隐式参数：

> 标记一个implicit的参数列表

```js
def sum(score: Int)(implicit y:Int): Int 
```

### 隐式转换：

`隐式转换触发机制:`

- 当表达式的类型与预期的类型不同时
- 当对象访问一个不存在的成员
- 当对象调用某个方法,而方法的参数声明与传入参数不匹配时



### _常用场景:

- 模式匹配

- 导包中的所有类

- 函数赋值

  ```js
  
  // me
  def fun = {
      println("call")
  }
  val v = fun // 调用函数fun
  val f = fun _ // 将函数fun赋值给f
  ```


### 偏函数：

> 在对符合某个条件，而不是所有情况进行逻辑操作时，使用偏函数是一个不错的选择。
>
> 将包在大括号内的一组case语句封装为函数，我们称为偏函数
>
> 偏函数是一个特质PatrialFunction

`具体形式：`

```js
val fun1 = new PartialFunction[Any: Int] {
    // 当返回真，就去调用apply，构建对象实例，假就不调用
   override def isDefinedAt(x: Any) = {
       println("x=" + x)
       x.isInstanceOf[Int]
   }
    
    override def apply(v1: Any) = {
        v1.asInstanceOf[Int] + 1
    }
}
```

`简写形式：`

```js
val fun1: PartialFunction[Any: Int] {
    case i: Int => i + 1
}
// 再简化
val list3 = list.collect{case i: Int => i + 1}// 写多行也没有问题
```



`collect调用：`

```js
list.collect(fun1)
```

![image-20200715085533394](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200715085533394.png)

### 模式匹配：

### Scala正则表达式：

- 查找

```js

```



- 替换
- 匹配
- 截取





## 类与对象:

### 类：

>  类中无法定义静态成员变量和方法

- 构造器
  - 主构造器
  - 辅助构造器
- 成员变量与方法
- 类的实例化

### 内部类：

- 一个类可以作为另一个类的成员
  - java内部类是外部类的成员
  - scala内部类绑定到外部类的对象实例
- 给自己用的，用来新建对象

### 样例类(case class)--实体类

>  用于描述不可变的值对象

- `样例类构造参数为val，自动实现类构造参数的getter`
- `样例类构造参数为var，自动实现类构造参数的setter和getter`
- `自动创建伴生对象`
- `自动实现其他方法`
  - toString，equals，copy, hashcode,
  - 伴生对象的apply和unapply

### 枚举类：

```js
object Weekday  extends Enumeration {
  //枚举值从0开始计数
  val Mon,Tue,Wed,Thu,Fri,Sat,Sun=Value
}
```



### 泛型类：

> 泛型类指可以接受类型参数的类，泛型类在集合类中被广泛使用

```js
class Stack[T] {
    var elements: List[T] = Nil
    def push(x: T) { elements = x :: elements }
    def top: T = elements.head
    def pop() {
      var t = elements.head
      elements = elements.tail
      t
    }
    def showElements(){
      elements.foreach(x=>print(s"$x "));println()}
  }

```

### 隐式类：





### 类型边界：

#### 类型上界：

- T<:A 表示类型变量T应该是类型A的**子类**

#### 类型下界：

- T>:A 表示类型变量T应该是类型A的**超类**

  

### 型变：

> java对于协变的一致性问题可以用  ? extends T  来解决

- `协变` 类似于<:  但是它可以事先不知道是哪个类型的子类,传入再确定是什么类型，而<:已经确定了是A的类型的子类

  

  > 对于两种类型 A 和 B，如果 A 是 B 的子类型，那么 Foo[A] 就是 Foo[B] 的子类型

  ```js
  class Foo[+T] // 协变类
  ```

- `逆变`

  > 对于两种类型 A 和 B，如果 A 是 B 的子类型，那么 Bar[B] 就是 Bar[A] 的子类型

  ```js
  class Bar[-T] // 逆变类
  ```

  `不变`

  > 默认情况下，Scala中的泛型类是不变的

  ```js
  class Baz[+T] //不协变类
  ```

### get/set:

- scala自动生成get/set方法

```js
var _name: String = _
```

- 当需要自定义时.自己重写的get /set 方法

```js
class Person {
    
    private[this] var _name: String = _

    def name: String = _name

    def name_=(value: String): Unit = _name = value
 
}
```

- 加注解自动生成兼容java的get/set方法

```scala
@BeanProperty var name: Int = _
```

### 单例对象：

> scala类中无法定义静态成员，object来表示静态成员和方法



### 伴生对象:

> 当你的类需要用到你的对象时,即用到既有实例方法又有静态方法的类.通常我们使用伴生对象完成

- 伴生类与伴生对象可互相访问各自私有成员
- 伴生对象可为伴生类增加静态成员

```js
// 伴生类
class Account(n: Int) {
    val id = Account.newUniqueNumber()
}
// 伴生对象
object Account {
    // 用伴生对象来代替new
    def apply(n: Int): Account = new Account(n: Int);
    private var lastNumber = 0
    private def newUniqueNumber = lastNumber += 1
}
// apply方法名默认可以不用写
Account(5)

```



## 特质:

### trait特征--接口+抽象类

> 多个类具有相同的特征1时，就可以将这个特征独立出来，采用关键字trait来声明。
>
> java中的接口都可以当作特质来使用。

- 特质本质还是用了java的抽象类来完成了方法的具体实现，在反编译过程中会发现，特质会去生成一个【特质名$class.class】的一个抽象类和一个【特质名】的接口，抽象类会去实现该接口的方法，

![image-20200712162312628](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200712162312628.png)

### 动态混入：

> b和c如果    都应用了某特质，b去实现了该特质的某种方法，c并不会收到影响，完成了解耦而java接口会因为传递性，c会有b实现的方法。



```js
var xxx = new Operate with OperateTrait
// 构建对象时混入的特质，对象可以使用特质的方法

```

![image-20200714085752343](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200714085752343.png)

![image-20200712164623213](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200712164623213.png)

### scala创建对象有几种方式：

- new 对象
- apply 创建
- 匿名子类方式
- 动态混入

### 叠加特质：

> 构建对象的同时混入多个特质，称为叠加特质

**那么特质声明顺序从左到右，方法执行顺序从右到左**

> 菱形结构相同父类

![image-20200712170126194](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200712170126194.png)

### 扩展特质：

> 特质继承类来扩展实现一些类的功能

