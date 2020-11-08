package com.wyw.hdfs;

import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;

/**
 * @ClassName:MyClient
 * @Author WYW
 * @Date03/06/202009:49
 * @Description: TODO
 * @Version V1.0
 **/
public class MyClient extends Thread {
	@Override
	public void run() {
		for (int i = 0; i < 50000; i++) {
			try {
				Socket localhost = new Socket("localhost", 50000);
				OutputStream os = localhost.getOutputStream();
				String clientInfo = " i am client" + i + "\n";
				os.write(clientInfo.getBytes());
				os.close();
				localhost.close();
				Thread.sleep(30);
			} catch (IOException e) {
				e.printStackTrace();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}

	}
File
	public static void main(String[] args) throws IOException {
		new MyClient().start();
	}

}
