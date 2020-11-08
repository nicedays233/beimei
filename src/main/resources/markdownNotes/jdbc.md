## JDBC

## 基础版

#### Statement版：

```java
String url = "jdbc:mysql://localhost:3306/mydb?useUnicode=true&characterEncoding=utf8";
String sql = "SELECT * FROM classinfo";
Connection con = null;
Statement sta = null;
PreparedStatement psta = null;
ResultSet rst = null;
try{
	class.forName("com.sql.jdbc.Driver");// 加载驱动
	con = DriverManager.getConnection(url,"root","root"); //建立连接
	sta = con.createStatement();// 创建传送代理，将sql语句传给DBMS数据库操作系统检查语句，没有预先编译  	
	rst = sta.executeQuery();//传送代理执行，并会返回结果集rst
	psta = con.PreparedStatment(sql);
}catch(SQLException e){
    e.printStackTrace();
}catch(ClassNotFoundException e){
    e.printStackTrace();
}finally{
    try{
        rst.close();//关闭资源，后用先关，先用后关
        sta.close();
        con.close();
    }catch(SQLException e){
    	e.printStackTrace();
    }
}

```

PreparedStatement版：

```java
String url = "jdbc:mysql://localhost:3306/mydb?useUnicode=true&characterEncoding=utf8";
String sql = "INSERT INTO classinfo(className,Date) VALUE(?,?)";//preparedstatment的占位符
Connection con = null;
Statement sta = null;
PreparedStatement psta = null;
ResultSet rst = null;
try{
	class.forName("com.sql.jdbc.Driver");// 加载驱动
	con = DriverManager.getConnection(url,"root","root"); //建立连接
    // 创建传送代理，预先编译检查,再将sql语句传给DBMS数据库操作系统检查语句，防止部分SQL注入
	psta = con.PrepareStatment(sql);
	psta.setString(1,"xxx");//从0列开始，0列为主键所以不写
	psta.setString(2,"xxxx-xx-xx");    
	int result = sta.executeUpdate();//传送代理执行，并会返回结果
}catch(SQLException e){
    e.printStackTrace();
}catch(ClassNotFoundException e){
    e.printStackTrace();
}finally{
    try{
        rst.close();//关闭资源，后用先关，先用后关
        sta.close();
        con.close();
    }catch(SQLException e){
    	e.printStackTrace();
    }
}

```

## 封装版：

```java
public class Mydb{
    private  String url="jdbc:mysql://localhost:3306/runoob?useUnicode=true&characterEncoding=utf8";
    private  String username="root";
    private  String password="root";
    // 初始化
    public Mydb(String url,String username,String password,String Driver)throws ClassNotFoundException{
        this.url = url;
        this.username = username;
        this.password = password;
        class.forName(Driver);
    }
    // 建立连接
     private Connection getCon(){
        return DriverManager.getConnection(url,username,password);
    }
    // 建立传送代理
    private PreparedStatment getPsta(Connection con,String sql,Object...params){
        PreparedStatement pst = con.prepareStatement(sql);
        if (null!= params && params.length>0){
            for (int i = 0; i < params.length ; i++) {
                pst.setObject(i+1,params[i]);
            }
        }
        return pst;
    }
   // 关闭资源
    private void close(Object...objs) throw SQLException{
        for(Object obj:objs){
            if(obj instanceof ResultSet){
				((ResultSet)obj).close();                
            }else if(obj instanceof PreparedStatement){
				((PreparedStatement)obj).close();
            }else if(obj instanceof Connection){
				((Connection)obj).close();
            }
        }
    };
    // 增删改操作
    public boolean zsg(String sql,Object...params)throw SQLException{
        Connection con = null;
        PreparedStatement pst = null;
        try{
            con = getCon();
            pst = getPst(con,sql,params);
            return pst.executeUpdate();
        }catch (SQLException e){
            e.printStackTrace();
        }finally {
            close(pst,con);
        }
        return -1;
    }
}
```

## 反射版

```java
// 反射版主要是体现在对动态的去修改，将原有的JDBC,URL,USERNAME,PASSWORD放入到配置文件中，对于维护这段代码来说更加的方便
// 同时当只知道实体类的对象时来完成得到类型信息解析，JDBC当我们新建一张表时，要将其在IDEA中解析成对应的类，













```

 