## HBase调优：

### Region管理：

- `Region拆分`
  - 当一个Region大到一定程度，会进行（split）
  - HBase可以通用Region Split 达到负载均衡
- `Region合并`
  - 如果删除了大量数据，很多region变小，这个时候region多个就会很浪费

### Region拆分：

#### 自动拆分：

- constantSizeRegionSplitPolicy
- IncreasingToUpperBoundRegionSplitPolicy（默认）

>Math.min(tableRegionCounts ^ 3 * initialSize,defaultRegionMaxFileSize)

```shell
tableRegionCounts 就是字面意思
initialSize 默认为memstore2倍
defaultRegionMaxFileSize ：region最大大小。默认10G
假设只有一个region，memstore是128M，10g
min(1 ^ 3 * 2 * 128, 10G) = 256M
也就是当达到256M时，就会拆分
同理2个region时，当每个region达到2G时会拆分
3个region时，当每个region达到6.75G时会拆分
4个region时，当每个region达到10G时会拆分
4个往上就都是10G
```

#### 手动选择拆分算法预拆分：

```shell
# HexStringSpli 以16进制分割得算法
# -c是个数 -f为列簇名
hbase org.apache.hadoop.hbase.util.RegionSplitter my_split_table HexStringSplit -c 10 -f mycf
```

 hbase shell查看或者网页查看

```shell
scan 'hbase:meta', {STARTROW=> 'my_split_table', LIMIT=>10}
192.168.56.101：60010
```

`HexStringSpit拆分算法：`

>HexStringSplit 把数据从“00000000”到“FFFFFFFF”之间的数据长度按照 n 等分之后算出每一段的起始 rowkey 和结束 rowkey，以此作为拆分点。

`UniformSplit拆分算法：`

>UniformSplit 有点像 HexStringSplit 的 byte 版，不管传参还是 n，唯一不一样
>的 是 起 始 和 结 束 不 是 String ， 而 是 byte[] 。起始 rowkey 是ArrayUtils.EMPTY_BYTE_ARRAY。结束rowkey是new byte[] {xFF, xFF, xFF, xFF, xFF, xFF, xFF, xFF}。最后调用 Bytes.split 方法把起始 rowkey 到结束 rowkey 之间的长度 n 等分，然后取每一段的起始和结束作为拆分点。默认的拆分点算法就这两个。还可以通过实现 SplitAlgorithm 接口实现自己的拆分算法。或者干脆手动定出拆分点.

#### 手动指定拆分点预拆分：

```shell
create 'test_split2' ,'mycf2',SPLITS=>['aaa','bbb','ccc','ddd']
# split_file文件里写aaa,bbb,ccc,ddd
create 'test_split2' ,'mycf2',SPLITS_FilE=>'/opt/xxx.txt'
```

#### 对指定region进行强制拆分：

![image-20200721114415122](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200721114415122.png)

```shell
# 指定id进行拆分
split 'ac0b0532f5daedb5d021f0175be7c51f.'
```



### Region合并：

#### Log-Structured Merge（LSM）

- 区别于传统·数据库得更新现有数据
- 使用类似日志结构合并LSM得方式
- 只需要将值写到log末尾然后进行排序
- 优点：插入和更新数据非常快
- 缺点：占用更多空间

| 传统数据库·            | LSM系统                           |
| ---------------------- | --------------------------------- |
| 更新现有数据，随机读写 | 只需要将值写到log末尾然后进行排序 |

- **Compaction分为Minor和Major两种**
  - `MinorCompaction--事件触发`
    - 将小文件合并成更少得大型文件--假删除
  - `Major Compaction--时间触发`
    - 将一个HStore中的所有文件合并成一个大文件--真正的删除



- **每次触发compact检查时，系统自动决定执行哪一种--3种**
  - 通过 CompactionChecker 线程来定时检查是否需要执行 compaction
    （RegionServer 启动时在 initializeThreads() 中初始化），每隔 10000 秒
    （可配置）检查一次。
  -  每当 RegionServer 发生一次 Memstore flush 操作之后也会进行检查是
    否需要进行 Compaction 操作。
  -  手动触发，执行命令 major_compact 、 compact

![image-20200721115535114](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200721115535114.png)

#### Flush和Compact操作

- flush操作

  ```shell
  flush '表名'
  ```

- compact操作

  ```shell
  #compact一个表的所有regions
  compact 't1'
  #compact某个空闲的region
  compact 'r1'
  #compact一个region的指定列簇
  compact 'r1','c1'
  #compact一个表的指定列簇
  compact 't1','c1'
  ```

#### 为什么需要合并Region?

> 那为什么需要合并Region呢？这个需要从Region的Split来说。当一个Region被不断的写数据，达到Region的Split的阀值时（由属性hbase.hregion.max.filesize来决定，默认是10GB），该Region就会被Split成2个新的Region。随着业务数据量的不断增加，Region不断的执行Split，那么Region的个数也会越来越多。

> 一个业务表的Region越多，在进行读写操作时，或是对该表执行Compaction操作时，此时集群的压力是很大的。这里笔者做过一个线上统计，在一个业务表的Region个数达到9000+时，每次对该表进行Compaction操作时，集群的负载便会加重。而间接的也会影响应用程序的读写，一个表的Region过大，势必整个集群的Region个数也会增加，负载均衡后，每个RegionServer承担的Region个数也会增加。

> 因此，这种情况是很有必要的进行Region合并的。比如，当前Region进行Split的阀值设置为30GB，那么我们可以对小于等于10GB的Region进行一次合并，减少每个业务表的Region，从而降低整个集群的Region，减缓每个RegionServer上的Region压力。

#### 



### 高可用：

### RowKey设计：

- 生成随机，加盐
- hash
- 反转
- 字符串拼接
- 

### 内存优化：

- 70%java堆

### 基础优化：

- hdfs开启追加同步



#### 实时查询的原理：LSM追加