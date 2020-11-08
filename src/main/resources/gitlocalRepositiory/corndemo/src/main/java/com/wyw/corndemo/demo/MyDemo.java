package com.wyw.corndemo.demo;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.Date;

/**
 * @ClassName:MuDemo
 * @Author WYW
 * @Date17/06/202012:30
 * @Description: TODO
 * @Version V1.0
 **/
@Component// 告诉spring把类new一下
public class MyDemo {
	// 7个 年可以不写
	@Scheduled(cron = "*/5 * * * * ?")
	public void cron(){
		System.out.println("我执行了" + new Date());
	}
}
