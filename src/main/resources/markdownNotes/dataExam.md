## DataExam:

### 1.请在 HDFS 中创建目录/app/data/exam，并将 answer_question.log 传到该目录。 

```shell
hdfs dfs -mkdir -p /app/data/exam
```

```shell
hdfs dfs -put /opt/answer_question.log /app/data/exam
```

### 2.在 Spark-Shell 中，加载 HDFS 文件系统 answer_question.log 文件，并使用 RDD 完成 以下分析，也可使用 Spark 的其他方法完成数据分析。（20 分）

-  提取日志中的**知识点 ID，学生 ID，题目 ID**，作答结果 4 个字段的值 

- ②将提取后的**知识点ID，学生ID，题目ID**，作答结果字段的值以文件的形式保存到HDFS的/app/data/result 目录下。

- **一行保留一条数据，字段间以“\t”分割**。文件格式如下所示。 

  > （提示：元组可使用 tuple.productIterator.mkString("\t")组合字符串，使用其他方法处理数据只要结果正确也给分）

```scala
 val rdd = sc.textFile("hdfs://192.168.56.101:9000/app/data/exam/answer_question.log")
    rdd.map{line => {
        var datas = line.split(" ")
        var arr = datas(9).split("_")
      (arr(1), arr(2), arr(3).replace("r", ""), datas(10).split(",")(0)).productIterator.mkString("\\t")
    }}.saveAsTextFile("hdfs://192.168.56.101:9000/app/data/exam/result")
  }
```

### 3.创建 HBase 数据表（10 分） 

- 在 HBase 中**创建命名空间（namespace）exam**

- 在该命名空间下**创建 analysis 表**

- 使用 **学生 ID 作为 RowKey**，

- 该表下有 **2 个列族 accuracy、question。**

- **accuracy** 列族用于**保存 学 员 答 题 正 确 率 统 计 数 据**

  > （ 总 分 accuracy:total_score ， 答 题 的 试 题 数 accuracy:question_count，正确率 accuracy:accuracy）；
  >
  > question 列族用于分类保存学员正确，错误和半对的题目 id（正确 question:right，错误 question:error，半对 question:half

```shell
zkServer.sh start
start-hbase.sh
hbase shell

```

```shell
create_namespace 'exam1'
create 'exam1:analysis','accuracy','question'
```



### 4.请在 Hive 中创建数据库 exam

- 在该数据库中**创建外部表 ex_exam_record 指向 /app/data/result下Spark处理后的日志数据** 
- **创建外部表ex_exam_anlysis映射至HBase 中的 analysis 表**的 accuracy 列族
- **创建外部表 ex_exam_question 映射至 HBase 中的 analysis 表**的 question 列族（20 分）

```sql
create external table if not exists ext_exam_analysis(
    student_id string,
    total_score float,
    question_count int,
    accuary float
)
stored by 'org.apache.hadoop.hive.hbase.HBaseStorageHandler' 
with serdeproperties("hbase.columns.mapping"=":key,accuracy:total_score,accuracy:question_count,accuracy:accuracy") 
tblproperties("hbase.table.name"="exam1:analysis")
```

```sql
create external table if not exists ex_exam_question(
    student_id string,
    right string,
    half string,
    error float
)
stored by 'org.apache.hadoop.hive.hbase.HBaseStorageHandler' 
with serdeproperties("hbase.columns.mapping"=":key,question:right,question:half,question:error") 
tblproperties("hbase.table.name"="exam1:analysis")
```

### 5.使用 ex_exam_record 表中的数据统计

- 每个学员总分、答题的试题数和正确率

- 并保存 到 ex_exam_anlysis 表中
- 其中正确率的计算方法如下： 正确率=总分/答题的试题数 

```sql
insert overwrite table ext_exam_analysis
select *, (s.total_score/s.question_count) as accuracy from (select student_id, sum(score) as total_score, count(topic_id) as question_count from exam_record t1 group by student_id) s
```

### 6.使用 ex_exam_record 表中的数据统计

- 每个作对，做错，半对的题目列表。 
- ①题目 id 以逗号分割，并保存到 ex_exam_question 表中。（10 分）
- ②完成统计后，在 HBaseShell 中遍历 exam:analysis 表并只显示 question 列族中的数据， 如下图所示（10 分）

```sql
select
s.student_id,
(case when s.score = 1 then tm else '' end) as right,
(case when  s.score = 0.5 then tm else '' end) as half,
(case when s.score = 0 then tm else ''  end) as error
from
(select concat_ws(',',collect_set(question_id)) as tm,student_id,score from exam_record group by student_id,score) s
group by s.student_id
```

- 扫描hbase

```sql
scan 'exam:analysis', {COLUMNS => ['question']}
```

