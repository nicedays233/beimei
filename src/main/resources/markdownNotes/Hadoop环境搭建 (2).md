## 环境准备

一个纯净版的centos7 虚拟机，配置好静态ip，主机名，主机映射

### 配置静态ip

```sh
vi /etc/sysconfig/network-scripts/ifcfg-eno16777736 
-----------------------------------------------------
TYPE=Ethernet
BOOTPROTO=none
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
NAME=eno16777736
UUID=f19fae49-46da-4b52-b704-6e1ec4c0470e
ONBOOT=yes
HWADDR=00:0C:29:EC:14:1F
IPADDR0=192.168.191.101
PREFIX0=24
GATEWAY0=192.168.191.2
IPV6_PEERDNS=yes
IPV6_PEERROUTES=yes
DNS1=114.114.114.114
DNS2=8.8.8.8
```

### 配置主机映射

```sh
vi /etc/hosts
-----------------------------------------------------
192.168.191.101 hadoop1
```

### 在/opt下创建两个文件夹，software，install

```sh
cd  /opt
mkdir software install
```

### 免密登陆

```sh
ssh-keygen
#3次回车
#拷贝密钥
ssh-copy-id hadoop1
```

### 安装jdk

```sh
#解压
tar zxvf jdk-8u171-linux-x64.tar.gz -C /opt/install/

#配置环境变量
vi /etc/profile
export JAVA_HOME=/opt/install/jdk1.8.0_171
export PATH=$JAVA_HOME/bin:$PATH
#刷新环境变量
source /etc/profile
#验证
java -version
java version "1.8.0_171"
Java(TM) SE Runtime Environment (build 1.8.0_171-b11)
Java HotSpot(TM) 64-Bit Server VM (build 25.171-b11, mixed mode)
```

## 安装Hadoop

Hadoop 的安装模式分为3种：单机（本地）模式，伪分布式，完全分布式（集群模式）

### 本地模式安装

#### 解压

```sh
tar zxvf hadoop-2.6.0-cdh5.14.2.tar.gz -C /opt/install/
```

#### 环境变量

```
vi /etc/profile
---------------------------
# hadoop
export HADOOP_HOME=/opt/install/hadoop-2.6.0-cdh5.14.2
export PATH=$HADOOP_HOME/bin:$PATH
---------------------------------
source /etc/profile
```

#### 测试

```sh
bin/hadoop
```

#### 官方示例演示

```sh
mkdir input
cp etc/hadoop/*.xml input
bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-2.6.0-cdh5.14.2.jar grep input output 'dfs[a-z.]+'
cat output/*
```

### 伪分布式搭建

#### 修改HDFS配置文件

##### etc/hadoop/hadoop-env.sh

```sh
export JAVA_HOME=/opt/install/jdk1.8.0_171
```

##### etc/hadoop/core-site.xml

```xml
<property>
    <name>fs.defaultFS</name>
    <value>hdfs://hadoop1:9000</value>
</property>
```

##### etc/hadoop/hdfs-site.xml

```xml
<property>
    <name>dfs.replication</name>
    <value>1</value>
</property>
```

##### etc/hadoop/slaves

```
hadoop1
```

#### 格式化文件系统

```sh
bin/hdfs namenode -format
```

#### 启动HDFS

```sh
sbin/start-dfs.sh
```

#### 验证是否成功

```sh
jps
20896 Jps
20787 SecondaryNameNode
20521 NameNode
20638 DataNode
```

使用web浏览器访问50070端口，查看是否能打开

![image-20200629145513595](image-20200629145513595.png)

#### 官方示例演示

```sh
hdfs dfs -mkdir /input
hdfs dfs -put etc/hadoop/*.xml /input
bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-2.6.0-cdh5.14.2.jar grep /input /output 'dfs[a-z.]+'
hdfs dfs -cat /output/part-r-00000
```

#### 修改Yarn配置

mapred-site.xml

```xml
cp etc/hadoop/mapred-site.xml.template etc/hadoop/mapred-site.xml
--------------------------
<property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
</property>
```

yarn-site.xml

```xml
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
</configuration>
```

#### 启动Yarn

```sh
sbin/start-yarn.sh
```

查看jps进程

```sh
jps
22304 ResourceManager
21989 DataNode
22389 NodeManager
21868 NameNode
22143 SecondaryNameNode
22703 Jps
```

使用web浏览器访问8088端口，查看是否能打开

#### 官方示例演示

```sh
hdfs dfs -rm -r -f /output
bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-2.6.0-cdh5.14.2.jar grep /input /output 'dfs[a-z.]+'
hdfs dfs -cat /output/part-r-00000
```

![image-20200629152313082](image-20200629152313082.png)

### 完全分布式

#### 集群准备

1. 准备3台客户机（关闭防火墙、静态ip，主机映射、主机名称），主机名称分别hadoop2，hadoop3，hadoop4

2. 安装jdk，配置环境变量

3. 配置ssh，免密登陆==【拷贝密钥的时候需要拷贝9次】==

4. 配置时间同步

#### 集群规划

|      | hadoop2            | hadoop3                      | hadoop4                     |
| ---- | ------------------ | ---------------------------- | --------------------------- |
| HDFS | NameNode  DataNode | DataNode                     | SecondaryNameNode  DataNode |
| YARN | NodeManager        | ResourceManager  NodeManager | NodeManager                 |

#### 修改配置文件

hadoop-env.sh

```sh
export JAVA_HOME=/opt/install/自己的路径
```

core-site.xml

```xml
	<!-- 指定HDFS中NameNode的地址 -->
	<property>
		<name>fs.defaultFS</name>
        <value>hdfs://hadoop2:9000</value>
	</property>

	<!-- 指定hadoop运行时产生文件的存储目录 -->
	<property>
		<name>hadoop.tmp.dir</name>
		<value>/opt/install/hadoop/data/tmp</value>
	</property>
```

hdfs-site.xml

```xml
	<property>
		<name>dfs.replication</name>
		<value>3</value>
	</property>

	<property>
        <name>dfs.namenode.secondary.http-address</name>
        <value>hadoop4:50090</value>
    </property>
```

yarn-env.sh

```sh
export JAVA_HOME=/opt/install/jdk
```

yarn-site.xml

```xml
	<!-- reducer获取数据的方式 -->
	<property>
		 <name>yarn.nodemanager.aux-services</name>
		 <value>mapreduce_shuffle</value>
	</property>

	<!-- 指定YARN的ResourceManager的地址 -->
	<property>
		<name>yarn.resourcemanager.hostname</name>
		<value>hadoop3</value>
	</property>
```

mapred-site.xml

```xml
	<!-- 指定mr运行在yarn上 -->
	<property>
		<name>mapreduce.framework.name</name>
		<value>yarn</value>
	</property>
```

slaves

```sh
hadoop2
hadoop3
hadoop4
```

集群分发配置文件

#### 启动集群

格式化HDFS

```sh
bin/hdfs namenode -format
```

启动HDFS【hadoop2】

```sh
sbin/start-dfs.sh
```

启动Yarn【hadoop3】

```sh
sbin/start-yarn.sh
```

jps和web页面查看【50070 和 8088端口】

#### 时间同步

安装ntp【hadoop2】

```sh
rpm -qa|grep ntp
yum -y install ntp

vi /etc/ntp.conf
-----------------------
# 修改1（设置本地网络上的主机不受限制。）
#restrict 192.168.1.0 mask 255.255.255.0 nomodify notrap为
restrict 192.168.1.0 mask 255.255.255.0 nomodify notrap
# 修改2（设置为不采用公共的服务器）
server 0.centos.pool.ntp.org iburst
server 1.centos.pool.ntp.org iburst
server 2.centos.pool.ntp.org iburst
server 3.centos.pool.ntp.org iburst为
#server 0.centos.pool.ntp.org iburst
#server 1.centos.pool.ntp.org iburst
#server 2.centos.pool.ntp.org iburst
#server 3.centos.pool.ntp.org iburst
# 添加3（添加默认的一个内部时钟数据，使用它为局域网用户提供服务。）
server 127.127.1.0
fudge 127.127.1.0 stratum 10

```

修改/etc/sysconfig/ntpd

```sh
vim /etc/sysconfig/ntpd
-----------------------
# 增加内容如下（让硬件时间与系统时间一起同步）
SYNC_HWCLOCK=yes
```

重新启动ntpd

```
service ntpd status
service ntpd start
chkconfig ntpd on
```

其他机器配置

```
crontab -e
----------------
*/10 * * * * /usr/sbin/ntpdate hadoop2
```











































