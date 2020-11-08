# kafka两大关注点：

## Kafka怎么保证数据可靠？

> 往两大方向考虑问题：

### 一：如何保证数据不丢失？

#### 1）：副本同步机制：

![image-20200818104859904](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200818104859904.png)

> kafka的partition为主从结构，在一个partition里，存在leader和follower，当数据发送给leader后，需要确保follower和leader数据同步后才发送给producer一个ack

##### 副本同步实现-ISR副本同步队列：

> ISR（In-Sync Replicas），副本同步队列。
>
> ISR中包括leader和follower，如果leader挂掉，ISR队列会选择一个服务作为新的leader
>
> 有replica.lag.max.messages（延迟条数）和replica.lag.time.max.ms（延迟时间）两个参**数决定一台服务是否可以加入ISR副本队列**，0.10后把延迟条数删除防止服务频繁得进去队列。
>
> **任意一个维度超过阈值都会把 Follower 剔除出 ISR** ，存入 OSR（Outof-Sync Replicas）列表，新加入的 Follower 也会先存放在 OSR 中。 

##### 为什么同步全部的副本数据：

- kafka由于会存放大量数据，不会去选择半数存活机制，半数会造成大量数据冗余。
- 因为都是部署在一个机架上的，所以网络延迟对kafka影响比较小

![image-20200818112804748](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200818112804748.png)

#### 2）：ack应答机制：

- `ack参数等级`
  - 0：producer不等待broker的ack，broker已接受到还没写入磁盘就返回成功，可能会造成数据丢失
  - 1：producer等待broker的ack，partition的leader落盘成功返回ack，**follower同步成功之前leader故障，数据可能会丢失**
  - -1（all）：leader和follower全部落盘成功才返回ack**，当follow同步完成之后，leader挂了，producer又发了一次写入broker请求，结果在另外一个leader又写了一次，造成数据重复**



#### 3）：故障时副本一致性问题解决

> **LEO（log-end-offset）**：每个副本的最后一个offset 

> **HW（high watemark）**：所有副本中最小的LEO

- follower故障：

> follower会被踢出ISR，follower读取本地磁盘的记录得HW，高于log文件得全部删掉，从HW开始进行向leader同步
>
> 等该 follower 的 LEO 大于等于该 Partition 的 HW，即 follower 追上 leader 之后，就可以重新 加入 ISR 了。 

- leader故障：

> leader发生故障后，从ISR中选出一个新的leader之后，，之后，为保证多个副本之间的 数据一致性，其余的 follower 会先将各自的 log 文件高于 HW 的部分截掉，然后从新的 leader同步数据。
>
> 只能保证副本得数据一致性

### 二：如何保证数据不重复？

#### 幂等性机制：

>  开启幂等性的 Producer 在初始化的时候会被分配一个 PID，发往同一 Partition 的消息会附带 SequenceNumber。而 Broker 端会对<PID,Partition,SeqNumber>做缓存，当具有相同主键的消息提交时，Broker 只会持久化一条。
> 但是 PID 重启就会变化，同时不同的 Partition 也具有不同主键，所以幂等性无法保证跨 分区跨会话的 ExactlyOnce

#### 实现exactly once：

> 保证每条信息被发送且仅被发送一次

0.11后，kafka引入`幂等性机制`（dempotent）（实例化一次机制），配合acks = -1时得at least once语义（会重复不丢失），完成了exactly once

> 只需将enable.idempotence属性设置为true，kafka自动将acks属性设为-1

### 



## kafka怎么完成数据高速读写？                                              

> kafka会把收到的消息都写入到硬盘中，他绝对不会丢失数据，为了优化写入速度kafka采用了两个技术，顺序写入和MMFile（Memory Mapped File）

### 一：顺序写入：

#### Kafka选择顺序写入磁盘：

有人一看到写入磁盘，就认为一定比内存慢，其实不然

- **磁盘顺序写入速度是超过内存的随机读写的**
- 写入磁盘同时避免了JVM的GC效率低，内存占用大
- 系统冷启动后，磁盘缓存依然可用。

#### 如何顺序写入？

在kafka每个partition都是一个文件，收到消息后kafka会把数据插入到文件末尾

![image-20200818085538993](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200818085538993.png)

这个办法无法删除数据，所以kafka本身会把所有数据保留下来，

所以每个consumer对每个topic都有一个offset来表示读取到了第几条数据。

### 二：zero-copy

> 零拷贝不是指0次复制，而是指0次调用CPU消耗资源

> 零拷贝技术基于DMA实现（Direct Memory Access），也就是让硬件跳过CPU调度，直接访问主内存。

#### 前提：kafka主要对数据的操作为读和写，不对数据修改

![image-20200818095925183](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200818095925183.png)

**因此先以read读操作为例：**

- 当我们作为应用程序读取read（）操作数据时，底层会**采用一次DMA技术读取磁盘文件**存储到内核空间的**读取缓存区**，供应用程序读取。
- 可读取缓存区**属于内核空间**，所以我们应用程序利用**cpu进行一次上下文切换（用户态-> 内核态->用户态）**，获取读取内核空间缓存区的数据，将readbuffer数据读取到用户缓存区，回到用户程序后然后继续操纵数据。发生了**2次copy，一次cpu调用**

**再以send写操作为例：**

- 我们最终目的是将文件发送到另外一个服务里，所以需要调用socket进行通信传输，此时我们们应用程序再次利用**cpu进行一次上下文切换（用户态-> 内核态->用户态）**，将用户态缓冲区的文件数据，copy到**内核空间的socket buffer里**，socket再通过**DMA技术将数据**从目标**套接字相关的缓存区**传到相关的协议引擎进行发送。应用程序执行完回到用户态，**发生了2次copy，一次cpu调用**。

#### 零拷贝优化实现0次调用cpu

上述进行了2次cpu调用，我们发现其实不对数据本身进行修改的话，一切都可以在内核空间操作，不需要通过用户空间也能完成read+send

> 此时的优化需要底层网络接口支持收集操作

- 在linux2.4及后版本，socketbuffer描述符做了相应调整，使DMA自带收集功能，对于用户来说，调用两个方法合并成transferTo（）方法，且内部的流程已然改变。

![image-20200818095910433](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200818095910433.png)

- transferTo（）方法英发DMA将文件内容复制到内核读取缓冲区
- 将数据位置和长度信息的描述符追加到socket buffer，避免了内容整体copy，DMA 引擎直接把数据从内核缓冲区传到协议引擎，全程都是DMA参与，从而消除CPU参与的数据复制消耗





以kafka为例，如果有100个消费者消费一份数据，在普通的数据传输方式下，**复制次数一共是100\*4 = 400次，cpu调用次数一共是100\*2 = 200次**；而使用了零拷贝技术之后，复制次数一共是100+1 = 101次（1次数据从磁盘到内核读取缓冲区，100次发送给100个消费者消费），cpu调用次数一共是0次。极大的提高了数据读写效率。

### 三：Memory Mapped Files

即便是顺序写入硬盘，硬盘的访问速度还是不可能追上内存。所以Kafka的数据并 不是实时的写入硬盘 ，它充分利用了现代操作系统 分页存储 来利用内存提高I/O效率。

Memory Mapped Files(后面简称mmap)也被翻译成 内存映射文件 ，在64位操作系统中一般可以表示20G的数据文件，它的工作原理是直接利用操作系统的Page来实现文件到物理内存的直接映射。完成映射之后你对物理内存的操作会被同步到硬盘上（操作系统在适当的时候）。

通过mmap，进程像读写硬盘一样读写内存（当然是虚拟机内存），也不必关心内存的大小有虚拟内存为我们兜底。

使用这种方式可以获取很大的I/O提升， 省去了用户空间到内核空间 复制的开销（调用文件的read会把数据先放到内核空间的内存中，然后再复制到用户空间的内存中。）也有一个很明显的缺陷——不可靠， 写到mmap中的数据并没有被真正的写到硬盘，操作系统会在程序主动调用flush的时候才把数据真正的写到硬盘。 Kafka提供了一个参数——producer.type来控制是不是主动flush，如果Kafka写入到mmap之后就立即flush然后再返回Producer叫 同步 (sync)；写入mmap之后立即返回Producer不调用flush叫 异步 (async)。

### 四：批量压缩

>  在很多情况下，系统的瓶颈不是CPU或磁盘，而是网络IO，对于需要在广域网上的数据中心之间发送消息的数据流水线尤其如此。进行数据压缩会消耗少量的CPU资源,不过对于kafka而言,网络IO更应该需要考虑。

- 如果每个消息都压缩，但是压缩率相对很低，所以Kafka使用了批量压缩，即将多个消息一起压缩而不是单个消息压缩
- Kafka允许使用递归的消息集合，批量的消息可以通过压缩的形式传输并且在日志中也可以保持压缩格式，直到被消费者解压缩
- Kafka支持多种压缩协议，包括Gzip和Snappy压缩协议

### 总结：

- mmap优化了I/O速度
- 顺序写入优化了写入速度
- 批量压缩优化网络I/O速率
- 零拷贝优化了cpu执行效率，减少了copy次数