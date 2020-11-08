##  ElasticSearch简介

####  ElasticSearch:（solr与Lucene与其类似）

-   是一个基于Lucene的搜索服务器(ES)---数据库
-   专门为分布式环境设计
-   封装了luence的检索细节，只是走restfulapi。
-   近乎实时的存储、检索数据；本身扩展性很好
-   通过简单的RESTful API来隐藏Lucene的复杂性
-   文件内容搜索的数据库----反向检索

Elasticsearch使用语言：

为什么要使用·elasticsearch？

**全文检索索引**：-**建一张**----**语义分析表** ----**hash字典表**---- **用空间换时间**                              -------oracle公司使用

- index：索引，由多个Document组成
- Type：索引类型，6.x仅支持一个，以后将逐渐被移除
- Document：文档，由多个Field组成
- Field：字段，包括字段名与字段值

|  RDBMS   | ElasticSearch |
| :------: | :-----------: |
| Database |     index     |
|  Table   |     Type      |
|   Row    |   Document    |
|  Column  |     Field     |



## ElasticSearch优缺点：

- 



##  ElasticSearch环境搭建

## ElasticSearch数据模型：

- index：索引，由多个document组成
- type：索引类型，6.x仅支持一个
- document：文档，由多个field组成
- Field：字段，包括字段名与字段值

| RDBMS    | ElasticSearch |
| -------- | ------------- |
| database | index         |
| table    | type          |
| row      | document      |
| column   | field         |



##  ElasticSearch用法

索引管理：

**分片：索引指向一个或多个分片得逻辑命名空间**，一篇文章拆成多份

**主分片数：默认分5片，索引首先被存储在主分片中，并复制相应得副本分片**

**副本分片：一旦主分片失效，副分片晋升为主分片**

主节点：负责创建索引，删除，分配分片数，追踪节点状态

节点：一个集群由多个节点组成，一个节点是es实例，默认每个节点都为候选主节点与数据节点



number_of_replicas副本数量

**ElasticSearchCRUD**：

**创建index（库）：**

```shell
# 通过hash映射来确定副本得存储位置
# 通过路由计算hash（routing） % number_of_primary_shards（分片）来得到存储得位置
# 建索引
PUT demo.1234
{
	"settings" :{
		"index" :{
			"number_of_shards" : 2, # 主分片数量 默认为5
			"number_of_replicas" : 2 # 副本数量，默认为1为不设
		}
	}
}
```

**创建Type（表）：**

postman上输入对应传送方式，URL

![image-20200526152538834](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200526152538834.png)

在body请求的raw处传送json格式：

![image-20200526151115060](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200526151115060.png)

在raw中输入json格式命令：

```shell
{
	"settings" : {
		# 加了index索引之后会硬盘
		# "index" : {}一般不加
		"number_of_shards" : 3, 
		"number_of_replicas" : 1
	},
	"mappings" : {
		# 建type 表
		"userinfos" : {
			# 建 document 行
			"properties" : {
				# 建 field 列
				"userid" : { "type" : "integer" },
				"username" : { "type" : "keyword" },
				"birthday" : {
					"type" : "date",
					"format" : "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
				},
				"say" : { "type" : "text" }
			}
		}
	}	
}
```

**Alert：添加或更改新字段**

![image-20200528084840308](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200528084840308.png)

```shell

{
	# document行
	"properties" : {
		# field字段名
		"say" : { "type" : "text" }
	}
}
```

```shell
# 修改字段属性使对应字段聚合开启，有的时候内
{
	"properties" : {
		"eventCateGory" : {
			"type" : "text",
			"fielddata" : true
		}
	}
}
```

Create：插入field信息**

 postman上输入对应传送方式，URL

![image-20200526151559030](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200526151559030.png)

在body请求的raw处传送json格式：

![image-20200526151115060](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200526151115060.png)

在raw中输入json格式命令：

```shell
{
	"settings" : {
		"number_of_shards" : 3, # 主分片为3
		"number_of_replicas" : 1 # 副本不设
	},
	"mappings" : {
		"userinfos" : {
			"properties" : {
				"userid" : { "type" : "integer" },
				"username" : { "type" : "keyword" },
				"birthday" : {
					"type" : "date",
					"format" : "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
				},
				"say" : { "type" : "text" }
			}
		}
	}	
}
```

**Update：更新field信息**

 postman上输入对应传送方式，URL中输入修改id和表和update命令

![image-20200526151640584](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200526151640584.png)

在body请求的raw处传送json格式：

![image-20200526151115060](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200526151115060.png)

在raw中输入json格式命令：

```shell
{
	"doc" : {
		"username" : "lisi"
	}
}
```

**Delete：删除field信息**

 postman上输入对应传送方式，URL中输入修改id和表

![image-20200526151957856](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200526151957856.png)

然后直接send即可删除

倒排索引：根据关键字找文章

将文章关键词分

**Read查找：**

![image-20200528090555682](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200528090555682.png)

- match_phrase短语查询：不能分割，需要连着查（认大小写也匹配）
- match_all：查所有
- match_phrase_prefix：短语前缀查询，前面都和match_phrase一样，最后一个分词作为前缀匹配
- match：布尔匹配查询：只要查到分词当中其中任意一个，就可以查到（认大小写也匹配）
- multi_match：多字段匹配查询

```shell
{
    "query": {
    	# 查询两个字段中是否都有该值的document
        "multi_match": {
          "query": "John like cooking",
          "fields": ["name","interest"]
        }
    }
}
```



- term：词条查询：查找**存储在倒排索引中**具体的确切词汇（不认大小写）
  - 如果你写how are ，这个直接算一个词来查。**严格精确查找**

```shell
{
	"query" : {
		"term" : {
			"msg" : "ccc"
		}
	}
}
```

- terms：多词条查询：多词--或者关系，其中一个成功即可

```shell
{
	"query" : {
		"term" : {
			"msg" : ["how","you"]
		}
	}
}

```

- range：范围查询

```shell
{
	"query" : {
		"range" : {
			"custid" : {
				"gte" : 15000, # 大于等于
				"lte" : 60000  # 小于等于
			}
		}
	}
}
```

- bool：布尔查询
  - must：必须符合，计算score
  - must：必须不符合
  - should：可以符合可以不符合--or
  - filter：必须符合，不计算score

```shell
{
	"query" : {
		"bool" : {
			"must" : [
				{
					"match" : {"browser" : "wyw1"}
					
				},
				{
					"match" : {"msg" : "huawei"}
				}
			],
			"must_not" : {
				"match" : {"browser" : "sohuwyw"}
			},
			"should" : [
				{
					"match" : {"eventCateGory" : "txt_input"}
				},
				{
					"match" : {"eventCateGory" : "button_click"}
				},
				{
						"match" : {"eventCateGory" : "href_click"}
				}
			],
			"filter" : [
				{
					"match" : {"browser" : "wyw1"}
					
				},
				{
					"match" : {"msg" : "huawei"}
				}
			]
		}
	}
}
```

- size：分页查询：

```shell
{
	"query" : {
		"bool" : {
		}
	},
	"size" : 5, # 每页显示量
	"from" : 10 # pagesize*(page-1)
}
```

- 聚合查询

```shell
{
    "aggs" : {
    	# 平均函数聚合
    	"avg_age" : {
    		"avg" : {
    			"field" : "age"
    		}
    	},
    	# 求和函数聚合
    	"sum_age" : {
    		"sum" : {
    			"field" : "age"
    		}
    	}
    }
}
```

groupby + count函数聚合：

```shell
{
	"size" : 0,
    "aggs" : {
    	"mybuckket" : {
    		"terms" : {
    			"field" : "name"
    		}	
    	}
    }
}
```

```shell
# 多字段分组 ，每个字段fielddata得开启
{
	"size" : 0,
	"aggs" : {
		"event_of_people" : {
			"terms" : {
				"script" : "doc['browser'].values+'##'+doc['eventCateGory'].values." 
				
			}	
		}
	}
}
```

```shell
# 截取时间字符串，script可以加java代码
{
	"size" : 0,
	"aggs" : {
		"event_of_people" : {
			"terms" : {
				"script" : "doc['time'].values[4] + doc['time'].values[3] + doc['time'].values[2] + '##' + doc['eventCateGory'].values" 
				
			}	
		}
	}
}
```

![image-20200528091325385](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200528091325385.png)



```SHELL
{
	"size" : 0,
    "aggs" : {
    	"mybuckket" : {
    		"terms" : {
    			"field" : "say"
    		}	
    	}
    }
}
```

![image-20200528092033255](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200528092033255.png)

## ElasticSearch工作原理

