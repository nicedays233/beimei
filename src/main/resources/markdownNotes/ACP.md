## ACP：

1. 创建表用like语句时，列注释，分区，表注释会被复制到新表上。

2. like时关键字，无法命名

3. 使用mapjoin hint时，语法上可以允许没有连接条件

   没有mapjoin hint时，多个连接条件之间必须是and关系

   没有mapjoin hint时，必须时等值连接

4. 通过sql读取分区表中的数据时，可以通过指定分区的方法只读取一部分分组，减少io开销

   可以单独处理指定分区中的数据，不会对其他分区数据产生影响

   对于过期的数据可以将对应的分区drop掉，不会影响其他分区中的数据

5. 云盾加密采用了**符合国家密码管理局要求的算法**来保证机制密钥的安全

6. mysql为**binlog日志**，sqlserver为**事务日志**

7. odps**屏显行数最大为5000**

8. 云监控产品的监控数据可以用**管理控制台和openAPI**两种方式下载

9. **磁盘空间**能标识RDS实例磁盘空间的使用量

10. **文件压缩**是odps的mapreduce不支持

11. odps的acl授权不包括**限制条件**这个操作

12. 多可用区RDS可以**轻松实现同城容灾**

13. RDS实例所选择的**内存大小**决定了该实例的最大连接数

14. ADS中表组在创建时需要指定**executeTimeout & minRedundancy**两个参数

15. OTS API单行操作不包括**postrow**

16. **效果** 不属于ODPS访问策略的访问控制元素

17. RDS mysql不支持**memory引擎**

18. odps用户定义标量函数可以**实现evaluate方法**

19. desc role role_test可查看角色role_test权限

20. 对于批量插入的表可以**二级list分区**，二级list分区是**非动态分区，分区值由用户导入时指定**。

21. ![image-20201007100128797](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007100128797.png)

22. odps的DDL操作，是由**worker**那层完成

23. **jar包**不属于odps项目空间的对象类型

24. **accountID**不属于构造此对象时必须提供的信息

25. DRDS默认每个实例**创建8个数据库**

26. 网络安全专家服务是阿里云云盾**安骑士**服务基础上，推出的安全代为托管服务。

27. 当一个用户被移除后与该用户有关的**acl授权**会保留

28. **数据库**是用户所关心的最大单元，也是用户和ads系统管理员的分界点

29. 阿里绿网**帮助用户检查网站内容的合规性，包括文字内容和图片**

30. OTS拼接是为了**解决单个分片键下数据量过大的问题**

31. ![image-20201007104437075](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007104437075.png)

32. **对ACL授权过的表重建，**会使授权失效

33. DRDS事务支持**最终一致性事务**

34. ![image-20201007104645810](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007104645810.png)

35. ADS的**高度智能优化策略是CBO**

36. 每个权限级别**能聚合其下面级别的所有权限**

37. ![image-20201007104822423](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007104822423.png)

38. ![image-20201007104929338](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007104929338.png)

39. ![image-20201007105043006](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007105043006.png)

40. OTS pythoncli 需要2.7py支持

41. OTS单表存储没有上限

42. ![image-20201007105502934](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007105502934.png)

43. **mysql5.0**不支持在线迁移

44. odps一个表上限最多拥有**60000个分区**

45. 分担RDS主实例的写压力适合RDS只读实例来完成

46. **大数据风控服务**可以开发云盾反欺诈服务。

47. web应用采用**javascript**接入云顿反欺诈服务

48. ![image-20201007105826720](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007105826720.png)

49. ADS表一级分区数据**不超过800万条**，分区数**不能超过256个**

50. OTS单个表包括**无限制的属性列**

51. sql优化特别要考虑**网络IO开销**

52. ADS表遵循最终一致性

53. ![image-20201007110114935](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007110114935.png)

54. ![image-20201007110235259](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007110235259.png)

55. ![image-20201007110305694](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007110305694.png)

56. **防web应用系统密码破解**不是安骑士包含的功能

57. ![image-20201007110401224](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007110401224.png)

58. 一个mysql数据实例最多可以**创建500个数据库**

59. RDS连接闪断发生时，**主库出现故障**的原因可能是实例本身故障

    ![image-20201007110644435](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007110644435.png)

60. ![image-20201007110706863](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007110706863.png)

61. ![image-20201007110723336](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007110723336.png)

62. ![image-20201007110751894](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007110751894.png)

    ![image-20201007110843752](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007110843752.png)

63. **独立白名单配置**只读实例可以使用

64. DRDS不具备**智能索引的特性**

65. **有效控制云产品间的网络延迟**属于多可用区的RDS

66. ![image-20201007111105947](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007111105947.png)

67. ![image-20201007111134163](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007111134163.png)

68. ![image-20201007111242744](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007111242744.png)

69. ![image-20201007111316269](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007111316269.png)

70. ![image-20201007111357470](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007111357470.png)

71. ![image-20201007111448805](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007111448805.png)

72. ![image-20201007111546022](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007111546022.png)

73. ![image-20201007111637213](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007111637213.png)

74. ![image-20201007111856312](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007111856312.png)

75. ![image-20201007112101891](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007112101891.png)

76. ![image-20201007112548743](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007112548743.png)

77. ![image-20201007112611528](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201007112611528.png)

78. ![image-20201009105357192](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201009105357192.png)

![image-20201009105424140](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201009105424140.png)

![image-20201009105550046](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201009105550046.png)

![image-20201009105640061](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201009105640061.png)

![image-20201009105702493](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201009105702493.png)

![image-20201009105734700](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201009105734700.png)

![image-20201009105756265](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201009105756265.png)

![image-20201009105812976](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201009105812976.png)

![image-20201009105841971](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201009105841971.png)

![image-20201009105926118](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201009105926118.png)

![image-20201009105947472](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201009105947472.png)

![image-20201009110029036](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201009110029036.png)

![image-20201009110043660](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201009110043660.png)

![image-20201009110206762](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201009110206762.png)

![image-20201009110402693](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201009110402693.png)

![image-20201009110426332](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201009110426332.png)

![image-20201009110524780](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201009110524780.png)

![image-20201011174634591](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011174634591.png)

![image-20201011174651192](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011174651192.png)

![image-20201011174751074](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011174751074.png)

![image-20201011174803401](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011174803401.png)

![image-20201011174819814](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011174819814.png)

![image-20201011174912526](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011174912526.png)

![image-20201011174928044](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011174928044.png)

![image-20201011174947744](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011174947744.png)

![image-20201011175155560](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011175155560.png)

![image-20201011175209033](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011175209033.png)

![image-20201011175224493](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011175224493.png)

![image-20201011175250761](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011175250761.png)

![image-20201011230638488](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011230638488.png)

![image-20201011230741718](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011230741718.png)

![image-20201011230818547](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011230818547.png)

![image-20201011230901087](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011230901087.png)

![image-20201011231012186](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011231012186.png)

![image-20201011231042119](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011231042119.png)

![image-20201011231141948](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011231141948.png)

![image-20201011231158598](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011231158598.png)

![image-20201011231241704](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011231241704.png)

![image-20201011231309886](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011231309886.png)

![image-20201011231341204](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011231341204.png)

![image-20201011231407831](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011231407831.png)

![image-20201011231437729](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011231437729.png)

![image-20201011231612057](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011231612057.png)

![image-20201011231658838](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011231658838.png)

![image-20201011231824858](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011231824858.png)

![image-20201011231900208](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011231900208.png)

![image-20201011231946214](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011231946214.png)

![image-20201011232005300](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011232005300.png)

![image-20201011232022098](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011232022098.png)

![image-20201011232657377](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011232657377.png)

![image-20201011232744770](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011232744770.png)

![image-20201011232803454](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011232803454.png)

![image-20201011232835377](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011232835377.png)

![image-20201011233008945](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011233008945.png)

![image-20201011233113326](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011233113326.png)

![image-20201011233122392](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011233122392.png)

![image-20201011233134712](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011233134712.png)

![image-20201011233151978](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011233151978.png)

![image-20201011233221275](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011233221275.png)

![image-20201011233248824](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201011233248824.png)87 u

![image-20201012233052386](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201012233052386.png)

