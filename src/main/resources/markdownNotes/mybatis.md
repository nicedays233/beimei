## Mybatis

### 概念：半自动化的ORM框架

- 半自动化：sql命令自定义，参数动态传入

```java
final String sql = "select * from table where field=?";
// 然后自动化完成参数的注入
// 是用pojo：（java的普通实体对象）自动完成参数映射
```

hibernate：是一个全自动化框架

- ORM： Object relational mapping：对象关系映射

将pojo（java实体对象）：Mysql  数据行（实体）--元组

### 使用操作：

1. 2种核心的配置文件

   - configuration

   - Mapper配置

     1. 注解配置方式：针对简单的sql命令

        1. @Select

        ```java
        @Select("select * from shirt_brands")
        	List<ShirtBrands> findAll();
        ```

        1. @Insert
        2. @Update
        3. @Delete

     2. XML文件配置：针对复杂的sql命令

        - mybatis**重要特性**:动态SQL

        - 动态sql需要独立的配置文件

          1. 路径：可以写在mapper包内，但不推荐

          2. xml作为静态资源存在resources下同路径（如下图）

          3. 操作节点

             - <insert id=""mapper接口中的方法名称>

               ​	sql命令

               </insert 结尾>

             - <delete id=""mapper接口中的方法名称>

               ​	sql命令

               </delete 结尾>

          4. 循环标签

             <foreach collection="list/array/map接口参数的类型" item="obj in collection" open="表达式开始符号" seperator="每两项之间的分隔符" close="表达式的结束符号" index="索引（0-N）">

             ....

             </foreach>

          5. set标签会自动去除最后一个'，'

          6. where 标签会自动去除第一个’and‘

          7. if标签可以判断属性的值是否为空，所有实体类属性写成引用类型，这样判断标准一致：null != 属性名称

          8. choose>when..when...othwerwise  多重分支
          
          9. resultmap:修正实体类的属性和数据库表字段的 名称/类型不一致
          
             automapping 设置为false时,mybatis在数据映射时，只考虑resultmap中设置的字段
          
             

![image-20200427161306773](C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\image-20200427161306773.png)

![image-20200427161405061](C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\image-20200427161405061.png)



2.2种配置文件的传参方式：

1. 3个核心对象
   - SqlSessionFactory 数据库会话工厂

```java
InputStream is = Resources.getResourcesAsStream("mybatis.xml");
SqlSessionFactory factory = new SqlSessionFactoryBuilder().build(is);
SqlSession session = factory.openSession(true);
```



- SqlSession 数据库会话对象

```java
UserMapper mapper = session.getMapper(UserMapper.class);// UserMapper为接口
```

3。myBatis中mapper接口的参数非实体类类型，如果只有一个参数，可以自动识别，多个参数无法识别参数名称，需要用到注解的方式@Param（"paramName"）

4.mybatis 中接口的入参规则和java一致，参数类别<=3直接入参，>3则封装，类型相同过多用集合

**5.事务处理**

1. **MySQL Transaction**

   - **原子性：**不可拆分

   - **一致性：**事务前后数据一致性

     经典案例：转账

   - **隔离性：**不同的事务之间是相互独立的

   - **持久性：**

     rollback 回滚

     commit   提交

2. **事务隔离级别**

   - 脏读：是指一个事务中访问到了另外一个事务未提交的数据
   - 不可重复读：是指在一个事务内根据同一个条件对行记录进行多次查询，但是搜出来的结果却不一致
   - 幻读：是指同一个事务内多次查询返回的结果集不一样（比如增加了或者减少了行记录）
   - PS:不同在于不可重复读是同一个记录的数据内容被修改了，幻读是数据行记录变多了或者少了
   
   

```java
SqlSession session = fa.openSession(TransactionIsolationLevel.READ_COMMITTED);
```



```java
// 开启事务必须关闭自动提交, 并选择事务隔离级别
// 级别从低到高
// TransactionIsolationLevel.NONE
// TransactionIsolationLevel.READ_UNCOMMITTED
// TransactionIsolationLevel.REPEATABLE_READ
// TransactionIsolationLevel.READ_COMMITTED
// TransactionIsolationLevel.SERIALIZABLE
```



### 特点：

1.半自动化的ORM实现

2.dao层

3.动态SQL

4.小巧灵活，简单易学

**持久化：数据程序在瞬时状态（内存）和持久状态（硬盘）间转换的过程**

### ORM：对象关系映射（）Object relational mapping

编写程序：把关系型数据库的数据以面向对象的方式处理数据

保存数据：把对象拆成以关系型数据库的方式存储数据

### 优点：

1.与JDBC相比，减少50%的代码量

2.SQL代码从程序代码中彻底分离，可重用

3.提供XML标签，支持编写动态SQL

4.提供XML标签，支持对象与数据库的ORM字段关系映射

### 缺点：

1.SQL语句编写依然需要自己来完成，如果业务逻辑在sql上很麻烦

2.优化体现在sql上，对开发人员有一定要求

3.数据库移植性差

**mybatis专注sql，足够灵活的dao层解决方案，用于性能要求较高，需求多变的项目**

