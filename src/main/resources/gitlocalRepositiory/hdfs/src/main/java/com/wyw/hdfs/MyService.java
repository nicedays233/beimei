package com.wyw.hdfs;

import org.apache.commons.net.io.SocketInputStream;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IOUtils;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.URI;
import java.net.URISyntaxException;

/**
 * @ClassName:MyService
 * @Author WYW
 * @Date03/06/202009:43
 * @Description: TODO
 * @Version V1.0
 **/
public class MyService {

	private static volatile MyService myService;

	private MyService() {}

	public static MyService getInstance(){
		if (myService == null){
			synchronized (MyService.class){
				if (myService == null){
					myService = new MyService();
				}
			}
		}
		return myService;
	}

	private static FileSystem fs;
	static {
		try {
			fs = FileSystem.get(new URI("hdfs://192.168.56.101:9000"), new Configuration());
		} catch (IOException e) {
			e.printStackTrace();
		} catch (URISyntaxException e) {
			e.printStackTrace();
		}
	}
	public static void main(String[] args) throws IOException {
		MyService instance = MyService.getInstance();
		int count = 0;
		// 服务器接收信息
		while (true) {
			ServerSocket sck = new ServerSocket(50000);
			// 阻塞接受

			Socket s = sck.accept();

			// 拿到客户端流
			InputStream is = s.getInputStream();
			System.out.println(is.toString() + count++);
			// 塞输出流，进行写入工作
			instance.write(is);
			System.out.println(is.toString() + count);
			is.close();
			sck.close();
		}

	}

	// hdfs写文件过程
	private void write(InputStream fis){
		try {
			// 输出到
			FSDataOutputStream fos = fs.append(new Path("/mydemo/niceday.txt"));
			IOUtils.copyBytes(fis,fos,8192,true);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
 }
