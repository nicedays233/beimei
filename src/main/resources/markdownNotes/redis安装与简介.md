## Redis安装与基本命令：

### Redis安装：

#### 第一步：下载redis安装包

```shell
wget http://download.redis.io/releases/redis-4.0.6.tar.gz
```

#### 第二步：解压压缩包并移动到指定目录

```shell
tar -zxvf redis-4.0.6.tar.gz
mv redis-4.0.6 /opt/soft/redis406
```

#### 第三步：yum安装gc依赖

```shell
yum install gcc
```

#### 第四步：跳转到redis解压目录下

```shell
cd redis-4.0.6
```

#### 第五步：编译安装

```shell
make MALLOC=libc
```

#### 第六步：修改redis.conf文件

```shell
vi /opt/soft/redis406/redis.conf
将daemonize no改为daemonize yes
添加需要绑定的主机
bind 192.168.56.101
```

#### 第七步：到src目录启动redis

```shell
./redis-server /opt/soft/redis406/redis.conf
```

#### 第八步：开启另一个窗口在src下启动命令行

```shell
./redis-cli -h 192.168.56.101 -p 6379
```



### Redis数据类型：

> Redis支持5种数据类型：string，hash，list，set，zset

#### String：

> 存字符串， 一个键最大能存512MB

- 塞字符串

```shell
set rediskey "value"
```

- 拿字符串

```shell
get rediskey
# value
```



#### Hash：

> 存键值对集合

- 存键值对

```shell
hmset rediskey hashkey1 "hashvalue1" hashkey2 "hashvalue2"
```

- 拿键值对

```shell
hget rediskey hashkey1
# "hashvalue1"
```

> 每个hash可以存储2^32 - 1键值对

#### List：

> Redis 列表是简单的字符串列表
>
> 按照插入顺序排序
>
> 你可以添加元素到列表的头部（左边）或者尾部（右边）

- 塞列表

```shell
lpush rediskey wyw1
#(integer) 1
lpush rediskey hsc
#(integer) 2
```

- 拿列表

```shell
lrange rediskey 0 10
1)wyw1
2)hsc
```

> 列表最多可存储2^32 - 1元素

#### Set：

> redis的set时string类型的无序集合
>
> 集合是通过哈希表实现的，所以添加，删除，查找的复杂度都是 O(1)

- 塞集合

```shell
sadd key member
```

- 拿集合

```shell
 smembers key
```



### redis常见命令：

#### redis键值命令：

- `expire key seconds`
  - 为给定 key 设置过期时间，以秒计。
- `del key`
  - 该命令用于在 key 存在时删除 key。
- `exists key`
  - 检查给定 key 是否存在。

#### redis字符串命令：

- `set key value`
  - 设置指定 key 的值
- `get key`
  - 获取指定 key 的值。
- `getrange key start end`
  - 返回 key 中字符串值的子字符
- `getset key value`
  - 将给定 key 的值设为 value ，并返回 key 的旧值(old value)。
- `mget key1 key2`
  - 获取所有(一个或多个)给定 key 的值。
- `setex key seconds value`
  - 将值 value 关联到 key ，并将 key 的过期时间设为 seconds (以秒为单位)。
- `setnx key value`  
  - 只有在 key 不存在时设置 key 的值。
- `strlen key`
  - 返回 key 所储存的字符串值的长度。
- `incr key`
  - 将 key 中储存的数字值增一
- `decr key`
  - 将 key 中储存的数字值减一
- `append key value`
  - 如果 key 已经存在并且是一个字符串， APPEND 命令将指定的 value 追加到该 key 原来值（value）的末尾

#### redis哈希命令：

- `hdel key field1 field2`
  - 删除一个或多个哈希表字段
- `hexists key field`
  - 查看哈希表 key 中，指定的字段是否存在。
- `hget key field`
  - 获取存储在哈希表中指定字段的值。
- `hgetall key`
  - 获取在哈希表中指定 key 的所有字段和值
- `hkeys key`
  - 获取所有哈希表中的字段
- `hlen key`
  - 获取哈希表中字段的数量
- `hmget key field1 field2`
  - 获取所有给定字段的值
- `hmset key field1 value1 field2 value2..`
  - 同时将多个 field-value (域-值)对设置到哈希表 key 中。
- `hvals key`
  - 获取哈希表中所有值。

#### redis列表命令：

- `lrem key count value`
  - 对一个列表进行修剪(trim)，就是说，让列表只保留指定区间内的元素，不在指定区间之内的元素都将被删除。
- `linsert key before|after value`
  - 在列表的元素前或者后插入元素
- `lindex key index`
  - 通过索引获取列表中的元素
- `llen key`
  - 获取列表长度
- `lpush`
  - 将一个或多个值插入到列表头部
- `ltrim key start stop`
  - 对一个列表进行修剪(trim)，就是说，让列表只保留指定区间内的元素，不在指定区间之内的元素都将被删除。
- `lset key index value`
  - 通过索引设置列表元素的值
- `lpop key`
  - 移出并获取列表的第一个元素
- `lrange key start stop`  
  - 获取列表指定范围内的元素
- `lset key index value`
  - 通过索引设置列表元素的值
- `drop key`
  - 移除列表的最后一个元素，返回值为移除的元素。

#### redis集合命令：

- `sadd key member1 member2`
  - 向集合添加一个或多个成员

- `scard key`
  - 获取集合的成员数
- `sdiff key1 key2`
  - 返回第一个集合与其他集合之间的差异
- `sidffstore key3 key1 key2`
  - 返回给定所有集合的差集并存储在 destination 中
- `sinter key1 key2`
  - 返回给定所有集合的交集
- `sinterstore key3 key1 key2`
  - 返回给定所有集合的交集并存储在 destination 中
- ``sunion key1 key2``
  - 返回所有给定集合的并集
- `sunionstore key3 key1 key2`
  - 所有给定集合的并集存储在 destination 集合中
- `spop key`
  - 移除并返回集合中的一个随机元素
- `smembers key`
  - 返回集合中的所有成员

