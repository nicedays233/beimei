## SSM--web

## 前后端分离（JS访问后台数据-java-json）

json：[]表示数组，{}表示对象，：表示键值对，‘，’表示键值对分割符

### 1.依赖(1-5:spring,6-8:web,9-10:json)

1. **mysql-driver**
2. **mybatis**
3. **spring-context**
4. **spring-jdbc**
5. **mybatis-spring**
6. **servlet**
7. **spring-web**
8. **spring-webmvc**
9. **jackson-core**
10. **jackson-databind**

![img](file:///E:\QQData\741454344\Image\Group2\I_\1Q\I_1QW]C3QL0M69E5[W%PF_0.png)

### 2.配置

项目结构：

![image-20200430140913024](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200430140913024.png)

![image-20200430141116648](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200430141116648.png)





1. XML

   

2. #### 注解

   - 类注解
     - @Component 组件
       - @Repository：数据访问层：mapper(Dao)
       - @Service ：业务层service(biz)
       - @Controller：jsp控制层 control
       - @RestController = @Controller + @ResponseBody:  ajax-json
     - @ResponseBody：ajax访问
     - @RequestMapping
     - @CrossOrigin：跨域  域名

   - 属性注解
     - @AutoWired 自动注入：不用写get/set方法了
   - 方法注解            RESTFUL请求风格定义
     - @RequestMapping
       - @GetMapping
       - @PostMapping
       - @DeleteMapping
       - @PutMapping
     - @CrossOrigin
   - 参数注解
     - @PathVariable
     - @RequestParam

   

   1. 


   