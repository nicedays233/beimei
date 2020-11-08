## Flink

- DataSetAPI：对静态数据进行批处理操作，将静态数据抽象成分布式的数据集，支持java，scala，python
- DataStreamAPI：对静态数据进行流处理操作，将流式的数据抽象成分布式的数据流，支持java，scala
- TableAPI：对结构化数据进行查询操作，将结构化抽象成关系表

### SparkStreaming和flink之间的区别

- sparkstreaming会依次创建DstreamGraph，JobGenerator，JobScheduler。flink则是通过代码生成streamgrapph，优化成jobGraph,然后提交给jobmanager进行处理，jobManager会根据executionGraph对job进行调度。
- sparkstreaming仅支持处理时间，flink支持处理时间，事件时间，注入时间，支持watermark机制处理滞后数据。
- 容错机制对sparkstreaming设置checkpoint点，flink通过两阶段提交协议来解决这个问题。
- 