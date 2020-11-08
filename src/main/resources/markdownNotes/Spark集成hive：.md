## Spark集成hive：

```
 .config("hive.metastore.uris", "thrift://192.168.56.100:9083")
      .config("spark.sql.warehouse.dir", "hdfs://192.168.100.56:9000/user/hive/warehouse")
```

![image-20200909142132937](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200909142132937.png)



### 或者在resource上塞入3个配置文件（spark2.3.4）



#### hive-site.xml

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
	<!-- 在configuration中加入配置 -->
	<property>
		<name>hive.metastore.warehouse.dir</name>
		<value>/opt/soft/hive110/warehouse</value>
	</property>
	<!--元数据是否在本地，hive和mysql是否在一个服务器上 -->
	<property>
		<name>hive.metastore.local</name>
		<value>false</value>
	</property>
	<!-- 如果是远程mysql数据库的话需要在这里写入远程的IP或hosts -->
	<property>
		<name>javax.jdo.option.ConnectionURL</name>
		<value>jdbc:mysql://192.168.56.101:3306/hive?createDatabaseIfNotExist=true&amp;useUnicode=true&amp;characterEncoding=UTF-8</value>
	</property>
	<property>
		<name>javax.jdo.option.ConnectionDriverName</name>
		<value>com.mysql.jdbc.Driver</value>
	</property>
	<property>
		<name>javax.jdo.option.ConnectionUserName</name>
		<value>root</value>
	</property>
	<property>
		<name>javax.jdo.option.ConnectionPassword</name>
		<value>123456</value>
	</property>
	<property>
		<name>hive.server2.authentication</name>
    		<value>NONE</value>
    		<description>
      			Expects one of [nosasl, none, ldap, kerberos, pam, custom].
     			 Client authentication types.
       			 NONE: no authentication check
       			 LDAP: LDAP/AD based authentication
        		KERBEROS: Kerberos/GSSAPI authentication
       			 CUSTOM: Custom authentication provider
                	(Use with property hive.server2.custom.authentication.class)
        		PAM: Pluggable authentication module
       			 NOSASL:  Raw transport
		 </description>
 	 </property>

  	<property>
    		<name>hive.server2.thrift.client.user</name>
    		<value>root</value>
    		<description>Username to use against thrift client</description>
  	</property>
 	 <property>
    		<name>hive.server2.thrift.client.password</name>
    		<value>root</value>
    		<description>Password to use against thrift client</description>
  	</property>
</configuration>

```

