package com.wyw.hdfs;

import org.apache.commons.collections.map.Flat3Map;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IOUtils;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;

/**
 * @ClassName:MyReadAndWrite
 * @Author WYW
 * @Date03/06/202009:06
 * @Description: TODO
 * @Version V1.0
 **/
public class MyReadAndWrite {
	static FileSystem fs;
	static {
		try {
			fs = FileSystem.get(new URI("hdfs://192.168.56.101:9000"), new Configuration());
		} catch (IOException e) {
			e.printStackTrace();
		} catch (URISyntaxException e) {
			e.printStackTrace();
		}
	}
	public void read(){
		try {
			FSDataInputStream fis = fs.open(new Path("/mydemo/niceday.txt"));
			FileOutputStream fos = new FileOutputStream("d://niceday.txt");
			// 建立蓄水池，将输出流放到池里，输入流从池里拿流，true自动关闭流
			IOUtils.copyBytes(fis,fos,4096,true);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	public void write(){
		try {
			// 将xx塞入输入流
			FileInputStream fis = new FileInputStream("d://event.log");
			// 输出到xxx
			FSDataOutputStream fos = fs.create(new Path("/mydemo/niceday.txt"));
			IOUtils.copyBytes(fis,fos,4096,true);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public static void main(String[] args) {
		new MyReadAndWrite().write();
//		new MyReadAndWrite().read();
	}
}
