## HBase安装：

### 第一步：上传linux

- 将tar包放到/opt目录下进行解压

```shell
tar -zxf hbase-1.2.0-cdh5.14.2.tar.gz 
mv hbase-1.2.0-cdh5.14.2 soft/hbase120
```

### 第二步：修改配置文件

- 进入hbase的conf目录下

  

```shell
cd soft/hbase120/conf/
vi hbase-site.xml
```

`修改hbase-site.xml`

```xml
<!--hbase.rootdir 将数据写入哪个目录 如果是单机版只要配置此属性就可以，value中file:/绝
对路径，如果是分布式则配置与hadoop的core-site.sh服务器、端口以及zookeeper中事先创建的目录一致-->
<property>
	<name>hbase.rootdir</name>
  <value>hdfs://192.168.56.101:9000/opt/soft/hbase120/rootdir</value>
</property>

<!--单机模式不需要配置，分布式配置此项为true-->
<property>
	<name>hbase.cluster.distributed</name>
	<value>true</value>
</property>

 <!--单机模式不需要配置 分布是配置此项为zookeeper指定的物理路径名-->
<property>               									 <name>hbase.zookeeper.property.dataDir</name>
	<value>/opt/soft/zk345/tmp</value>
</property>

```

此处为zookeeper的dataDir物理路径，去寻找zookeeper的配置文件看看是否与其一致

```shell
cd soft/hbase120/conf/
vi hbase-env.sh
```

`修改hbase-env.sh文件`

```sh
# 修改两处配置文件的出处
export JAVA_HOME=/opt/soft2/jdk180/jdk1.8.0_111
export HBASE_MANAGES_ZK=false
```

![image-20200619172453552](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200619172453552.png)

![image-20200619172512687](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200619172512687.png)



`配置环境`

```shell
vi /etc/profile
```

> 在末尾添加如下内容
> 注意路径与自己的保持一致

```shell
export HBASE_HOME=/opt/soft/hbase120
export PATH=$PATH:$HBASE_HOME/bin
```

- 退出保存，并激活 

```shell
source /etc/profile
```



### 第三步：启动HBase

**启动顺序 ：hadoop -> zookeeper -> hbase**

> start-all.sh
>
> zkServer.sh start
>
> start-hbase.sh

```shell
# 查看进程是否都已启动
[root@niceday bin]# jps
5458 Jps
3939 ResourceManager
3477 NameNode
4053 NodeManager
3607 DataNode
5003 HMaster
3774 SecondaryNameNode
4814 QuorumPeerMain
5150 HRegionServer
```


`命令行工具启动 : hbase shell`

![image-20200624014342245](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200624014342245.png)

看到此界面即为成功登入

### 第四步：去zk查看root表

- 启动zk

```shell
zkCli.sh 
```

- 查看是否有hbase注册

![image-20200721092920266](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200721092920266.png)

- 查看hbase-meta表位置

>找到 hbase:meta 表的位置，hbase:meta 是 hbase 当中一张表，肯定由一个
>HRegionServer 来 管 理 ， 其 实 主 要 就 是 要 通 过 ZooKeeper 的
>“/hbase/meta-region-server”获取存储“hbase:meta”表的 HRegionServer 的地
>址

```shell
get /hbase/meta-region-server
```

