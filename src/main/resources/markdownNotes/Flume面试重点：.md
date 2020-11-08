## Flume面试重点：

### taildir source特点：

- 断点续传，多目录传输

### taildir source是哪个flume版本产生的？

- apache1.7/ cdh1.6

### 没有断点续传功能时怎么做的？

- 自定义

### taildir挂了怎么办？

不会丢数据：断电续传

### 怎么处理重复数据？

不处理：生产环境通常不处理，因为会影响传输效率

处理的话：

- 在taildirsource里增加自定义事务
- 下一级处理（hive，dwd，sparkstreaming，flink，布隆），去重手段（group by，开窗取第一条，redis）

### taildir source 是否支持递归遍历文件夹读取文件？

不支持，可以自定义，递归遍历文件夹 + 读取文件

### file channel  |  memeory channel  |  kafka channel

1. file channel

   - 数据存储于磁盘，
   - 优势：可靠性高
   - 劣势：传输速度低
   - 默认容量：100万event

   > tips: filechannel 可以通过配置datadirs 指向多个路径，每个路径对应不同的硬盘，增大flume吞吐量。

2. memory channel

   - 数据存储于内存，
   - 劣势：可靠性低
   - 优势：传输速度高
   - 默认容量：100个event

3. kafka channel

   - 数据存储kafka，基于磁盘
   - 优势：可靠性高
   - 传输速度快 kafka channel > memory channel + kafka sink 原因省去了sink阶段

### Flume拦截器自定义步骤：

1. 实现Interceptor
2. 重写四个方法
   - `initialize` 初始化
   - `public Event intercept(Event event)` 处理单个Event
   - `public List<Event> intercept(List<Event> events)`处理多个Event，在这个方法中调用 Event `intercept(Event event)`
   - `close`方法
3. 静态内部类：实现Interceptor.Builder

### Flume Channel选择器

![image-20200819195222005](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200819195222005.png)

> Channel Selectors ,可以让不同的项目日志通过不同的Channel到不同的Sink中去，官方文档上Channel Selectors 有两种类型： Replicating Channel Selector 和Multiplexing Channel Selector

这两个Selector区别是：Replicating会将source过来的events发往所有channel，而Multiplexing可以选择法网哪些Channel。

### Flume采集数据会丢失吗？

- filechannel不会，channel存储可以存储在fiel中，数据传输自身有事务
- memeoryChannel有可能会丢