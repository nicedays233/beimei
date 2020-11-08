
写在前面：

​	这是一个分布式demo，方便今后搭建分布式项目的时候直接使用。

项目从传统项目着手，逐步改造成高可用的分布式，eureka、ribbon、hystrix、zuul、config 等，浅显的涉及到微服务的拆分，负载均衡，服务降级，路由网关等。

源码地址GitHub：https://github.com/Mujio-killer/mall.git

## 一、传统项目介绍

​		一直想学习一下Spring Cloud，奈何苦于Spring Cloud全家人口众多，不知道该如何入手；再者相关的demo在网上比较难找，特别是从零搭建而且能正常运行的少之又少。本文是参考多篇博文，在实际搭建验证过后写的，主要配置均能够实现对应功能，在此基础上也会去探究其他相关配置，有验证疏漏之处欢迎指出。

主要参考：简书[Felix独箸](https://www.jianshu.com/u/0e5883241140)

------

###### 前期准备：

> 开发环境：win10   jdk1.8   IDEA 2019.1
> 一个传统项目，本文使用spring boot下的商城demo，若已有项目可直接跳到第二节。

###### 工程目录结构：![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326134308274.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

###### pom.xml如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.2.5.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.mujio</groupId>
    <artifactId>mall</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>mall</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>1.8</java.version>
    </properties>

    <dependencies>
        <!-- 添加web服务依赖 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <!-- MySQL数据库依赖 -->
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>5.1.41</version>
        </dependency>
        <!-- mybatis依赖 -->
        <dependency>
            <groupId>org.mybatis.spring.boot</groupId>
            <artifactId>mybatis-spring-boot-starter</artifactId>
            <version>1.1.1</version>
        </dependency>

        <!-- springboot项目需要的依赖，创建项目自动添加 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
            <exclusions>
                <exclusion>
                    <groupId>org.junit.vintage</groupId>
                    <artifactId>junit-vintage-engine</artifactId>
                </exclusion>
            </exclusions>
        </dependency>

    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>

```

###### MallApplication启动类：

```java
package com.mujio.mall;


import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;


@SpringBootApplication
@MapperScan("com.mujio.*.mapper")
public class MallApplication {

    public static void main(String[] args) {
        SpringApplication.run(MallApplication.class, args);
    }

}

```

###### controller包：

```java
package com.mujio.mall.controller;


import com.mujio.mall.entity.Order;
import com.mujio.mall.service.OrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

@RequestMapping("/order")
@RestController
public class OrderController {

    @Autowired
    private OrderService orderService;

    @RequestMapping("/{id}")
    @ResponseBody
    public Order getOrder(@PathVariable("id") int id){
        return orderService.getOrder(id);
    }
}

```

```java
package com.mujio.mall.controller;


import com.mujio.mall.entity.Goods;
import com.mujio.mall.service.GoodService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

@RequestMapping("/goods")
@RestController
public class GoodsController {

    @Autowired
    private GoodService goodService;

    @RequestMapping("/{id}")
    @ResponseBody
    public Goods getGoods(@PathVariable("id") int id){
        return goodService.getGoods(id);
    }

}

```

###### service包：

```java
package com.mujio.mall.service;

import com.mujio.mall.entity.Goods;
import com.mujio.mall.entity.Order;
import com.mujio.mall.mapper.ConnMapper;
import com.mujio.mall.mapper.GoodsMapper;
import com.mujio.mall.mapper.OrderMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class OrderService {

    @Autowired
    private ConnMapper connMapper;

    @Autowired
    private GoodsMapper goodsMapper;

    @Autowired
    private OrderMapper orderMapper;

    public Order getOrder(int id){
        Order order = new Order();
        order.setId(id);
        List<Integer> list = connMapper.getConn(id);
        List<Goods> goodsList = new ArrayList<>();
        for (int goodsid: list ) {
            goodsList.add(goodsMapper.getGoods(goodsid));
        }
        order.setGoodsList(goodsList);
        order.setCreatedate(orderMapper.getOrder(id).getCreatedate());

        return order;
    }

}

```

```java
package com.mujio.mall.service;

import com.mujio.mall.entity.Goods;
import com.mujio.mall.mapper.GoodsMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class GoodService {

    @Autowired
    private GoodsMapper goodsMapper;

    public Goods getGoods(int id){
        return goodsMapper.getGoods(id);
    }
}

```

###### mapper包：

```java
package com.mujio.mall.mapper;


import com.mujio.mall.entity.Order;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface OrderMapper {

    @Select("select * from orders where id = #{id}")
    Order getOrder(int id);
}

```

```java
package com.mujio.mall.mapper;


import com.mujio.mall.entity.Goods;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface GoodsMapper {

    @Select("select * from goods where id = #{id}")
    Goods getGoods(int id);
}
	
```

```java
package com.mujio.mall.mapper;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface ConnMapper {

    @Select("select goodsid from conn where orderid = #{id}")
    List<Integer> getConn(int id);
}

```

###### entity包：

```java
package com.mujio.mall.entity;

import java.util.Date;
import java.util.List;

public class Order {
    private int id;

    private List<Goods> goodsList;

    private Date createdate;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public List<Goods> getGoodsList() {
        return goodsList;
    }

    public void setGoodsList(List<Goods> goodsList) {
        this.goodsList = goodsList;
    }

    public Date getCreatedate() {
        return createdate;
    }

    public void setCreatedate(Date createdate) {
        this.createdate = createdate;
    }


    @Override
    public String toString() {
        return "Order{" +
                "id=" + id +
                ", goodsList=" + goodsList +
                ", createdate=" + createdate +
                '}';
    }
}

```

```java
package com.mujio.mall.entity;

public class Goods {

    private int id;

    private String name;

    private String price;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPrice() {
        return price;
    }

    public void setPrice(String price) {
        this.price = price;
    }

    @Override
    public String toString() {
        return "Goods{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", price='" + price + '\'' +
                '}';
    }
}

```

```java
package com.mujio.mall.entity;

import java.util.List;

public class Conn {
    private int id;

    private int orderid;

    private List goodlist;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getOrderid() {
        return orderid;
    }

    public void setOrderid(int orderid) {
        this.orderid = orderid;
    }

    public List getGoodlist() {
        return goodlist;
    }

    public void setGoodlist(List goodlist) {
        this.goodlist = goodlist;
    }
}

```

###### application.properties配置：

```properties
#服务开放端口配置
server.port=8080

#数据库连接配置
spring.datasource.driver-class-name=com.mysql.jdbc.Driver
spring.datasource.url=jdbc:mysql://localhost:3306/mall?characterEncoding=utf8&useUnicode=true&zeroDateTimeBehavior=convertToNull
spring.datasource.username=root
spring.datasource.password=123

```

###### 数据库：

```sql
/*
Navicat MySQL Data Transfer

Source Server         : mujio
Source Server Version : 50045
Source Host           : localhost:3306
Source Database       : mall

Target Server Type    : MYSQL
Target Server Version : 50045
File Encoding         : 65001

Date: 2020-03-23 14:35:14
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for conn
-- ----------------------------
DROP TABLE IF EXISTS `conn`;
CREATE TABLE `conn` (
  `id` int(11) NOT NULL auto_increment,
  `orderid` int(11) default NULL,
  `goodsid` int(11) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of conn
-- ----------------------------
INSERT INTO `conn` VALUES ('1', '1', '1');
INSERT INTO `conn` VALUES ('2', '1', '2');
INSERT INTO `conn` VALUES ('3', '1', '3');
INSERT INTO `conn` VALUES ('4', '2', '4');
INSERT INTO `conn` VALUES ('5', '2', '5');
INSERT INTO `conn` VALUES ('6', '3', '6');
INSERT INTO `conn` VALUES ('7', '3', '7');
INSERT INTO `conn` VALUES ('8', '4', '8');
INSERT INTO `conn` VALUES ('9', '5', '9');
INSERT INTO `conn` VALUES ('10', '6', '10');
INSERT INTO `conn` VALUES ('11', '6', '1');
INSERT INTO `conn` VALUES ('12', '6', '2');
INSERT INTO `conn` VALUES ('13', '7', '3');
INSERT INTO `conn` VALUES ('14', '7', '4');
INSERT INTO `conn` VALUES ('15', '8', '5');
INSERT INTO `conn` VALUES ('16', '8', '6');
INSERT INTO `conn` VALUES ('17', '8', '7');
INSERT INTO `conn` VALUES ('18', '9', '8');
INSERT INTO `conn` VALUES ('19', '9', '9');
INSERT INTO `conn` VALUES ('20', '10', '10');
INSERT INTO `conn` VALUES ('21', '10', '4');

-- ----------------------------
-- Table structure for goods
-- ----------------------------
DROP TABLE IF EXISTS `goods`;
CREATE TABLE `goods` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(255) default NULL,
  `price` double default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of goods
-- ----------------------------
INSERT INTO `goods` VALUES ('1', '电脑', '7299');
INSERT INTO `goods` VALUES ('2', '鼠标', '49');
INSERT INTO `goods` VALUES ('3', '键盘', '239');
INSERT INTO `goods` VALUES ('4', '鼠标垫', '9');
INSERT INTO `goods` VALUES ('5', '转接口', '39');
INSERT INTO `goods` VALUES ('6', '电脑包', '109');
INSERT INTO `goods` VALUES ('7', '手写板', '319');
INSERT INTO `goods` VALUES ('8', '显示器', '699');
INSERT INTO `goods` VALUES ('9', '固态', '659');
INSERT INTO `goods` VALUES ('10', '内存', '229');

-- ----------------------------
-- Table structure for orders
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `id` int(11) NOT NULL auto_increment,
  `createdate` datetime default NULL COMMENT '创建时间',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of orders
-- ----------------------------
INSERT INTO `orders` VALUES ('1', '2020-03-23 11:10:03');
INSERT INTO `orders` VALUES ('2', '2020-03-23 11:10:08');
INSERT INTO `orders` VALUES ('3', '2020-03-23 11:10:10');
INSERT INTO `orders` VALUES ('4', '2020-03-23 11:10:13');
INSERT INTO `orders` VALUES ('5', '2020-03-23 11:10:16');
INSERT INTO `orders` VALUES ('6', '2020-03-23 11:10:19');
INSERT INTO `orders` VALUES ('7', '2020-03-23 11:10:21');
INSERT INTO `orders` VALUES ('8', '2020-03-23 11:10:24');
INSERT INTO `orders` VALUES ('9', '2020-03-23 11:10:28');
INSERT INTO `orders` VALUES ('10', '2020-03-23 11:10:30');

```

###### 进行简单测试：

访问：http://localhost:8080/order/1
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326134753777.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)
访问：http://localhost:8080/goods/1
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020032613483978.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)



​		到这里只是一个普通的单体web项目，当业务量达到一定程度的时候，这样的结构很难满足需求，这时候就需要进行业务的拆分。下一节开始，将实现**订单服务**与**商品服务**的拆分。



## 二、订单与商品服务分离



​		这里需要将订单与商品服务独立布置在两台服务器上，我们可以通过分模块单独运行来模拟。

###### 拆分商品服务：

在mall下新建goods-server模块，复制mall中与商品相关的代码：

1. pom.xml中<dependencies></dependencies>中的内容;
2. GoodService、GoodsMapper、Goods、GoodsController的代码;
3. application.properties内容。

给GoodsServerApplication添加@MapperScan("com.mujio.*.mapper")

![(img-Y5C3R6JG-1585201252368)(C:%5CUsers%5CAdministrator%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200323152558558.png)\]](https://img-blog.csdnimg.cn/20200326135003916.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70)

修改application.properties开放端口为8000：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326135159310.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

启动GoodsServerApplication，并打开http://localhost:8000/goods/1测试：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326135239465.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

商品服务拆分完成。



###### 拆分订单服务：

在mall下新建order-server模块，复制mall中与订单相关的代码：

1. pom.xml中<dependencies></dependencies>中的内容
2. OrderController、OrderService、ConnMapper、OrderMapper、Conn、Goods、Order的代码；
3. application.properties内容。

> 这里需要注意的是，订单服务中仍需要部分商品服务的代码。

给OrderServerApplication添加@MapperScan("com.mujio.*.mapper")：

![](https://img-blog.csdnimg.cn/20200326135339284.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

修改application.properties开放端口为9000：

![20200326135403295.png](https://img-blog.csdnimg.cn/20200326135403295.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)



接下来，开始改造一直报红的GoodService的代码。现在订单与商品分开了，但是订单服务需要从商品服务中获取具体商品信息，这里我们可以利用RestTemplate从指定的接口获取数据：

首先需要在启动类中引入RestTemplate：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326135428634.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

接着在GoodService的代码可以改为：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326135515962.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)
最后修改OrderService，原本的项目中可以直接利用GoodsMapper来获取信息，现在只能通过GoodService来获取了：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326135552803.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)



访问：http://localhost:9000/order/1可以获取到相关信息：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326135620518.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

但是如果此时商品服务宕机了，我们的订单服务就会报错：


但是这个时候的订单信息除了商品信息获取不到其他信息应当是正常的。所以我们需要进一步修改代码以保证订单其他信息正常，这里可以选择修改GoodService，造一条商品服务异常时的替代信息：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326140703586.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)



这样我们完成了订单和商品的服务分离。但是这样还是不能有效提高系统的可靠性，单台的服务宕机，整个系统都受到影响。所以我们需要开启多台服务，来保证其中一部分不能提供服务时，还有其他的可以。下一节，我们将利用eureka来实现多台服务的“并联”。



## 三、实现分布式系统的高可用

> 后期的eureka一直到config的搭建，请注意依赖的版本号，避免冲突，本文依赖可以正常运行，大家可以参考文中的pom.xml

###### Eureka服务端搭建

Eureka的具体作用这里不做多讲，主要来实践其搭建和使用方法。创建新模块，命名为eureka-server。

> 需要注意的 是，使用spring boot创建eureka时需要选择Cloud Discovery中的Eureka Server依赖，也可以在创建好后自行添加依赖，这里直接创建模块自行添加依赖。

###### pom.xml如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.2.5.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.mujio</groupId>
    <artifactId>eureka</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>eureka</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>1.8</java.version>
        <spring-cloud.version>Hoxton.SR3</spring-cloud.version>
    </properties>

    <dependencies>
        <!-- eureka依赖 -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
            <exclusions>
                <exclusion>
                    <groupId>org.junit.vintage</groupId>
                    <artifactId>junit-vintage-engine</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
    </dependencies>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${spring-cloud.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>

```

给启动类EurekaApplication添加注解@EnableEurekaServer来开启eureka的server服务：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326141937663.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

修改配置文件，这里为了后期配置方便需要把properties文件改为yaml文件：

```yml
server:
  port: 7000

eureka:
  client:
    #是否注册到Eureka服务中
    register-with-eureka: true
    #是否从Eureka服务中获取注册信息
    fetch-registry: false
    service-url:
      #Eureka客户端与服务端进行交互的地址
      defaultZone: http://localhost:${server.port}/eureka/
```

这时，eureka的服务就可以启动了，但是这仅仅是它的服务端，所以现在可以启动并打开http://localhost:7000/验证配置的是否正确了：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326140740569.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

但是图中标记位置并没有出现任何服务，这是因为我在启动的时候将配置文件register-with-eureka的值改为了false，下面的文中将改为true，请注意观察区别；作为系统内部的服务，直接暴露出来也很不安全，这里我们需要给eureka服务加入用户认证：

首先在pom.xml中加入依赖

```xml
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
            <version>2.0.5.RELEASE</version>
        </dependency>
```

在application.yml中加入认证信息的配置：

```yaml
spring:
  security:
    user:
      name: mujio
      password: 123456

eureka:
  client:
    register-with-eureka: true #是否注册到Eureka服务中
    fetch-registry: false #是否从Eureka服务中获取注册信息
    service-url: #Eureka客户端与服务端进行交互的地址
      defaultZone: http://${spring.security.user.name}:${spring.security.user.password}@127.0.0.1:7000/eureka/
```

还需要在启动入口处加入安全认证：

```java
package com.mujio.eureka;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.server.EnableEurekaServer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;

@EnableEurekaServer
@SpringBootApplication
public class EurekaApplication {

    public static void main(String[] args) {
        SpringApplication.run(EurekaApplication.class, args);
    }


    @EnableWebSecurity
    public class WebSecurityConfigure extends WebSecurityConfigurerAdapter {
        @Override
        protected void configure(HttpSecurity http) throws Exception {
            http.csrf().disable();
            super.configure(http);
        }
    }
}

```

再次打开eureka页面http://localhost:7000/会自动跳转到登陆页面：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326140806923.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

登陆后可以看到已经有服务注册进来:
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326140859378.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)
但是这里注册的服务名为**UNKNOWN**，这是因为我们没有在配置文件中指定自己的服务名称，加入

```yml
spring:
  application:
  	#指定应用名称
    name: eureka-server
```

再次登陆应用名称将显示为eureka-server。



##### Eureka客户端搭建

eureka作为服务注册与发现中心，可以用来管理项目中的服务，那么它的客户端是什么呢？其实是几乎所有的服务都可以交给eureka来管理，包括eureka本身。

###### 客户端-商品服务：

修改pom.xml：

> 从eureka开始，建议将<parent>标签中springboot的版本改为**2.1.1.RELEASE**，否则会提示缺少健康检查的依赖。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <!-- springboot版本改为2.1.1.RELEASE -->
        <version>2.1.1.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.mujio</groupId>
    <artifactId>goods-server</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>goods-server</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>1.8</java.version>
        <spring-cloud.version>Greenwich.RC2</spring-cloud.version>
    </properties>

    <dependencies>
        <!-- 添加web服务依赖 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <!-- MySQL数据库依赖 -->
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>5.1.41</version>
        </dependency>
        <!-- mybatis依赖 -->
        <dependency>
            <groupId>org.mybatis.spring.boot</groupId>
            <artifactId>mybatis-spring-boot-starter</artifactId>
            <version>1.1.1</version>
        </dependency>

        <!-- springboot项目需要的依赖，创建项目自动添加 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
            <exclusions>
                <exclusion>
                    <groupId>org.junit.vintage</groupId>
                    <artifactId>junit-vintage-engine</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
        <!-- 添加eureka依赖 start -->
        <!-- eureka客户端依赖 -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
            <exclusions>
                <!-- eureka的数据转换，自动将数据结果转为xml格式，我们不需要xml格式的结果所以需要排除 -->
                <exclusion>
                    <groupId>com.fasterxml.jackson.dataformat</groupId>
                    <artifactId>jackson-dataformat-xml</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
    </dependencies>
    <!--  指定springcloud依赖版本  -->
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${spring-cloud.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>
    <repositories>
        <repository>
            <id>spring-milestones</id>
            <name>Spring Milestones</name>
            <url>https://repo.spring.io/milestone</url>
        </repository>
    </repositories>
    <!-- 添加eureka依赖 end -->
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>

```

在配置文件中将客户端注册到eureka中，为了配置方便将配置文件改为yaml格式：

application.yml：

```yaml
server:
  port: 8000


spring:
  #数据库连接配置
  datasource:
    driver-class-name: com.mysql.jdbc.Driver
    url: jdbc:mysql://localhost:3306/mall?characterEncoding=utf8&useUnicode=true&zeroDateTimeBehavior=convertToNull
    username: root
    password: 123
  application:
    #指定服务名称
    name: goods-server

eureka:
  client:
    #是否注册到Eureka服务中,这里是客户端需要向eureka注册
    register-with-eureka: true
    #是否从Eureka服务中获取注册信息
    fetch-registry: false
    service-url:
      #Eureka客户端与服务端进行交互的地址,这里端口直接写成eureka服务的端口
      defaultZone: http://mujio:123456@localhost:7000/eureka/
  instance:
    #把ip地址注册到Eureka服务中
    prefer-ip-address: true
```

启动eureka客户端和服务端，再次登陆eureka的管理页面http://localhost:7000/：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326140930523.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

这时，商品服务已经注册进来了，接下来开始改造订单服务。

###### 客户端-订单服务

修改pom.xml，同样是需要将springboot的版本改为2.1.1.RELEASE：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <!-- springboot版本改为2.1.1.RELEASE -->
        <version>2.1.1.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.mujio</groupId>
    <artifactId>order-server</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>order-server</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>1.8</java.version>
        <spring-cloud.version>Greenwich.RC2</spring-cloud.version>
    </properties>

    <dependencies>
        <!-- 添加web服务依赖 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <!-- MySQL数据库依赖 -->
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>5.1.41</version>
        </dependency>
        <!-- mybatis依赖 -->
        <dependency>
            <groupId>org.mybatis.spring.boot</groupId>
            <artifactId>mybatis-spring-boot-starter</artifactId>
            <version>1.1.1</version>
        </dependency>

        <!-- springboot项目需要的依赖，创建项目自动添加 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
            <exclusions>
                <exclusion>
                    <groupId>org.junit.vintage</groupId>
                    <artifactId>junit-vintage-engine</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
        <!-- 添加eureka依赖 start -->
        <!-- eureka客户端依赖 -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
            <exclusions>
                <!-- eureka的数据转换，自动将数据结果转为xml格式，我们不需要xml格式的结果所以需要排除 -->
                <exclusion>
                    <groupId>com.fasterxml.jackson.dataformat</groupId>
                    <artifactId>jackson-dataformat-xml</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
    </dependencies>
    <!--  指定springcloud依赖版本  -->
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${spring-cloud.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>
    <repositories>
        <repository>
            <id>spring-milestones</id>
            <name>Spring Milestones</name>
            <url>https://repo.spring.io/milestone</url>
        </repository>
    </repositories>
    <!-- 添加eureka依赖 end -->

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>

```

接着修改配置文件为application.yml，订单服务虽然可以交给eureka管理，但是我们这里只需要从eureka中获取到商品的注册信息即可，所以register-with-eureka可以改为false：

```yaml
server:
  port: 9000


spring:
  #数据库连接配置
  datasource:
    driver-class-name: com.mysql.jdbc.Driver
    url: jdbc:mysql://localhost:3306/mall?characterEncoding=utf8&useUnicode=true&zeroDateTimeBehavior=convertToNull
    username: root
    password: 123
  application:
    #指定服务名称
    name: order-server

eureka:
  client:
    #是否注册到Eureka服务中,这里是订单服务，只需从eureka中获取信息可以不注册
    register-with-eureka: false
    #是否从Eureka服务中获取注册信息,订单需要获取信息
    fetch-registry: true
    service-url:
      #Eureka客户端与服务端进行交互的地址,这里端口直接写成eureka服务的端口
      defaultZone: http://mujio:123456@localhost:7000/eureka/
  instance:
    #把ip地址注册到Eureka服务中
    prefer-ip-address: true
```

订单服务还需要给启动类加上@EnableDiscoveryClient注解来发现eureka中的服务：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326140956955.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

最后修改订单服务中的GoodService，此前用的是直接指定url的方式来获取商品信息，我们将他改造一下：

```java
package com.mujio.orderserver.service;


import com.mujio.orderserver.entity.Goods;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cloud.client.ServiceInstance;
import org.springframework.cloud.client.discovery.DiscoveryClient;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;

@Service
public class GoodService {

    //利用RestTemplate请求接口
    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    private DiscoveryClient discoveryClient;

    public Goods getGoods(int id) {
        String service = "goods-server";
        List<ServiceInstance> instances = discoveryClient.getInstances(service);
        if (instances.isEmpty()) {
            return null;
        }
        //instances.get(0)使用获取到的第一个服务
        String url = "http://" + instances.get(0).getHost() + ":" + instances.get(0).getPort() + "/goods/" + id;
        return restTemplate.getForObject(url, Goods.class);
    }

/*    public Goods getGoods(int id){
        String url = "http://localhost:8000/goods/" + id;
        Goods goods = new Goods();
        goods.setId(0);
        goods.setName("未能获取到商品信息");
        goods.setPrice("");
        Goods g;
        try {
            g = restTemplate.getForObject(url, Goods.class);
        } finally {
                g = goods;
            return g;
        }

    }*/
}

```

我们启动订单、商品以及eureka服务，访问http://localhost:9000/order/1：![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326141016346.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

能够正常通过eureka访问到商品服务，但是这还是商品与订单的单台服务器，我们可以自行将订单和商品模块各复制几份，修改端口后，再试试，启停商品和订单部分服务试试？

我个人把订单模块复制了一份，端口为9001，商品服务复制了两份，端口分别为8001和8002。

我们访问http://localhost:9000/order/1和http://localhost:9001/order/1均能获得结果，停止其中一个另一个当然也能正常运行：![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326141037199.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

但是我们停止商品服务8000，再次访问发现页面报错了，重新打开网页又会发现返回值正常了：![在这里插入图片描述](https://img-blog.csdnimg.cn/202003261411020.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326141124301.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

这种体验可不是太好吧？仔细想想原来是我们订单服务的GoodService请求路径用的是**instances.get(0)使用获取到的第一个服务**：![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326141145471.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

所以我们每次访问的都是同一台商品服务，这并没有减轻服务器的压力啊！感觉是不是服务器岂白启动了那么多？下一节，我们来解决这个问题。



## 四、负载均衡的引入



为了使服务器资源得到充分利用，每次在请求商品服务器时，需要请求不同的服务器，从而达到分担服务器压力的效果，其实就是这节要说的负载均衡。又需要“开刀”了！

首先对启动类下手，给它加上负载均衡的注解：![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326141210706.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

接着改造一下GoodService：

```java
package com.mujio.orderserver.service;


import com.mujio.orderserver.entity.Goods;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class GoodService {

    //利用RestTemplate请求接口
    @Autowired
    private RestTemplate restTemplate;

//    @Autowired
//    private DiscoveryClient discoveryClient;

    public Goods getGoods(int id) {
        String serverName = "goods-server";
        String url = "http://" + serverName + "/goods/" + id;
        return restTemplate.getForObject(url,Goods.class);
    }

  /*  public Goods getGoods(int id) {
        String service = "goods-server";
        List<ServiceInstance> instances = discoveryClient.getInstances(service);
        if (instances.isEmpty()) {
            return null;
        }
        //instances.get(0)使用获取到的第一个服务
        String url = "http://" + instances.get(0).getHost() + ":" + instances.get(0).getPort() + "/goods/" + id;
        return restTemplate.getForObject(url, Goods.class);
    }*/

/*    public Goods getGoods(int id){
        String url = "http://localhost:8000/goods/" + id;
        Goods goods = new Goods();
        goods.setId(0);
        goods.setName("未能获取到商品信息");
        goods.setPrice("");
        Goods g;
        try {
            g = restTemplate.getForObject(url, Goods.class);
        } finally {
                g = goods;
            return g;
        }

    }*/
}

```

现在请求的时候只需要代入服务名称，eureka就会自动去识别，至于请求具体哪一个商品服务，则是由@LoadBalanced引入的负载均衡来控制了。

为了测试负载均衡的效果，可以让商品服务的controller在接收到请求时打印一下标识，让三个controller分别打印goods-server、goods-server01和goods-server02：![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326141259271.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

重新启动，访问http://localhost:9001/order/5，仔细观察对应的输出结果，可以发现每次访问的商品服务并不是固定的，负载均衡为我们实现了轮询功能，但是具体按什么顺序去查询的呢？自己去探究去吧，我没探究，哈哈哈哈哈哈哈……





## 五、服务降级和熔断

本节将引入熔断器Hystrix。首先来看一下什么是雪崩效应：

> 服务雪崩效应是一种因“服务提供者的不可用”（原因）导致“服务调用者不可用”（结果），并将不可用逐渐放大的现象

举个**栗子**：假设，order-server请求goods-server时，由于某些原因，goods-server返回时间变为无限长，此时order-server也将一直等待响应，当order-server堆积了大量处于等待状态的请求时，order-server服务器终将撒手人寰。

这时就需要Hystrix登场，在服务出现问题时它会及时的去切断有问题的服务器，保证系统的基本秩序。

开刀：

订单服务加入hystrix依赖：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.2.5.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.mujio</groupId>
    <artifactId>mall</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>mall</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>1.8</java.version>
    </properties>

    <dependencies>
        <!--  熔断所需依赖 start -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-hystrix</artifactId>
            <version>1.4.0.RELEASE</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>com.netflix.hystrix</groupId>
            <artifactId>hystrix-javanica</artifactId>
        </dependency>
        <!--  熔断所需依赖 end -->

        <!-- 添加web服务依赖 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <!-- MySQL数据库依赖 -->
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>5.1.41</version>
        </dependency>
        <!-- mybatis依赖 -->
        <dependency>
            <groupId>org.mybatis.spring.boot</groupId>
            <artifactId>mybatis-spring-boot-starter</artifactId>
            <version>1.1.1</version>
        </dependency>

        <!-- springboot项目需要的依赖，创建项目自动添加 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
            <exclusions>
                <exclusion>
                    <groupId>org.junit.vintage</groupId>
                    <artifactId>junit-vintage-engine</artifactId>
                </exclusion>
            </exclusions>
        </dependency>

    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>

```

启动类OrderServerApplication加上开启hystrix的注解@EnableHystrix：![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326141325336.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

最后需要改造一下订单服务中的GoodService：

```java
package com.mujio.orderserver.service;


import com.mujio.orderserver.entity.Goods;
import com.netflix.hystrix.contrib.javanica.annotation.HystrixCommand;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class GoodService {

    //利用RestTemplate请求接口
    @Autowired
    private RestTemplate restTemplate;


    //启用负载均衡后，restTemplate自动选择访问哪个服务
    @HystrixCommand(fallbackMethod = "getGoodsServiceOffline")
    public Goods getGoods(int id){
        String serverName = "goods-server";
        String url = "http://" + serverName + "/goods/" + id;
        return restTemplate.getForObject(url,Goods.class);
    }
    //请求失败后，调用fallbackMethod指定的方法
    public Goods getGoodsServiceOffline(int id){
        Goods goods = new Goods();
        goods.setId(0);
        goods.setName("未能获取到商品信息");
        goods.setPrice("");
        return goods;
    }




/*
//    @Autowired
//    private DiscoveryClient discoveryClient;

    public Goods getGoods(int id) {
        String serverName = "goods-server";
        String url = "http://" + serverName + "/goods/" + id;
        System.out.println(url);
        return restTemplate.getForObject(url,Goods.class);
    }
*/

  /*  public Goods getGoods(int id) {
        String service = "goods-server";
        List<ServiceInstance> instances = discoveryClient.getInstances(service);
        if (instances.isEmpty()) {
            return null;
        }
        //instances.get(0)使用获取到的第一个服务
        String url = "http://" + instances.get(0).getHost() + ":" + instances.get(0).getPort() + "/goods/" + id;
        return restTemplate.getForObject(url, Goods.class);
    }*/

/*    public Goods getGoods(int id){
        String url = "http://localhost:8000/goods/" + id;
        Goods goods = new Goods();
        goods.setId(0);
        goods.setName("未能获取到商品信息");
        goods.setPrice("");
        Goods g;
        try {
            g = restTemplate.getForObject(url, Goods.class);
        } finally {
                g = goods;
            return g;
        }

    }*/
}

```

重启服务，访问http://localhost:9000/order/4并多次刷新,信息正常；停止goods-server01，再次访问，多次刷新：![在这里插入图片描述](https://img-blog.csdnimg.cn/2020032614142746.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)
可以看到，刚停止时goods-server01时，返回速度明显慢了一些，并且在关闭后访问会显示“未能获取到商品信息”，但是多次访问刷新之后又会发现信息又正常了。这是因为熔断器发挥了作用，在服务出现故障的时候调用了fallbackMethod，并且及时切断该服务，使得再刷新后数据恢复正常。

目前我们已经初步实现了分布式的目的，但是仔细一想，这个系统还是有问题：eureka要是崩了咋办？开启两个order-server有个锤子用？访问的时候不还是得区分端口？还有这个服务调用藏在service中会不会有点太深了？

当然哈，只是觉得这一节篇幅有点短了，不如现在强行加点：

**Feign：**

> feign是声明式的web service客户端，Spring Cloud集成了Ribbon和Eureka，可在使用Feign提供负载均衡的http客户端。

瞧瞧这说法，“可使用Feign提供负载均衡的http客户端”，怎么提供呢？一步一步来：

加依赖（负载均衡在order-server中，当然也是给order-server的pom.xml加了）：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <!-- springboot版本改为2.1.1.RELEASE -->
        <version>2.1.1.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.mujio</groupId>
    <artifactId>order-server</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>order-server</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>1.8</java.version>
        <spring-cloud.version>Greenwich.RC2</spring-cloud.version>
    </properties>

    <dependencies>
        <!--  Feign所需依赖 start -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-openfeign</artifactId>
        </dependency>
        <!--  根据spring cloud的版本选择，早期的使用下面的依赖 -->
        <!--<dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-feign</artifactId>
        </dependency>-->
        <!--  Feign所需依赖 end -->

        <!--  熔断所需依赖 start -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-hystrix</artifactId>
            <version>1.4.0.RELEASE</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>com.netflix.hystrix</groupId>
            <artifactId>hystrix-javanica</artifactId>
        </dependency>
        <!--  熔断所需依赖 end -->

        <!-- 添加web服务依赖 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <!-- MySQL数据库依赖 -->
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>5.1.41</version>
        </dependency>
        <!-- mybatis依赖 -->
        <dependency>
            <groupId>org.mybatis.spring.boot</groupId>
            <artifactId>mybatis-spring-boot-starter</artifactId>
            <version>1.1.1</version>
        </dependency>

        <!-- springboot项目需要的依赖，创建项目自动添加 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
            <exclusions>
                <exclusion>
                    <groupId>org.junit.vintage</groupId>
                    <artifactId>junit-vintage-engine</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
        <!-- 添加eureka依赖 start -->
        <!-- eureka客户端依赖 -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
            <exclusions>
                <!-- eureka的数据转换，自动将数据结果转为xml格式，我们不需要xml格式的结果所以需要排除 -->
                <exclusion>
                    <groupId>com.fasterxml.jackson.dataformat</groupId>
                    <artifactId>jackson-dataformat-xml</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
    </dependencies>
    <!--  指定springcloud依赖版本  -->
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${spring-cloud.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>
    <repositories>
        <repository>
            <id>spring-milestones</id>
            <name>Spring Milestones</name>
            <url>https://repo.spring.io/milestone</url>
        </repository>
    </repositories>
    <!-- 添加eureka依赖 end -->

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>

```

> 需要**注意**的是，本文中使用的spring cloud的版本是：Greenwich.RC2，加入feign时如出现冲突，比其早的版本，请考虑使用spring-cloud-starter-feign

继续改造，首先是启动类加注解@EnableFeignClients:

```java
package com.mujio.orderserver;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.client.loadbalancer.LoadBalanced;
import org.springframework.cloud.openfeign.EnableFeignClients;
import org.springframework.context.annotation.Bean;
import org.springframework.web.client.RestTemplate;

@EnableFeignClients
@EnableDiscoveryClient
@SpringBootApplication
public class OrderServerApplication {

    public static void main(String[] args) {
        SpringApplication.run(OrderServerApplication.class, args);
    }

    @Bean
    @LoadBalanced
    public RestTemplate restTemplate(){
        return new RestTemplate();
    }
}

```

创建个使用feign的接口：![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326141451206.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

> 这里有个@FeignClient(value = "goods-server")，它会根据value值自动转换成对应的服务，所以要注意商品服务的应用名要与之一致。

它有点类似与controller根据请求路径调用对应service方法，所以我是放在了controller包中。

再次改造GoodService（刀妹？？）：

```java
package com.mujio.orderserver.service;


import com.mujio.orderserver.controller.GoodsFeignClient;
import com.mujio.orderserver.entity.Goods;
import com.netflix.hystrix.contrib.javanica.annotation.HystrixCommand;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class GoodService {

    // 引入feign
    @Autowired
    private GoodsFeignClient goodsFeignClient;

    //启用负载均衡后，有restTemplate自己去选择访问那个服务
    @HystrixCommand(fallbackMethod = "getGoodsServiceOffline")
    public Goods getGoods(int id){
        return goodsFeignClient.getGoods(id);
    }

    public Goods getGoodsServiceOffline(int id){
        Goods goods = new Goods();
        goods.setId(0);
        goods.setName("未能获取到商品信息");
        goods.setPrice("");
        return goods;
    }



/*
    @Autowired
    private RestTemplate restTemplate;

    //启用负载均衡后，restTemplate自动选择访问哪个服务
    @HystrixCommand(fallbackMethod = "getGoodsServiceOffline")
    public Goods getGoods(int id){
        String serverName = "goods-server";
        String url = "http://" + serverName + "/goods/" + id;
        return restTemplate.getForObject(url,Goods.class);
    }
    //请求失败后，调用fallbackMethod指定的方法
    public Goods getGoodsServiceOffline(int id){
        Goods goods = new Goods();
        goods.setId(0);
        goods.setName("未能获取到商品信息");
        goods.setPrice("");
        return goods;
    }

*/



/*
//    @Autowired
//    private DiscoveryClient discoveryClient;

    public Goods getGoods(int id) {
        String serverName = "goods-server";
        String url = "http://" + serverName + "/goods/" + id;
        System.out.println(url);
        return restTemplate.getForObject(url,Goods.class);
    }
*/

  /*  public Goods getGoods(int id) {
        String service = "goods-server";
        List<ServiceInstance> instances = discoveryClient.getInstances(service);
        if (instances.isEmpty()) {
            return null;
        }
        //instances.get(0)使用获取到的第一个服务
        String url = "http://" + instances.get(0).getHost() + ":" + instances.get(0).getPort() + "/goods/" + id;
        return restTemplate.getForObject(url, Goods.class);
    }*/

/*    public Goods getGoods(int id){
        String url = "http://localhost:8000/goods/" + id;
        Goods goods = new Goods();
        goods.setId(0);
        goods.setName("未能获取到商品信息");
        goods.setPrice("");
        Goods g;
        try {
            g = restTemplate.getForObject(url, Goods.class);
        } finally {
                g = goods;
            return g;
        }

    }*/
}

```

搞完重启服务，测试啥的自然不用说了。下一节将引入zuul，顺便解决另外两个问题。（主要是因为本节代码已经上传了，嘿嘿）



## 六、API网关：Zuul

zuul也叫路由网关，具体啥作用咱目前也不用管，个人喜欢先上手，会用了再去了解它到底是什么。咱们暂时可以参考controller来理解zuul，简单来说就类似于路径带"/order"访问订单服务，带"/goods"访问商品服务。

开干，新建模块zuul，pom.xml如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.2.5.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.mujio</groupId>
    <artifactId>zuul</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>zuul</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>1.8</java.version>
        <!-- 引入zuul时使用Hoxton.SR3 -->
<!--        <spring-cloud.version>Greenwich.RC2</spring-cloud.version>-->
        <spring-cloud.version>Hoxton.SR3</spring-cloud.version>
    </properties>

    <dependencies>
        <!-- 需要eureka依赖 -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
        </dependency>
        <!-- zuul依赖 -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-zuul</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
            <exclusions>
                <exclusion>
                    <groupId>org.junit.vintage</groupId>
                    <artifactId>junit-vintage-engine</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
    </dependencies>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${spring-cloud.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>

```

> 注意：引入zuul时，会发现依赖报错，将spring cloud版本换成Hoxton.SR3可解决。

启动类开启eureka和zuul的注解：

```
@EnableDiscoveryClient
@EnableZuulProxy
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326141518684.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

修改配置文件为application.yml：

```yaml
server:
  port: 7100

spring:
  application:
    #指定服务名称
    name: zuul-server

eureka:
  client:
    #是否注册到Eureka服务中
    register-with-eureka: true
    #是否从Eureka服务中获取注册信息
    fetch-registry: true
    service-url:
      #Eureka客户端与服务端进行交互的地址
      defaultZone: http://mujio:123456@localhost:7000/eureka/
  instance:
    #把ip地址注册到Eureka服务中
    prefer-ip-address: true
    ip-address: 127.0.0.1


zuul:
  routes:
    goods-server:
      # 将所有/goods/的路径映射到goods-server上
      path: /goods/**
      serviceId: goods-server
      strip-prefix: false
```

启动，测试http://localhost:7100/goods/1和http://localhost:7100/goods-server/goods/1：![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326141540669.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

我们访问的是zuul的端口，加上的是商品服务的映射路径，成功获取到商品服务的返回值，但是为什么这两个路径都是正常的呢？大家可以去掉配置文件中的 strip-prefix: false 试试，把path改为其他值再试试。

在zuul实现路由时，还可以通过继承ZuulFilter来实现路由前置后置等方法，且看代码：

```java
package com.mujio.zuul.filter;

import com.netflix.zuul.ZuulFilter;
import com.netflix.zuul.context.RequestContext;
import com.netflix.zuul.exception.ZuulException;
import org.apache.commons.lang.StringUtils;
import org.springframework.cloud.netflix.zuul.filters.support.FilterConstants;
import org.springframework.stereotype.Component;

import javax.servlet.http.HttpServletRequest;

/**
 * 可以通过不同的filter继承ZuulFilter来实现前置后置等方法
 * FilterConstants.PRE_TYPE请求被路由前调用
 * FilterConstants.POST_TYPE在ROUTE和ERROR后调用
 * FilterConstants.ROUTE_TYPE请求时调用
 * FilterConstants.ERROR_TYPE请求出现错误时调用
 */
@Component
public class UserFilter extends ZuulFilter{
    
    // 请求被路由前调用
    @Override
    public String filterType() {
        return FilterConstants.PRE_TYPE;
    }

    //数值越大优先级越靠后
    @Override
    public int filterOrder() {
        return 0;
    }
    
    //是否进行过滤
    @Override
    public boolean shouldFilter() {
        return true;
    }
    
    //具体的过滤规则实现
    @Override
    public Object run() throws ZuulException {
        HttpServletRequest req = RequestContext.getCurrentContext().getRequest();
        String token = req.getParameter("token");
        if (StringUtils.isEmpty(token)){
            RequestContext.getCurrentContext().setSendZuulResponse(false);//不进行路由
            RequestContext.getCurrentContext().setResponseStatusCode(200);
            RequestContext.getCurrentContext().setResponseBody("{\"error\":\"invalid token\"}");
        }
        return null;
    }
}
```

重启，测试http://localhost:7100/goods/1：![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326141603683.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)
http://localhost:7100/goods/1?token=1：![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326141623681.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

如上效果，通过zuul实现了token验证的功能。



解决上一节提到的两个问题：

1. eureka服务挂了咋办？
2. 启动多个订单服务有什么用？

首先看第一个问题，我们先复制两份eureka，端口设为7001、7002。修改三个eureka服务配置文件为：

eureka：

```yaml
server:
  port: 7000

spring:
  application:
    name: eureka-server
  security:
    user:
      #认证信息
      name: mujio
      password: 123456

eureka:
  client:
    #是否注册到Eureka服务中
    register-with-eureka: true
    #是否从Eureka服务中获取注册信息---修改为true
    fetch-registry: true
    service-url:
      #Eureka客户端与服务端进行交互的地址,加入认证信息---修改为用","隔开的两个eureka地址
      defaultZone: http://${spring.security.user.name}:${spring.security.user.password}@localhost:7001/eureka/,http://${spring.security.user.name}:${spring.security.user.password}@localhost:7002/eureka/
```

eureka01：

```yaml
server:
  port: 7001

spring:
  application:
    name: eureka-server
  security:
    user:
      #认证信息
      name: mujio
      password: 123456

eureka:
  client:
    #是否注册到Eureka服务中
    register-with-eureka: true
    #是否从Eureka服务中获取注册信息---修改为true
    fetch-registry: true
    service-url:
      #Eureka客户端与服务端进行交互的地址,加入认证信息---修改为用","隔开的两个eureka地址
      defaultZone: http://${spring.security.user.name}:${spring.security.user.password}@localhost:7000/eureka/,http://${spring.security.user.name}:${spring.security.user.password}@localhost:7002/eureka/
```

eureka02:

```yaml
server:
  port: 7002

spring:
  application:
    name: eureka-server
  security:
    user:
      #认证信息
      name: mujio
      password: 123456

eureka:
  client:
    #是否注册到Eureka服务中
    register-with-eureka: true
    #是否从Eureka服务中获取注册信息---修改为true
    fetch-registry: true
    service-url:
      #Eureka客户端与服务端进行交互的地址,加入认证信息---修改为用","隔开的两个eureka地址
      defaultZone: http://${spring.security.user.name}:${spring.security.user.password}@localhost:7000/eureka/,http://${spring.security.user.name}:${spring.security.user.password}@localhost:7001/eureka/
```



重启，测试http://localhost:9000/order/1：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326141647370.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

停止eureka，再次访问；停止eureka01再次访问；停止eureka02再次访问。再逐次停止goods-server再次访问。

可以发现，eureka服务并没有影响到order服务的运行，但是商品服务的宕机，影响到了order获取商品的信息，直到所有的eureka和商品服务都宕机了，订单服务任然能运行，只是获取不到正确的商品信息。真正实现了订单服务的高可用。



至此，我们的分布式系统已经相对完整了，这个时候我们来考虑第二个问题：

2.订单服务挂了怎么办？

其实这个问题我并没有找到满意的解答。准确的问题中心并不单单指订单服务，可以是登陆中心，可以是Zuul网关等等。

假设用户走进"门店"，门店可以通过各种方法保证提供稳定的服务，但是保证门店屹立不倒呢？这个问题还是留着继续思考吧。



下一节，引入config配置中心。



## 七、配置中心Config

Spring Cloud Config为分布式系统中的外部化配置提供了服务器端和客户端支持。通过配置服务器，可以很方便的来管理各应用程序的外部属性。本文将实现客户端获取配置参数。

新建config模块，添加pom.xml依赖：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.2.5.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.mujio</groupId>
    <artifactId>config</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>config</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>1.8</java.version>
        <!-- spring cloud版本 -->
        <spring-cloud.version>Hoxton.SR3</spring-cloud.version>
    </properties>

    <dependencies>
        <!-- config所需要的依赖 -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-config-server</artifactId>
        </dependency>
        <!-- config需要注册到eureka中，故需要添加eureka依赖 -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
        </dependency>
        <!-- springboot健康检查 -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
            <exclusions>
                <exclusion>
                    <groupId>org.junit.vintage</groupId>
                    <artifactId>junit-vintage-engine</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
    </dependencies>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${spring-cloud.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>

```

修改配置文件为application.yml：

```yaml
server:
  port: 9400

eureka:
  client:
    #是否注册到Eureka服务中
    register-with-eureka: true
    #是否从Eureka服务中获取注册信息
    fetch-registry: false
    #Eureka客户端与服务端进行交互的地址
    service-url:
      defaultZone: http://mujio:123456@localhost:7000/eureka/
    #健康检查（需要spring-boot-starter-actuator依赖）
    healthcheck:
      enabled: true

  instance:
    #把ip地址注册到Eureka服务中
    prefer-ip-address: true
    # 续约更新时间间隔（默认30秒）
    lease-renewal-interval-in-seconds: 10
    # 续约到期时间（默认90秒）
    lease-expiration-duration-in-seconds: 10
```

添加配置文件bootstrap.yml，这里以读取本地文件为例：

```yml
spring:
  application:
    name: config-server #配置服务名称
  profiles:
    active: native #设置为本地启动的方式，而不是通过git
  cloud:
    config:
      server:
        native:
          # 配置文件所在目录，classpath（类路径）和（系统文件路径） file两种
          searchLocations: classpath:/

```

给启动类加上eureka注解和config服务端注解：

```java
package com.mujio.config;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.config.server.EnableConfigServer;

@EnableConfigServer
@EnableDiscoveryClient
@SpringBootApplication
public class ConfigApplication {

    public static void main(String[] args) {
        SpringApplication.run(ConfigApplication.class, args);
    }

}

```

以goods-server为例，pom.xml中加入config的依赖：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <!-- springboot版本改为2.1.1.RELEASE -->
        <version>2.1.1.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.mujio</groupId>
    <artifactId>goods-server</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>goods-server</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>1.8</java.version>
        <spring-cloud.version>Greenwich.RC2</spring-cloud.version>
    </properties>

    <dependencies>
        <!-- 添加web服务依赖 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <!-- MySQL数据库依赖 -->
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>5.1.41</version>
        </dependency>
        <!-- mybatis依赖 -->
        <dependency>
            <groupId>org.mybatis.spring.boot</groupId>
            <artifactId>mybatis-spring-boot-starter</artifactId>
            <version>1.1.1</version>
        </dependency>

        <!-- springboot项目需要的依赖，创建项目自动添加 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
            <exclusions>
                <exclusion>
                    <groupId>org.junit.vintage</groupId>
                    <artifactId>junit-vintage-engine</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
        <!-- 添加eureka依赖 start -->
        <!-- eureka客户端依赖 -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
            <exclusions>
                <!-- eureka的数据转换，自动将数据结果转为xml格式，我们不需要xml格式的结果所以需要排除 -->
                <exclusion>
                    <groupId>com.fasterxml.jackson.dataformat</groupId>
                    <artifactId>jackson-dataformat-xml</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
        <!-- config客户端所需依赖 -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-config</artifactId>
        </dependency>
    </dependencies>
    <!--  指定springcloud依赖版本  -->
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${spring-cloud.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>
    <repositories>
        <repository>
            <id>spring-milestones</id>
            <name>Spring Milestones</name>
            <url>https://repo.spring.io/milestone</url>
        </repository>
    </repositories>
    <!-- 添加eureka依赖 end -->
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>

```

> config的客户端和服务端依赖并不一样，一个是spring-cloud-config-server一个是spring-cloud-starter-config。

添加引导配置bootstrap.yml：

```yml
spring:
  application:
    name: goods-server
  cloud:
    config:
      discovery:
        enabled: true
        service-id: goods-server
      profile: dev
      uri: http://localhost:9400/
      enabled: true

eureka:
  client:
    register-with-eureka: true #是否注册到Eureka服务中
    fetch-registry: true #是否从Eureka服务中获取注册信息
    service-url: #Eureka客户端与服务端进行交互的地址
      defaultZone: http://mujio:123456@localhost:7000/eureka/
  instance:
    prefer-ip-address: true #把ip地址注册到Eureka服务中
    ip-address: 127.0.0.1

```

已经可以进行测试了，启动端口为7000的eureka，启动config，检查eureka管理页面中是否正确获取到config服务：![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326141732252.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

启动成功，接着启动goods-server，我们原本配置的端口为8000，我读取的是在config模块resources下的配置文件goods-server-dev.yml内容为：

> 这里读取的配置文件与goods-server模块bootstrap.yml中指定的 service-id: goods-server和 profile: dev一致。

```yaml
server:
  port: 8029

spring:
  application:
    name: goods-server #指定服务名称

eureka:
  client:
    register-with-eureka: true #是否注册到Eureka服务中
    fetch-registry: false #是否从Eureka服务中获取注册信息
    service-url: #Eureka客户端与服务端进行交互的地址
      defaultZone: http://mujio:123456@localhost:7000/eureka/
  instance:
    prefer-ip-address: true #把ip地址注册到Eureka服务中
```

启动结果：![在这里插入图片描述](https://img-blog.csdnimg.cn/20200326141755615.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzI4MzM2Mw==,size_16,color_FFFFFF,t_70#pic_center)

可以看到，goods-server的application.yml配置文件中指定的端口为8000，但是实际启动的端口是config中读取到的配置8029。说明咱们已经初步配置好了config。



## 八、简单总结

​	看过[Felix独箸](https://www.jianshu.com/u/0e5883241140)大佬原文的朋友应该知道，我这里写的代码只是对原文的copy，稍作改动。本来是准备给自己用的demo，一开始也没有想着写文章，但是参照原文搭建的时候还是出现了很多的问题，有的时候我们并不想去深入探究具体什么原理，只是想立马用起来，所以我厚着脸皮又搭了一遍，并且记录了下来。文中也尽量将我能正常运行的代码都贴了出来，只为有需要的时候可以直接**ctrl+C** and **ctrl+V**。细心的也可以发现，其实我springboot的版本以及spring cloud的版本并不是完全一致的，在实际搭建的过程中有尝试其他版本，但是忘了改了……

有时间还是得多去看看官方的说法，那些英文的说明也没有特别的深奥，不懂得词划出来翻一下就好了，至于这个轮子就搭到这里吧。有需要源码的可以到我的github来下载：

github地址：https://github.com/Mujio-killer/mall.git


