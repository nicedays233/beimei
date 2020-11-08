package com.wyw.corndemo.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

import java.sql.*;

@SpringBootApplication
@EnableScheduling
public class DemoApplication {

	public static void main(String[] args) throws ClassNotFoundException, SQLException {

		Class.forName("com.mysql.jdbc.Driver");
		// 这里是隐式调用
		// dm用于管理驱动程序自己在内存里搜引用驱动程序，尝试在初始化中加载的驱动程序中的合适的驱动程序
		Connection con = DriverManager.getConnection("jdbc:mysql://192.168.56.101:3306/mydemo","root","123456");
//		CallableStatement cs = con.prepareCall("{call func_sum(?,?)}");
		 PreparedStatement ps = con.prepareStatement("select func_sum(?,?) as res");
		 ps.setInt(1,30);
		 ps.setInt(2,99);
		ResultSet resultSet = ps.executeQuery();
		while (resultSet.next()) {
			System.out.println(resultSet.getInt("res"));
		}
//		cs.setInt(1, 20);
//		cs.setInt(2,30);
//		cs.registerOutParameter(3,Types.INTEGER);
//		cs.execute();
//		System.out.println(cs.getInt(3));
		con.close();
	}

}
