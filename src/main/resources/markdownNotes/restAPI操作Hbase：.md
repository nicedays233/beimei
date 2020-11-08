## restAPI操作Hbase：

### 创建表

```shell
curl -v -X PUT \
  'http://localhost:9081/test/schema' \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"@name":"test","ColumnSchema":[{"name":"data"}]}'
```

> Store value '$(decode $DATA)' in column '$(decode $COLUMN)' as row 'row1'"

> The row, column qualifier, and value must each be Base-64 encoded

-----------------------------------------------------------------------------

### 插入命令：

> KEY=$(openssl enc -base64 <<< 'row1')
> COLUMN=$(openssl enc -base64 <<< 'data:test')
> DATA=$(openssl enc -base64 <<< 'some data')

```shell
# 将5个变量base-64加密
TABLE='test'
FAMILY='data'
KEY=$(echo 'row1' | tr -d "\n" | base64)
COLUMN=$(echo 'data:test' | tr -d "\n" | base64)
DATA=$(echo 'Some More Data' | tr -d "\n" | base64)
echo $KEY
echo $COLUMN
echo $DATA
```



```shell
curl -v -X PUT \
  'http://localhost:9081/test/row1/data:test' \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"Row":[{"key":"'$KEY'","Cell":[{"column":"'$COLUMN'", "$":"'$DATA'"}]}]}'
```

> Get row 'row1' from table 'test'

-----------------------------------------------------------------------------

### 获取一条数据：

```shell
curl -v -X GET \
  'http://localhost:9081/test/row1' \
  -H "Accept: application/json"
```

Delete table 'test'

-----------------------------------------------------------------------------



### 删除一条数据或表：

```shell
curl -v -X DELETE \
  'http://localhost:9081/test/schema' \
  -H "Accept: application/json"
```

