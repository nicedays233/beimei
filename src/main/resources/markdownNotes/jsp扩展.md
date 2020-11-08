## 一：侦听器

#### 1.web侦听器分类：接口

- 上下文  ServletContextListener tomcat启动关闭时，各执行一次

- 会话     HttpSessionListener     在会话创建何销毁时，各执行一次

- servlet ...

  对三种进行侦听

#### 2.创建：创建一个实现servlet-api 中定义好的侦听器接口类

#### 3.配置：web.xml中：

###### <listener><listener-class>全包路径</listener-class></listener>

###### <listener><listener-class>全包路径</listener-class></listener>

...





## 二：过滤器

#### 1.针对servlet中的一些或全部行为进行筛选性质的统一处理

​		xxx.do动态

​		xxx.html/xxx.jsp/xxx.css/...  静态

对某一类的请求进行过滤，比如没有登录的状态的请求会过滤到登录页面去

#### 2.创建：创建一个实现servlet-api中定义好的过滤器接口类

#### 3.配置：web.xml配置filter和filter-mapping

过滤器执行的先后顺序就是配置的先后顺序

## 三：会话

#### 1.http协议是基于单次请求HttpServletRequest和响应HttpServletResponse的，这个过程不记录状态，因此无法确认身份

#### 2.使用会话HttpSession来存储状态

#### 3.HttpSession创建和生命周期

- 每一位用户第一次请求时由**tomcat容器**创建会话对象
- 提取会话对象：HttpSession session = HttpServletRequest.getSession();
- HttpSession 的最大【闲置：从不做任何操作开始计时】时间，默认为30分钟

![image-20200421174209628](C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\image-20200421174209628.png)

##### tomcat的web.xml里配置

- session.setMaxlnactiveInterval(秒)来设置生命周期
- HttpSession 何时死亡
  - 寿终正寝：闲置时间到了，会话自动死亡
  - 手动干死它：session.invalidate();
  - 关闭浏览器：关闭窗口没有用
- 如果记录状态：
  - session.setAttribute(String key,Object value)
  - T t = (T)session.getAttribute(String key)

## 四：页面跳转的方式

#### 1.转发

- 需要携带数据：req.setAttribute()
- 如何转发：req.getRequestDispatcher("*.jsp/*.do").get

#### 2.重定向

- 无需携带数据

![image-20200421182101335](C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\image-20200421182101335.png)

