## Hadoop高可用集群环境搭建：

> standby的通过journalnode来将active的namenode信息同步到standby的namenode上

`前提：Hadoop完全分布式和zookeeper完全分布式已搭建完成`

### 一：配置HDFS-HA集群：

#### 第一步：在第一台主机器上配置core-site.xml

```xml
<configuration> 
<!-- 把两个 NameNode）的地址组装成一个集群 mycluster--> 
    <property> 
        <name>fs.defaultFS</name> 					
        <value>hdfs://mycluster</value> 
    </property>
<!-- 指定 hadoop 运行时产生文件的存储目录 --> 
    <property> 
        <name>hadoop.tmp.dir</name> 
        <value>/opt/install/hadoop/data/tmp</value> 
    </property>
</configuration>
```

#### 第二步：在第一台主机器上配置hdfs-site.xml

```xml
<configuration> 
    <!-- 完全分布式集群名称 -->
    <property>
        <name>dfs.nameservices</name> 		      
        <value>mycluster</value> 
    </property>
<!-- 集群中 NameNode 节点都有哪些,这里是 nn1 和 nn2--> 
    <property>
        <name>dfs.ha.namenodes.mycluster</name> 
        <value>nn1,nn2</value>
        </property>
<!-- nn1 的 RPC 通信地址 --> 
    <property> 
        <name>dfs.namenode.rpc-address.mycluster.nn1</name> 
        <value>hadoop102:9000</value> </property>
<!-- nn2 的 RPC 通信地址 -->
    <property> 
        <name>dfs.namenode.rpc-address.mycluster.nn2</name> 
        <value>hadoop103:9000</value>
    </property>
<!-- nn1 的 http 通信地址 --> 
    <property> 
        <name>dfs.namenode.http-address.mycluster.nn1</name> 
        <value>hadoop102:50070</value> 
    </property>
<!-- nn2 的 http 通信地址 --> 
    <property> 
        <name>dfs.namenode.http-address.mycluster.nn2</name> 
        <value>hadoop103:50070</value> 
    </property>
<!-- 指定 NameNode 元数据在 JournalNode 上的存放位置 --> 
    <property>
        <name>dfs.namenode.shared.edits.dir</name>     <value>qjournal://hadoop102:8485;hadoop103:8485;hadoop104:8485/mycluster</value> 
    </property>
<!-- 配置隔离机制，即同一时刻只能有一台服务器对外响应 --> 
    <property>
        <name>dfs.ha.fencing.methods</name> 
        <value>sshfence</value> 
    </property>
<!-- 使用隔离机制时需要 ssh 无秘钥登录--> 
    <property>
        <name>dfs.ha.fencing.ssh.private-key-files</name>
        <value>/root/.ssh/id_rsa</value>
    </property>
<!-- 声明 journalnode 服务器存储目录--> 
    <property> 
        <name>dfs.journalnode.edits.dir</name> 
        <value>/opt/soft/hadoop260/data/jn</value> 
    </property>
<!-- 关闭权限检查--> 
    <property> 
        <name>dfs.permissions.enable</name> 
        <value>false</value> 
    </property>
<!-- 访问代理类：client，mycluster，active 配置失败自动切换实现方 式--> 
    <property> 
 	<name>dfs.client.failover.proxy.provider.mycluster</name> 
<value>org.apache.hadoop.hdfs.server.namenode.ha.ConfiguredFailoverProxyProvider</value>
    </property> 
</configuration>
```

拷贝配置好的xml文件（hadoop环境）拷贝到其他节点的对应位置。

### 二：启动HDFS-HA集群：

#### 第一步：在各个节点上，都启动journalnode服务：

```shell
hadoop-daemon.sh start journalnode
```

#### 第二步：在第一台主节点上，对其格式化，并启动：

> 若已配置过完全分布式的机器，之前对namenode格式化过一次，所以要将/opt/soft/hadoop260/tmp/dfs/data，将data文件夹删除。
>
> 因为格式化会重置datanode的ID，多次格式化datanode可能id会不一样导致datanode起不来

```shell
hdfs namenode-format
hadoop-daemon.sh start namenode
```

#### 第三步：在第二台standby辅节点上同步主节点元数据信息：

```shell
hdfs namenode -bootstrapStandby
```

#### 第四步：启动standby的namenode节点：

```shell
hadoop-damemon.sh start namenode
```

#### 第五步：所有节点启动datanode

```shell
hadoop-daemons.sh start datanode
```



### 三：配置HDFS-HA自动故障转移：



#### 第一步：在每个节点上增加配置文件的信息：

`hdfs-site.xml`

```xml
<property> 
    <name>dfs.ha.automatic-failover.enabled</name> 
    <value>true</value> 
</property> 
```

`core-site.xml`

```xml
<property>
    <name>ha.zookeeper.quorum</name> 
  <value>hadoop102:2181,hadoop103:2181,hadoop104:2181</value> 
</property> 
```



####  验证自动故障active不转移出错解决方法：
**方法一：** 将hdfs-site.xml其中一个改成如下形式

```xml
<property> 
    <name>dfs.ha.fencing.methods</name> 
    <value>
    sshfence
    shell(/bin/true)
    </value> 
</property>
```
**方法二：**  安装下面这个插件

```shell
yum install psmisc 
```

一台机器改完分发到其他机器上

#### 第二步：启动zookeeper集群：

```shell
zkServer.sh start
```

#### 第三步：初始化HA在zookeeper中的状态：

```shell
hdfs zkfc -formatZK
```

#### 第四步：启动HDFS服务：

> 哪个机器的Failover Controller进程先启动，哪个机器就是active namenode

```shell
hdfs zkfc-formatZK
```



### 四：YARN-HA配置:

#### 第一步：修改yarn-site.xml配置

```xml
<configuration>
	<property>
        <name>yarn.nodemanager.aux-services</name> 		
        <value>mapreduce_shuffle</value> 
    </property>
<!--启用 resourcemanagerha--> 
    <property>
        <name>yarn.resourcemanager.ha.enabled</name>
        <value>true</value> 
    </property>
<!--声明两台 resourcemanager 的地址--> 
    <property> 
        <name>yarn.resourcemanager.cluster-id</name> 
        <value>cluster-yarn1</value> 
    </property>

    <property> 
        <name>yarn.resourcemanager.ha.rm-ids</name> 
        <value>rm1,rm2</value> 
    </property>

    <property> 
        <name>yarn.resourcemanager.hostname.rm1</name> 
        <value>niceday2</value></value> 
    </property>

    <property> 
        <name>yarn.resourcemanager.hostname.rm2</name> 
        <value>niceday3</value> 
    </property>
<!--指定 zookeeper 集群的地址--> 
    <property> 
        <name>yarn.resourcemanager.zk-address</name><value>niceday2:2181,niceday3:2181,niceday4:2181</value> 
    </property>
<!--启用自动恢复--> 
    <property> 
        <name>yarn.resourcemanager.recovery.enabled</name> 
        <value>true</value> </property>
<!--指定 resourcemanager 的状态信息存储在 zookeeper 集群--> 
    <property> 
        <name>yarn.resourcemanager.store.class</name> <value>org.apache.hadoop.yarn.server.resourcemanager.recovery.Z KRMStateStore</value>
    </property>
</configuration>
```

并将修改的配置文件分发到其他机器上：

#### 第二步：启动active的namenode的RM

```shell
start-yarn.sh
```

#### 第三步：启动standby的namenode的RM

```shell
yarn-daemon.sh start resourcemanager
```

#### 第四步：查看两台机器的RM的状态

```shell
yarn rmadmin -getServiceState rm1
yarn rmadmin -getServiceState rm2
```



> 全部完成后，每个机器start-all.sh,把剩余的nodemanager也全部全部启动，最终三台机器的所有进程如下图所示，

则搭建成功hadoop高可用集群。

![image-20200706154731413](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200706154731413.png)

![image-20200706171901488](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200706171901488.png)



---

之后重启机器时，再按以下顺序启动hadoop环境

`启动journalnode`

```shell
hadoop-daemon.sh start journalnode
```

`主节点启动namenode`

```shell
hadoop-daemon.sh start namenode
```

`辅节点同步主节点信息，并启动辅节点`

```shell
hdfs namenode -bootstrapStandby
hadoop-daemon.sh start namenode
```

`各个节点启动datanode`

```shell
hadoop-daemon.sh start datanode
```

`各个节点启动zookeeper`

```shell
zkServer.sh start
```

`初始化HA在zookeeper中状态`

```shell
hdfs zkfc -formatZK
```

`启动HDFS服务`

```shell
start-dfs.sh
```

`在主节点启动yarn服务`

```shell
start-yarn.sh
```

`在辅节点也启动yarn服务`

```shell
start-yarn.sh
```

![image-20200706194710418](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200706194710418.png)