## Spark性能调优：

### 常规调优：

#### 一：最优资源配置：

**标准Spark提交脚本：**

```shell
/usr/opt/spark234/bin/spark-submit \ --class com.wyw.spark.Analysis \ 
--num-executors 80 \ 
--driver-memory 6g \ 
--executor-memory 6g \
--executor-cores 3 \ 
/usr/opt/spark234/jar/spark.jar \
```

**可修改分配资源：**

| **名称**              | **说明**                           |
| --------------------- | ---------------------------------- |
| **--num-executors**   | **配置Executor的数量**             |
| **--driver-memory**   | **配置Driver内存**                 |
| **--executor-memory** | **配置每个Executor的内存大小**     |
| **--executor-cores**  | **配置每个Executor的CPU core数量** |

- `Spark Standalone模式：`提交任务前，从运维部门了解资源可使用情况，15台机器 32g内存 2CPU core，指定15个Executor，每个分配32g，2核心

- `Spark Yarn模式：`由于Yarn使用**资源队列**进行资源的分配和调度，

  比如资源队列有400G内存， 100 个核， 那么指定50个 Executor，每个Executor 分配 8G 内存，2 个核。                  