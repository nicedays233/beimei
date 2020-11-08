### Inputformat的数据多种处理方式：

#### FileInputFormat：--处理文件

- `TextInputFormat:`
  - <偏移量，行数据>----LineRecordReader
- `KeyValueTextInputFormat:`
  - <分隔符前，分隔符后>----KeyValueLineRecordReader
- `NLineInputFormat:`
  - <偏移量，行数据>----LineRecordReader
- `CombineTextInputFormat：`
  - 用于处理小文件过多场景，将多个小文件逻辑规划到一个切片中。<偏移量，行数据>----LineRecordReader（跨文件了）
- `DBInputFormat：`
- `SequenceFileInputFormat:`
- `TableInputFormat：`

### Combiner类令人忽视的点：

- Combiner组件的父类是Reducer
- 但是Combiner是运行再MapTask节点上的

### 从Yarn角度看MapReduce流程：（再详细版）

---

**第一步：**Client向RM提交job请求，RM的app manager返回jobId和hdfs地址，Client将运行作业资源（分片信息，jar包，配置信息等）资源上传到hdfs上。

---

**第二步：**上传成功后，再向RM的app manager去申请执行作业的请求，app manager把请求转发给Scheduler调度器，调度器将请求放入调度队列，当到执行到某个请求时，调度器通知app manager区某个datanode上开辟一个容器container，通过nodemanager调用container去创建一个appmaster。

---

**第三步：**appmaster去拉取hdfs路径的提交文件信息来创建Map和reducetask，同时map和reduce执行需要计算资源，appmaster通过rpc协议通过轮询的方式向调度器申请运行map和reducetask计算资源，然后appmaster此时可以去通知nodemanager，让其启动任务了。

---

**第四步：** 任务从共享的hdfs上拉取执行的资源，开始任务，每个任务计算完毕后，map和reducetask将文件结果上传到hdfs的路径上，并向AppMaster发送成功信息，AppMaster向RM发送请求，请求注销自己，然后调度器再去执行下一个任务。

---