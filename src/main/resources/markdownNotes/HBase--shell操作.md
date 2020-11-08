## HBase--shell操作：

### 创建HBase表：

#### 创建简单表：

```shell
create '表名', {NAME => '列簇名1'},{NAME => '列簇名2'}......

# 简写版
create '表名', '列簇名1','列簇名2','列簇名3'

# 详细版
create '表名', {NAME => '列簇名1' ,VERSIONS => 版本号, TTL => 过期时间, BLOCKCACHE => true, 等等}

# 例子
create 't1', {NAME => 'f1', VERSIONS => 1, TTL => 2592000, BLOCKCACHE => true}
```

#### 

#### 创建命名空间：

```shell
create_namespace 'mydemo'
create_namespace 'mydemo' ,{"author" => "sch","create_time" => "2020-07-12"}
```

#### 查看命名空间：

```shell
list_namespace
```

#### 查看命名空间属性：

```shell
describe_namespace '命名空间名'
```

#### 修改命名空间：

```shell
alter_namespace 'test01', {METHOD => "set", "author" => "kgc"}
alter_namespace 'test01', {METHOD => "unset", "author" => "kgc"}
```

#### 删除命名空间：

```shell
drop_namespace 'xxx'
```



#### 创建带命名空间的表：

```shell
create '命名空间:表名', {NAME => '列簇名1' ,VERSIONS => 版本号, TTL => 过期时间, BLOCKCACHE => true, 等等}

# 例子
create 'mydemo:t1', {NAME => 'f1', VERSIONS => 1, TTL => 2592000, BLOCKCACHE => true}
```



### 查看HBase版本：

```shell
version
```

### 查看HBase状态：

```shell
status
```

### 查看HBase帮助文档：

```shell
help '命令名'
```

### 判断表是否存在：

```shell
exists '表名'
```

### 启用/禁用表：

```shell
enable '表名'
disable '表名'
```



### HBase查看表信息：

```shell
desc '表名'
```



### HBase添加：

```shell
put '表名','行键','列簇名:列名','列值'
```



### HBase修改：

- 修改列簇名

```shell
alter '表名','列簇名'
```

- 修改为多版本存储

```shell
alter ‘user’,{NAME => ‘列簇’, VERSIONS => 3}
```



### HBase查询：

#### scan扫描：

- 获取全表值

```shell
scan '表名'
```

- 获取某列簇的值

```shell
scan '表名', {COLUMN => '列簇名'}
```

- 获取某列名的值

```shell
scan '表名', {COLUMN => '列簇名:列名'}
```

- 指定rowkey范围查询

```shell
.scan ‘表名’, {STOPROW => ‘行键名’}
```



#### get获取：

- 获取行值

```shell
get '表名','行键'
```

- 获取某行的列簇值或列名值

```shell
get '表名','行键','列簇名:列名'
```

- 多版本获取那一行那一列的值数据

```shell
# 拿到最近的4个版本的那一行那一列的值
get '表名','行键','列簇名',{CLOUMN => '列名', VERSIONS => 4}
```



#### filter过滤获取：

`ValueFilter-值过滤：`

```shell
# binary 等于某个值显示出来，这里是binary是因为底层用二进制存储
get '表名','行键',{FILTER => "ValueFilter(=,'binary:值')"}

# substring：包含某个值显示出来
get '表名','行键',{FILTER => "ValueFilter(=,'subtring:值')"}
```

`ColumnPrefixFilter-列名前缀过滤：`

```shell
scan '表名', {FILTER => "ColumnPrefixFilter('列名前缀')"}

# 加and或者or混合使用
scan '表名', {FILTER => "ColumnPrefixFilter('列名前缀') AND ValueFilter(=,'subtring:26')"}
```



### HBase删除：

- 删除某一列

```shell
delete ‘表名’, ‘行键’, ‘列族名:列名’
```

- 删除某一列簇：

```shell
alter '表名', {NAME => '列簇名', METHOD => 'delete'}
```

- 删除表：删除表前先要禁用表

```shell
disable '表名'
drop '表名'
```

- 清空表

```shell
truncate '表名'
```



### 安全权限（Security with GRANT）

- grant命令进行授权管理
  - 如读，写，执行和管理等
- 我们可以为用户赋予RWXCA权限中得一个或多个

#### 权限管理命令：

- 使用grant命令授权
- 使用revoke命令删除权限
- 使用user——permission查看用户对表所拥有得权限