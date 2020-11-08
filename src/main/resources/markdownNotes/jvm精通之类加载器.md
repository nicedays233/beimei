# JVM类加载器：

## 类加载器子系统：

![image-20200715140908531](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200715140908531.png)

### 作用：

- 从文件系统或网络中加载class文件在文件开头有特定得文件标识
- ClassLoader只负责class文件得加载，至于它是否可以运行，则有Execution Engine（执行引擎）决定
- 加载得类信息存放于一块称为方法区得内存空间，除了类得信息外，方法去中还会存放运行时**常量池信息**，可能还包括字符串字面量和数字常量（这部分常量信息是class文件中常量池部分得内存映射）

## 类加载过程：

### 一：Loading--加载阶段

- 通过一个类得全限定名获取定义此类得二进制字节流。
- 将这个字节流所代表得静态存储结构转化为方法区得运行时数据结构。
- **在内存中生成一个代表这个类得java.lang.Class对象**，作为方法区这个类得各种数据访问入口。

#### 补：加载class文件得方式：

- 从本地系统中直接加载
- 通过网络获取，典型场景：web applet
- 从zip压缩包中读取，成为日后jar，war格式得基础
- 运行时计算生成，---动态代理技术
- 由其他文件生成，---jsp应用
- 从专有数据库中提取class文件，比较少见
- 从加密文件中获取，典型得防class文件被反编译得保护措施

### 二：linking--链接阶段

#### 验证（verify）

- 目的在于确保Class文件得字节流中包含信息符合当前虚拟机要求，**保证被加载类的正确性**，不会危害虚拟机自身安全。
- 主要包括四种验证：**文件格式验证，元数据验证，字节码验证，符号引用验证。**

字节码文件起始有个模数：CA FE BA EE，检测开头是否合法

#### 准备（prepare）

- 为类变量分配内存并且设置**该类变量得默认初始值，及零值**
- 这里**不包含用final修饰得static**，**因为final在编译得时候就会分配了，准备阶段会显式初始化。**
- **这里不会为实例变量分配初始化**，类变量会分配在方法区中，而实例变量是会随者对象一起分配到java堆中。

#### 解析（resolve）

- 将常量池内得**符号引用**转换为**直接引用**得过程。
- 事实上，解析操作往往会伴随着jvm在执行完初始化之后再执行。
- 符号引用就是一组符号来描述所引用得目标，符号引用得字面量形式明确定义在《java虚拟机规范》的Class文件格式中，直接引用就是直接指向目标的指针，相对偏移量或一个间接定位到目标的句柄。
- 解析动作主要针对类或接口，字段，类方法，接口方法，方法类型等，对应常量池中的CONSTANT_Class_info,CONSTANT_Fieldref_info,CONSTANT_Methodref_info等。

### 三：Initialization--初始化阶段

#### 初始化：

- 初始化阶段就是**执行类构造器方法<clinit>()**的过程
- 此方法不需定义，是javac编译器自动收集类中的所有类变量的赋值动作和静态代码块中的语句合并而来。如果没有申明静态代码就不会出现<clinit>
- 构造器方法中指令按语句在源文件中出现的顺序执行
- <clinit>（）不同于类的构造器。（关联：构造器是虚拟机视角下的<init>()）
- 若该类具有父类，JVM会保证子类的<clinit>（）执行前，父类的<clinit>()已经执行完毕。
- 虚拟机必须保证一个类的<clinit>()方法在多线程下被同步加锁。

 

## 类加载器分类：



![image-20200715151320768](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200715151320768.png)

>用户自定义类是由系统类加载器加载的
>
>String类是由引导类加载器加载的--java核心类库是由引导类加载器加载的

### 引导类加载器（Bootstrap ClassLoader）：

- 这个类加载使用**C/C++语言实现的**，嵌套在JVM内部
- 它用来**加载java的核心库**（例如JAVA_HOME/jre/lib/rt.jar，/resources.jar或sun.boot.class.path路径下的内容）,用于提供jvm自身需要的类
- 并不继承自java.lang.ClassLoader，没有父加载器。
- 加载扩展类和应用程序类加载器，并**指定为他们的父类加载器**。
- 出于安全考虑，bootstrap启动类加载器只加载包名为java，javax，sun等开头的类。

### 自定义类加载器（User-Defined ClassLoader）：

> 将所有派生于抽象类ClassLoader的类加载器都划分为自定义加载器

#### 扩展类加载器--Extension ClassLoader

- java语言编写，由sun.misc.Launcher$ExtClassLoader实现
- **派生于ClassLoader类**
- 父类加载器为**启动类加载器**。
- 从java.ext.dirs系统属性所指定的目录中加载类库，或从JDK的安装目录的jre/lib/ext子目录下加载类库，**如果用户创建的JAR放在此目录下，也会自动由扩展类加载器加载。**

#### 系统类加载器（应用程序类加载器，AppClassLoader）

- java语言编写，由sun.misc.Launcher$AppClassLoader实现

- **派生于ClassLoader类**

- 父类加载器为**扩展类加载器**。

- 负责加载环境变量**classpath或系统属性  java.class.path  指定路径下的类**库

- **该类加载是程序中默认的类加载器**，一般来说，java应用的类都是由它来完成加载

- 通过ClassLoader#getSystemClassLoader()方法可以获取到该类加载器

  

#### 用户自定义类加载器

> 我们可以自定义类加载器，来定制类的加载方式

- 隔离加载类
- 修改类加载的方式
- 扩展加载源
- 防止源码泄露

`用户自定义类加载器实现步骤：`

1. 开发人员通过继承抽象类java.lang.ClassLoader类的方式，实现自己的类加载器，以满足一些特殊的需求。
2. jdk1.2之后将自定义类得加载逻辑写在findClass()方法中
3. 在编写自定义类加载器时，如果没有太过于复杂的需求，可以直接继承URLClassLoader类，可以避免自己去编写findClass（）方法及其获取字节码流的方式。

## ClassLoader:

> ClassLoader类，它是一个抽象类，其后所有的类加载器都继承子ClassLoader（不包括启动类加载器）

![image-20200715160844143](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200715160844143.png)

| 方法名称                                              | 描述                                                         |
| ----------------------------------------------------- | ------------------------------------------------------------ |
| getParent（）                                         | 返回该类加载器的超类加载器                                   |
| loadClass（String name）                              | 加载名称为name的类，返回结果为java.lang.Class类的实例        |
| findClass(String name)                                | 查找名称为name的类，返回结果为java.lang.Class类的实例        |
| findLoadedClass（String name）                        | 查找名称为name的已经被加载过的类，返回结果为java.lang.Class类的实例 |
| defineClass（String name，byte[] b,int off, int len） | 把字节数组b中的内容转换为一个java类，返回结果为java.lang.Class类的实例 |
| resolveClass(Class<?> c)                              | 链接指定的一个java类                                         |

### 获取ClassLoader的途径：

`获取当前类的ClassLoader`

```java
clazz.getClassLoader()
```

`获取当前线程上下文的ClassLoader`

```java
Thread.currentThread().getContextClassLoader()
```

`获取系统的ClassLoader`

```java
ClassLoader.getSystemClassLoader()
```

`获取调用者的ClassLoader`

```java
DriverManager.getCallerClassLoader()
```

## 双亲委派机制：

>java虚拟机对class文件采用的是**按需加载**的方式，也就是说，当需要使用该类时才会将它的class文件加载到内存生成class对象，而且加载某个类的class文件时，java虚拟机采用的是**双亲委派模式，即请求由父类处理**，它是一种任务委派模式。



### 双亲委派工作原理：

1. 如果一个类加载器收到了类加载请求，它并**不会自己先去加载**，而是把这个**请求委托给父类加载器**去执行
2. 如果父类加载器**还存在其父类加载器，则进一步向上委托**，依次递归，请求**最终将到达顶层的启动类加载器**
3. 如果**父类加载器可以完成类加载任务，就成功返回，倘若父类加载器无法完成此加载任务，子加载器才会尝试自己去加载**，这就是双亲委派模式



![image-20200715162943450](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200715162943450.png)



### 双亲委派的优点：

- 避免类的重复加载
- 保护程序安全，防止核心API被随意篡改---沙箱安全机制

### 类的主动与被动使用方式：

`主动使用`

- 创建类的实例
- 访问某个类或接口的静态变量，或者对该静态变量赋值
- 调用类的静态方法
- 反射（Class.forname("com.wy.")）
- 初始化一个类的子类
- java虚拟机启动时被标明为启动类的类
- jdk1.7之后提供动态语言支持：
  - REF_getStatic,REF_putStatic,REF_invokeStatic句柄对应的类没有初始化，则初始化。

`被动使用`

- 除了以上七种情况，其余使用java类的方式都是类得被动使用，不会导致类的初始化。