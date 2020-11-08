## Logstash入门：

#### **一：imput标准输入输出命令：**

**./logstash -e 'input { stdin {} } output { stdout {codec => rubydebug}}'**// 使用给定的字符串

```shell
# 将其写在配置文件config里
input {
        stdin {}
}
output {
        stdout {
                codec => rubydebug
        }
}
```

![image-20200601095029176](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200601095029176.png)

#### **二：file读取配置文件封装命令：**

**./logstah -f** // 读取配置文件

```shell
input {
        file {
                path => "/opt/aa.txt"
                start_position => "beginning"
                sincedb_path => "/dev/null"  // 不管对文件修不修改，每次读取此文件时，都会读取一遍，不加的话只有文件修改过后才会被全量读取。
        }
}
output {
        stdout {
                codec => rubydebug
        }
}
```

#### **三：filter过滤器的用法：**

##### **1.JSON字符串过滤**

- **mutate过滤器**：
  - 能够帮助你修改指定字段的内容。

```shell
# 将嵌套JSON扁平化
input {
        file {
                path => "/opt/aa.txt"
                start_position => "beginning"
                sincedb_path => "/dev/null" 
                codec => json
        }
}
filter {
        mutate {
                add_field => { '@adv' => '%{cm}' } # 先新建一个新的字段，并将friends赋值给它
        }
        json {
                source => "@adv" # 对字段再进行json格式解析
                remove_field => [ "@adv" , "cm" ] # 删除不必要的字段，也可以不用这语句
        }
}
```

**第一步：** add_field 新建表名

![image-20200525160241076](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200525160241076.png)

**第二步：**source 再次对其解析成json

![image-20200525160350600](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200525160350600.png)

**第三步：**remove_field 对多余的cm和@adv字段进行删除

##### **2.正则匹配过滤**

- **grok语法**：
  - 正则匹配：

```
(?<字段名>正则表达式)
```

```
# IP和NUMBER是预先定好的正则表达式
%{IP:字段名}\|%{NUMBER:字段名}
```

​		

##### **3.多文件和多过滤：**

```shell
input {
        file {
                path => "/opt/bb.txt"
                start_position => "beginning"
                sincedb_path => "/dev/null"
                type => "action"
                codec => json
        }
        file {
                path => "/opt/aa.txt"
                start_position => "beginning"
                sincedb_path => "/dev/null"
                type => "system"
        }
}
filter {
        if [type] == "system" {
                grok {
                        match => { "message" => "(?<userid>[0-9]+)\|(?<event_name>[a-zA-Z_]+)\|(?<times>[0-9]+)\|(?<clientip>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})" }
                remove_field => [ "message" ]
                }
        } else {
                mutate {
                        add_field => { "nice" => "%{cm}" }
                }
                json {
                        source => "nice"
                        remove_field => [ "nice" , "cm" ]
                }
        }
}
output {
        stdout {
                codec => rubydebug
        }
}

```

**4.输出到Elasticsearch**

```shell
input {
        file {
                path => "/opt/bb.txt"
                start_position => "beginning"
                sincedb_path => "/dev/null"
                type => "action"
                codec => json
        }
        file {
                path => "/opt/aa.txt"
                start_position => "beginning"
                sincedb_path => "/dev/null"
                type => "system"
        }
}
filter {
        if [type] == "system" {
                grok {
                        match => { "message" => "(?<userid>[0-9]+)\|(?<event_name>[a-zA-Z_]+)\|(?<times>[0-9]+)\|(?<clientip>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})" }
                remove_field => [ "message" ]
                }
        } else {
                mutate {
                        add_field => { "nice" => "%{cm}" }
                }
                json {
                        source => "nice"
                        remove_field => [ "nice" , "cm" ]
                }
        }
}
output {
        if [type] == "system" {
                elasticsearch {
                        hosts => "http://192.168.56.101:9200" #ip位置
                        index => "systems" # es的索引--库
                        document_type => "sys" # es的type--表
                }
        } else {
                elasticsearch {
                        hosts => "http://192.168.56.101:9200"
                        index => "customs"
                        document_type => "actions"
                }
        }
}

```

