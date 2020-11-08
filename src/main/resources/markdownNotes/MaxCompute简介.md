## MaxCompute简介:

### ODPS概念：

> 大数据计算服务是一种快速，完全托管TB/PB级数据仓库解决方案。

### MaxCompute作用：

- 批量结构化数据的存储和计算
- 提供海量数据仓库和大数据分析建模解决方案

### MaxCompute功能组成：

![image-20200629131408076](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200629131408076.png)

### MaxCompute组件：

`【数据通道】：`

- **Tunnel：**

> **提供高并发的离线数据上传下载服务**

用户可以使用Tunnel服务向MaxCompute批量上传或下载数据。

`【计算及分析任务】：`

- **SQL：**

> MaxCompute以表的形式存储数据,并对外提供SQL查询

PS:  MaxCompute SQL 不支持事务，索引及**Update/Delete** 等操作

- **MapReduce：**

> Google 提出的分布式数据处理模型

  MaxCompute  MapReduce 为 用户提供 Java 编程接口。

- **Graph：**

>MaxCompute 提供的 Graph 功能是一套面向迭代的图计算处理框架。

 图计算作业 使用图进行建模，图由点(Vertex)和边(Edge)组成，点和边包含权值(Value)。通过迭代对图进行编辑、演化，最终求解出结果。

**典型应用：**PageRank，单源最短距离算法 ，K-均值聚类算法 等等。

## MaxCompute基本概念：

### 项目空间：

> Project是MaxCompute的基本组织单元，类似传统RDBMS的database，是进行多用户隔离和访问控制的主要边界。

- 用户可以拥有多个Project
- 可以在一个project中访问另外一个project的对象

```sql
use my_project --进入某个项目空间
```

### 表：

>MaxCompute的存储单元

#### 表格类型：

- **内部表：**

  > 所有数据都被存储在MaxCompute中

- **外部表：**

  > MaxCompute并不真正持有数据，表数据存在OSS中，MC紧急炉元数据信息。

  `处理外部表数据流程`

  1. 将数据上传至OSS
  2. 在RAM产品中授予MaxCompute服务OSS数据权限
  3. 自定义Extractor：用于读取OSS上的特殊格式数据。默认csv
  4. 创建外部表
  5. 执行SQL作业分析数据

  PS：MC仅支持**读外部表**，不支持**写外部表**

### 分区：

> 创建表时指定分区空间--指定表内某几个字段作为分区列。

#### 分区的作用：

- 避免全表扫描，提高处理效率

```sql
create table src(
    keystring,
    value bigint
)
partitionedby(ptstring);
-- 目前，MaxCompute 仅承诺 String类型分区
```



### 任务：

> MaxCompute的基本计算单元

对于用户提交的大多数任务，特别是计算型任务，例如：SQL DML语句，MapReduce等，  **MaxCompute 会对其进行解析，得出任务的执行计划。执行计划是由具有依赖关系的多个执行阶段(Stage)构成的。**

部分MaxCompute任务并不是计算型任务，如SQL中的DDL语句，这些任务本质上仅需要读取，**修改MaxCompute中元数据信息**，这些任务无法解析出执行计划。

### 资源：

MaxCompute特有概念。

>  用户如果想使用 **MaxCompute的 自定义函数(UDF)** 或 **MapReduce 功能**需要依赖资源来完成

MaxCompute 资源类型包括：

1. File类型：
2. Table类型：MaxCompute中的表
3. Jar类型：编译好的java jar包
4. Archive类型：通过资源名称中的后缀识别压缩类型.zip/.tgz/tar.gz/.tar/jar

### 服务连接：

在公网条件下，不同Region的用户均可以通过如两个连接访问MaxCompute：

`service.odps.aliyun.com----MaxCompute服务连接地址`

`dt.odps.aliyun.com----Tunnel服务连接地址`

在经典网络及VPC环境下，不同Region的用户通过如下连接访问服务：

`odps-ext.aliyun-inc.com----MaxCompute服务连接地址`

 ` dt-ext.nu16.odps.aliyun-inc.com 在华北2区访问 Tunnel的连接地址` 

`dt-ext.eu13.odps.aliyun-inc.com 在华东2区访问 Tunnel的连接地址  `

### 大数据计算服务组成架构：

> 客户端---接入层---逻辑层---计算层

![image-20200701090629001](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200701090629001.png)

#### 客户端：

![image-20200701090725162](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200701090725162.png)

ODPS以**RESTful API** 方式对外提供服务，用户可以通过不同的方式来使用ODPS的服务，直接通过**RESTful API**--请求访问，**ODPS SDK**  **ODPS CLT**和 **JAVA集成开发环境**，**管理控制台**，**R语言集成开发环境**,是的用户可以基于自己的IDE开发。



#### 接入层：

![image-20200701093705637](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200701093705637.png)

#### 逻辑层：

![image-20200701093716446](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200701093716446.png)

`请求处理器:Worker`

- 处理所有的RESTful请求
- 本地处理一些作业
- 提交分布式作业给调度器

> **本地能处理的作业：**
>
> ​	-- 用户空间，表，资源，任务等管理
>
> **需要提交给调度器的作业：**
>
> ​	-- SQL，MR等分布式计算的任务

`调度器：Scheduler`

- 负责Instance调度
- 查询计算集群的资源情况

> **Instance调度处理：**
>
> - 维护一个Instance列表
> - 把Instance分解成Task
> - 生成Task的工作流（DAG图）
> - 把可运行Task放到TaskPool中
> - 定时对该优先级队列进行排序

`作业执行管理器：Executor`

- 向TaskPool申请Task
- 生成任务描述文件提交给计算层
- 监控并反馈状态给调度器

> 作业执行器的运行细节：
>
> - 判断自身资源是否充足
> - 主动轮询TaskPool，请求下一个Task
> - 生成计算层的分布式作业描述文件，提交给计算层
> - 监控这些任务的运行状态
> - 定时把状态汇报给调度器

#### 计算层：

![image-20200701094701597](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200701094701597.png)

