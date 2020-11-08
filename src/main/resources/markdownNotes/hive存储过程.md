## mysql存储过程:

### 优点：

- 存储过程可封装，并隐藏复杂的商业逻辑。
- 存储过程可以回传值，并可以接受参数。
- 存储过程无法使用 SELECT 指令来运行，因为它是子程序，与查看表，数据表或用户定义函数不同。
- 存储过程可以用在**数据检验，强制实行商业逻辑**等。

### 缺点

- 存储过程，往往定制化于特定的数据库上，因为支持的编程语言不同。**当切换到其他厂商的数据库系统时，需要重写原有的存储过程**。
- 存储过程的**性能调校与撰写，受限于各种数据库**系统。

### 第一步：创建存储过程：

```sql
CREATE
    [DEFINER = { user | CURRENT_USER }]
-- 设置程序名
　procedure sp_name ([proc_parameter[,...]])
    [characteristic ...] routine_body
 --设置参数
proc_parameter:
    [ IN | OUT | INOUT ] param_name type
 
characteristic:
    COMMENT 'string'
  | LANGUAGE SQL
  | [NOT] DETERMINISTIC
  | { CONTAINS SQL | NO SQL | READS SQL DATA | MODIFIES SQL DATA }
  | SQL SECURITY { DEFINER | INVOKER }
 
routine_body:
　　Valid SQL routine statement
 
[begin_label:] BEGIN
　　[statement_list]
　　　　……
END [end_label]
```

```sql
DELIMITER $$ -- 声明语句结束符
```

声明存储过程:

```sql
CREATE PROCEDURE demo_in_parameter(IN p_in int)       
```

存储过程开始和结束符号:

```
BEGIN .... END    
```

变量赋值:

```sql
SET @p_in=1  
```

变量定义:

```sql
DECLARE l_int int unsigned default 4000000; 
```

创建mysql存储过程、存储函数:

```
create procedure 存储过程名(参数)
```

存储过程体:

hqlsql存储过程hive2.0