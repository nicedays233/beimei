## Spring

### 一：概念：

- java:JavaSE（Standard）标准，javaEE（Enterprise）企业，JavaME（Mobile）移动

- java EE 的框架，目的：做对象的生命周期管理的容器
- 解耦：耦合度，对象和对象之间的依赖程度
- 通过Spring容器托管所有对象以及对象之间的关系

### 二：功能--特色

- **IOC:**Inversion of Control:控制反转
- 里面需要用到依赖注入，所谓依赖注入，就是对象与对象之间，对象与属性之间的关系需要在对象里进行声明，而我spring直接在配置文件里写的方式注入，或者通过注解的方式自动注入。
- **AOP:**Aspect Oriented Programming：面向切面的编程
- WebMVC：
  - Model（Biz+Dao :数据映射ORM）
  - View(JSP/HTML)
  - Control(Servlet)

### 三：七大核心

1. **spring-core**
2. **spring-context**
3. **spring-aop**
4. **spring-jdbc**
5. **spring-dao**
6. **spring-web**
7. **spring-webmvc**

### 四：依赖

- spring-context 2.5.2

### 五：配置

- bean就是-对象配置

**文件头配置**

![image-20200429141827009](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200429141827009.png)

![image-20200429141848269](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200429141848269.png)

**三种方式给对象赋值**

![image-20200429150121418](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200429150121418.png)

**调用**

![image-20200429150610907](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200429150610907.png)



## spring-mybatis

### 概念：spring和mybatis合作开发的ORM中间件

### 依赖：

- mysql-connector 5.1.38
- mybatis 3.4.6
- spring-context 5.2.2
- spring-jdbc 5.2.2
- mybatis-spring 1.3.2

### 声明式事务：

注解：

@Trsactional(value,rollbackFor,progagation.isolation,readonly)

​	管理器：value                        一般在xml配置文件中统一指定

​	传播：propagation				Progagation.REQUIRED默认也最受欢迎

​	隔离：isolation                      Isolation.DEFAULT默认可以修改

​	只读：readonly                      false默认，true主要针对

​	回滚：rollbackFor                  指定数据回滚规则

​													rollbackFor=SqlException.class



​			

![image-20200429165841523](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200429165841523.png)

