- ElasticSearch(存储+检索+分析)
- logstash(日志收集)----
- Kibana(可视化)

1条日志---------1KB

1GB数据--------100万数据

###  log4j产生日志

##### 配置文件信息:

```java
# 输出debug级--日志级别
log4j.rootLogger=debug,appender1

# 输出到控制台--日志目的地--appender追加（默认追加模式）
log4j.appender.appender1=org.apache.log4j.ConsoleAppender

# 采用是什么样的格式--日志格局--PatternLayout（灵活指定布局模式）
log4j.appender.appender1.layout=org.apache.log4j.PatternLayout

# 日志输出什么样的内容--日志内容
log4j.appender.appender1.layout.ConversionPattern =%r[%t] [%p] -%c-%l-%m%n
```

- **日志内容格式**:

  1. %p --priority--输出优先级，即 DEBUG ， INFO ， WARN ， ERROR ， FATAL
  2. %r 输出自应用启动到输出该 log 信息耗费的毫秒数 
  3. %c --class--输出所属的类目，通常就是所在类的全名 
  4. %t --time--输出产生该日志事件的线程名 
  5. %n 输出一个回车换行符， Windows 平台为 “rn” ， Unix 平台为 “n”
  6. *%d* --date--输出日志时间点的日期或时间，默认格式为 *ISO8601* 
     - yyyy-MM-dd HH:mm:ss
  7. %L: --line--输出代码中的行号
  8. %m --message--输出代码中指定的消息

  ##### 按日期生成日志文件

  