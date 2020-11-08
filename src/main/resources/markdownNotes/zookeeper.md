## ZooKeeper分布式应用协调服务：

### ZooKeeper架构：

>ZooKeeper是一个为分布式应用提供协调服务得apache项目

`Zookeeper = 文件系统 + 通知机制`

- ZooKeeper从设计模式来看是从观察者模式设计得分布式服务管理框架，负责存储和管理大家都关心得数据。
- 一旦数据状态发生变化，注册再zookeeper得观察者会做出相应得反应。

### zookeeper角色：

- leader领导者
  - 负责投票发起和决议，更新系统状态
- follower跟随者
  - 用于接收客户端请求，并向客户端返回结果，选举时参与投票
- observer观察者
  - 可以接收客户端连接，将写请求转发给leader节点，observer不参加投票过程，之同步leader状态。----为了扩展系统，提高读取速度。

### ZooKeeper数据结构：--每个zookeeper节点数据一样

- `znode：`
  - 数据模型类似linux文件系统，每个节点称作一个znode，每个znode默认存1mb数据
- `节点类型`
  - persistent：持久化节点
  - persistent_sequential：持久化顺序编号节点
  - ephemeral：临时节点
  - ephemeral_sequential：临时顺序编号节点

### ZooKeeper选举机制：

- `半数机制：`

  - 集群半数以上机器存活，集群才可用--奇数会比偶数多浪费一台机器

  - zookeeper选举leader时，一般谁上面数据存的是最新得，谁作为leader，如果是刚搭建好得集群，会通过myid最大得来作为leader，但是也不一定，leader如果已经确定了，就不一定是最大得myid最大得作为leader。

    ```shell
    zkServer.sh status # 查看节点状态
    ```

- leader选举机制触发：

  - leader宕机
  - 服务器初始化启动

### ZooKeeper集群搭建：

**第一步：** 解压zookeeper安装包：

```shell
-zxvf zookeeper-3.4.5-cdh5.14.2.tar.gz
```



**第二步：** 到对应配置文件夹下--修改配置文件

```shell

cd /opt/soft/zk345/conf
```

```shell
cp zoo_sample.cfg zoo.cfg
vi zoo.cfg
```

```shell
# The number of milliseconds of each tick心跳次数
tickTime=2000
# The number of ticks that the initial
# synchronization phase can take
initLimit=10
# The number of ticks that can pass between
# sending a request and getting an acknowledgement异步限制
syncLimit=5
# the directory where the snapshot is stored.
# do not use /tmp for storage, /tmp here is just
# example sakes.文件存放
dataDir=/opt/soft/zk345/tmp
# the port at which the clients will connect端口
clientPort=2181
# the maximum number of client connections.
# increase this if you need to handle more clients
#maxClientCnxns=60
#
# Be sure to read the maintenance section of the
# administrator guide before turning on autopurge.
#
# http://zookeeper.apache.org/doc/current/zookeeperAdmin.html#sc_maintenance
#
# The number of snapshots to retain in dataDir
#autopurge.snapRetainCount=3
# Purge task interval in hours
# Set to "0" to disable auto purge feature
#autopurge.purgeInterval=1
# 2287 领导和跟随者之间连接用的，传递信息,
# 3387 领导挂掉，跟随者之间选领导使用
server.1=192.168.56.102:2287:3387
server.2=192.168.56.103:2287:3387
server.3=192.168.56.104:2287:3387

```



修改myid

```shell
vi /opt/soft/zk345/tmp/myid 
# 给myid写上数字
```

启动zk

```shell
# 启动zk
zkServer.sh
```



进入zk客户端

```
zkCli.sh
```

### zookeeper命令

ls

```shell
#　查看节点
ls 目录
```

create

```shell
# 创建nciedya2临时节点
create -e /kgc/niceday2 "niceday2"

# 创建nciedya2有序节点
create -s /kgc/niceday2 "niceday2"

# 创建nciedya2临时有序节点
create -e -s /kgc/niceday2 "niceday2"
```

get

```ｓｈｅｌｌ
# 查看节点
```

set

```shell

```

delete

```shell
delete
rmr 
```

监听节点

```shell
ls /kgc watch
```



节点数据结构：

```shell
cZxid = 0x100000014 # 创建事务id
ctime = Mon Jul 06 09:47:40 CST 2020 # 创建时间
mZxid = 0x100000014 # 修改事务id
mtime = Mon Jul 06 09:47:40 CST 2020 # 修改时间
pZxid = 0x100000014 # 更新id
cversion = 0 # 子节点修改次数
dataVersion = 0 
aclVersion = 0
ephemeralOwner = 0x0 # 这个节点属于谁
dataLength = 10 #数据得长度
numChildren = 0 # 子节点数量
```

