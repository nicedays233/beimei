## linux

sys1、网络配置
vi /etc/sysconfig/network-scripts/ifcfg-enp0s3

2、修改配置
BOOTPROTO=static
ONBOOT=yes
IPADDR=192.168.56.xxx

3、保存配置
首先使用esc(键退出)->:(符号输入)->wq(保存退出)

4、重启网络
systemctl restart network

5、测试网络连接
ping ![img](file:///C:\Users\lenovo\AppData\Roaming\Tencent\QQTempSys\[5UQ[BL(6~BS2JV6W}N6[%S.png)www.baidu.com

6、关闭和禁用防火墙
systemctl stop firewalld
systemctl disablefirewalld





>
>
>

- **在文档插入**

  1. **在首行插入**
     1. 没有1行 echo “内容” >>
     2. 如果你有1行 sed -i '1[i|a] 你的内容' 你的文件 i插行前 a插行
  2. **在文档尾部插入**
     1. echo “你的内容” >>  你的文件
  3. **在指定行前或后插入数据**
     1. sed -i '/你的正则行/[i|a] 你的内容'

- **在文档删除**

  1. **删除N行**\

     1. sed -i '行号d' 你的文件 （删除一定范围的行 '1,5d'）

  2. **删除最后一行**

     1. sed -i '$d' 你的文件

  3. **删除匹配的行**

     1. sed -i '/^文件行开头/d' 你的文件

     2. sed -i '/文件行结尾$/d' 你的文件

        

- **在文档中替换**

  1. **在每行前替换**

     1. sed -i '[行号]s/你的正则/替换结果/' 你的文件
     2. sed -i '[行号]s/替换的内容/想要替换结果/' 你的文件

     