





![ ](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200720111001094.png)

```shell

##通过shell导入文档数据到hbase
hbase org.apache.hadoop.hbase.mapreduce.ImportTsv \
-Dimporttsv.separator=','  \
-Dimporttsv.columns="HBASE_ROW_KEY,order:numb,order:date" \
customer file:///home/vagrant/hbase_import_data.csv
# file路径为虚拟机路径
```

