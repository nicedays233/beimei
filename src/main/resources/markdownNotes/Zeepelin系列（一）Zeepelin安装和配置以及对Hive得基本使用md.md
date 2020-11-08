## Zeppelin安装：

### 第一步：上传linux

- 将tar包放到/opt目录下进行解压

```shell
tar -zvxf zeppelin-0.8.1-bin-all.tgz 
mv zeppelin-0.8.1-bin-all /opt/soft/zeppelin081
```

### 第二步：修改配置文件

- 进入conf目录修改

```shell
cd /opt/soft/zeppelin081/conf/
cp zeppelin-site.xml.template zeppelin-site.xml
```

- 修改端口号：默认是8080，为避免冲突，修改为其他端口号

```shell
vi zeppeln-site.xml
```

```xml
<property>
  <name>zeppelin.server.port</name>
  <value>8000</value>
  <description>Server port.</description>
</property>
```

- 添加JAVA_HOME和HADOOP_CONF_DIR  （指定自己的java和hadoop安装目录）

```shell
cp zeppelin-env.sh.template zeppelin-env.sh
vi zeppelin-env.sh
```

```shell
export JAVA_HOME=填写自己的java_home配置路径
export HADOOP_CONF_DIR=填写自己得hadoop得conf配置路径
```

### 第三步：配置hive解释器

>  Zepplin中没有默认的hive解释器，但是我们可以通过jdbc解释器进行添加

`环境和变量配置`

- 拷贝**hive的配置文件**hive-site.xml到zeppelin-0.8.1-bin-all/conf下

```shell
cp /opt/soft/hive110/conf/hive-site.xml /opt/soft/zeppelin-0.8.1-bin-all/conf/
```

- 拷贝jar包，拷贝下面两个jar包到zeppelin安装目录下interperter中。（版本根据自己安装版本来确定

  > hadoop-common-2.6.0.jar
  >
  > hive-jdbc-1.2.1-standalone.jar

```sh
# 这两个jar包在对应得hadoop和hive上拷贝即可
cp /opt/soft/hadoop260/share/hadoop/common/hadoop-common-2.6.0-cdh5.14.2.jar /opt/soft/zeppelin-0.8.1-bin-all/interpreter/jdbc
cp /opt/soft/hive110/lib/hive-jdbc-1.1.0-cdh5.14.2-standalone.jar /opt/soft/zeppelin-0.8.1-bin-all/interpreter/jdbc
```

### 第四步：web界面配置集成Hive

- **进入bin目录下执行 ./zeppelin-daemon.sh start** 
- **输入自己虚拟机的ip加设置得端口号访问zeppelin**

- **右上角anonymous --> interpreter --> +Create新建一个叫做hive的集成环境**

![image-20200616003356815](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200616003356815.png)![image-20200616003409936](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200616003409936.png)

- **设置properties**

  | default.driver | org.apache.hive.jdbc.HiveDriver   |
  | -------------- | --------------------------------- |
  | default.url    | jdbc:hive2://192.168.42.200:10000 |
  | default.user   | 里面如果有值，设置为空            |

  ps：如果之后遇到了权限不允许访问得问题，都是default.user设置了用户，而与自己的虚拟机得用户不匹配导致的。将default.user清空即可。

- **点击保存，并重启restart hive 解释器**

- 在虚拟机后台启动hiveserver2

  ```shell
  hiveserver2
  ```

  

## Zeppelin使用：

### 使用Hive解释器：

- 点击create new note

![image-20200616004804733](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200616004804733.png)

- 选择hive解释器

![image-20200616004950213](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200616004950213.png)

- 输入对应得hive命令完成对虚拟机数据库得远程查询

![image-20200616005111798](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200616005111798.png)

- 可以通过对应得sql语句直接生成图表来显示

![image-20200616005506536](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200616005506536.png)

![image-20200616005549967](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200616005549967.png)