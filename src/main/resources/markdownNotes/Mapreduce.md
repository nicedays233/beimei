## MapReduce的基本原理：



#### map+reduce：

<img src="C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200604190107994.png" alt="image-20200604190107994" style="zoom:67%;" />

#### MapReduce全流程：

1.有一个待处理的文本200M——>我们首先客户端submit提交流程，获取待处理的信息，

2.然后根据参数配置，形成一个任务分配的规划（切片）0-128，128-200。当中有可能产生数据迁移。

3.在提交给yarn之前，先完成基本文件的设置（1。xml文件2。分片信息，完整的jar包），

4.YARN(RM)拿到切片信息nodemanager计算出maptask数量，maptask拿到数据后inputformat生成一个recorderReader，

5.recordreader负责把maptask的一个切片处理成k，v值，交给maptask的mapper，

6.mapper里的逻辑处理完后，context.write（k,v），写给outputCollector，然后它传给环形缓冲区，

7.缓冲区总有一天会满，达到它的80%，先在内存进行快排使其有序，满了要写磁盘上，形成文件，数据全部拿到后，

8.因为数据量较大，不能在内存里排序，在磁盘对key归并排序，然后变成了按key有序，自然而然就完成了分组，

9.现在多个maptask得到了归并有序，全部给了reducetask，reducetask在以此再次进行一次归并排序，得到了有序的相同key不同values，交给redeucer，

10.reducer通过context write（k，v）交给outputformat，opf生成recordwriter，然后write输出结果





#### 环状缓冲区：

空间换时间，协调

#### Hadoop V1 MR 引擎

- Job tracker
  - 运行在namenode
  - 接受客户端job请求
  - 提交给task tracker
- task tracker
  - 从job tracker接受任务请求
  - 执行map，reduce等操作
  - 返回心跳给job tracker



#### Hadoop V2 YARN--升级

![image-20200605133302445](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200605133302445.png)

#### 数据倾斜产生原因：---hive的表格可以看出来

大量空值，导致某些节点负担重，有些节点负担轻。

#### 解决办法：

加盐或者随机分区

**map join**

没有reduce过程，所有的工作都在map阶段完成，极大减少了网络传输和io的代价。如何实现：

**上述的join过程可以看作外表与内表的连接过程，外表是订单表，外表大，内表是商品表，内表小。**所以可以把内表事先缓存于各个maptask结点，然后等到外表的数据传输过来以后，直接用外表的数据连接内表的数据并输出即可

Map端join是指只有map工作，reduce不工作，这样可以有效的避免数据倾 斜。



任务提交：

`waitforcompletion()`

```java
public boolean waitForCompletion(boolean verbose
                                   ) throws IOException, InterruptedException,
                                            ClassNotFoundException {
    // 定义过job后就是define状态
    if (state == JobState.DEFINE) {
      // 提交的方法
      submit();
    }
    if (verbose) {
      monitorAndPrintJob();
    } else {
      // get the completion poll interval from the client.
      int completionPollIntervalMillis = 
        Job.getCompletionPollInterval(cluster.getConf());
      while (!isComplete()) {
        try {
          Thread.sleep(completionPollIntervalMillis);
        } catch (InterruptedException ie) {
        }
      }
    }
    return isSuccessful();
  }
```

`submit()`

```java
// submit具体方法
public void submit() 
         throws IOException, InterruptedException, ClassNotFoundException {
    // 再次确认job状态
    ensureState(JobState.DEFINE);
    // 将旧的api封装成新的api，兼容旧代码
    setUseNewAPI();
    // 连接集群
    connect();
    // 拿到任务提交人，进行提交任务
    final JobSubmitter submitter = 
        getJobSubmitter(cluster.getFileSystem(), cluster.getClient());
    status = ugi.doAs(new PrivilegedExceptionAction<JobStatus>() {
      public JobStatus run() throws IOException, InterruptedException, 
      ClassNotFoundException {
        
        return submitter.submitJobInternal(Job.this, cluster);
      }
    });
    state = JobState.RUNNING;
    LOG.info("The url to track the job: " + getTrackingURL());
   }


// connect具体方法
  private synchronized void connect()
          throws IOException, InterruptedException, ClassNotFoundException {
    // 没有集群时生成集群
    if (cluster == null) {
      // 做判断究竟是本地的还是yarn的集群，来新建对应的集群
      cluster = 
        ugi.doAs(new PrivilegedExceptionAction<Cluster>() {
                   public Cluster run()
                          throws IOException, InterruptedException, 
                                 ClassNotFoundException {
                     return new Cluster(getConfiguration());
                   }
                 });
    }
  }

```

`submitJobInternal()`

```java
// 通过任务提交人提交状态，内部提交job
JobStatus submitJobInternal(Job job, Cluster cluster) 
  throws ClassNotFoundException, InterruptedException, IOException {

    // validate the jobs output specs 
    // 检查  
    checkSpecs(job);

    Configuration conf = job.getConfiguration();
    addMRFrameworkToDistributedCache(conf);

    Path jobStagingArea = JobSubmissionFiles.getStagingDir(cluster, conf);
    //configure the command line options correctly on the submitting dfs
    InetAddress ip = InetAddress.getLocalHost();
    if (ip != null) {
      submitHostAddress = ip.getHostAddress();
      submitHostName = ip.getHostName();
      conf.set(MRJobConfig.JOB_SUBMITHOST,submitHostName);
      conf.set(MRJobConfig.JOB_SUBMITHOSTADDR,submitHostAddress);
    }
    // 让yarn集群给job获取身份证编号
    JobID jobId = submitClient.getNewJobID();
    job.setJobID(jobId);
    // 有了jobid，yarn就会准备一个临时文件夹，要运行job的必要文件提交到job文件夹下面
    Path submitJobDir = new Path(jobStagingArea, jobId.toString());
    JobStatus status = null;
    try {
      conf.set(MRJobConfig.USER_NAME,
          UserGroupInformation.getCurrentUser().getShortUserName());
      conf.set("hadoop.http.filter.initializers", 
          "org.apache.hadoop.yarn.server.webproxy.amfilter.AmFilterInitializer");
      conf.set(MRJobConfig.MAPREDUCE_JOB_DIR, submitJobDir.toString());
      LOG.debug("Configuring job " + jobId + " with " + submitJobDir 
          + " as the submit dir");
      // get delegation token for the dir
      TokenCache.obtainTokensForNamenodes(job.getCredentials(),
          new Path[] { submitJobDir }, conf);
      
      populateTokenCache(conf, job.getCredentials());

      // generate a secret to authenticate shuffle transfers 给了一个可信的shuffle令牌
      if (TokenCache.getShuffleSecretKey(job.getCredentials()) == null) {
        KeyGenerator keyGen;
        try {
         
          int keyLen = CryptoUtils.isShuffleEncrypted(conf) 
              ? conf.getInt(MRJobConfig.MR_ENCRYPTED_INTERMEDIATE_DATA_KEY_SIZE_BITS, 
                  MRJobConfig.DEFAULT_MR_ENCRYPTED_INTERMEDIATE_DATA_KEY_SIZE_BITS)
              : SHUFFLE_KEY_LENGTH;
          keyGen = KeyGenerator.getInstance(SHUFFLE_KEYGEN_ALGORITHM);
          keyGen.init(keyLen);
        } catch (NoSuchAlgorithmException e) {
          throw new IOException("Error generating shuffle secret key", e);
        }
        SecretKey shuffleKey = keyGen.generateKey();
        TokenCache.setShuffleSecretKey(shuffleKey.getEncoded(),
            job.getCredentials());
      }
	 // 
      copyAndConfigureFiles(job, submitJobDir); 
      Path submitJobFile = JobSubmissionFiles.getJobConfPath(submitJobDir);
      
      // Create the splits for the job
      LOG.debug("Creating splits at " + jtFs.makeQualified(submitJobDir));
      // 切片规则的方法  
      int maps = writeSplits(job, submitJobDir);
      // 把切片的数量设置成maps的数量
      conf.setInt(MRJobConfig.NUM_MAPS, maps);
      LOG.info("number of splits:" + maps);

      // write "queue admins of the queue to which job is being submitted"
      // to job file.
      String queue = conf.get(MRJobConfig.QUEUE_NAME,
          JobConf.DEFAULT_QUEUE_NAME);
      AccessControlList acl = submitClient.getQueueAdmins(queue);
      conf.set(toFullPropertyName(queue,
          QueueACL.ADMINISTER_JOBS.getAclName()), acl.getAclString());

      // removing jobtoken referrals before copying the jobconf to HDFS
      // as the tasks don't need this setting, actually they may break
      // because of it if present as the referral will point to a
      // different job.
      TokenCache.cleanUpTokenReferral(conf);

      if (conf.getBoolean(
          MRJobConfig.JOB_TOKEN_TRACKING_IDS_ENABLED,
          MRJobConfig.DEFAULT_JOB_TOKEN_TRACKING_IDS_ENABLED)) {
        // Add HDFS tracking ids
        ArrayList<String> trackingIds = new ArrayList<String>();
        for (Token<? extends TokenIdentifier> t :
            job.getCredentials().getAllTokens()) {
          trackingIds.add(t.decodeIdentifier().getTrackingId());
        }
        conf.setStrings(MRJobConfig.JOB_TOKEN_TRACKING_IDS,
            trackingIds.toArray(new String[trackingIds.size()]));
      }

      // Set reservation info if it exists
      ReservationId reservationId = job.getReservationId();
      if (reservationId != null) {
        conf.set(MRJobConfig.RESERVATION_ID, reservationId.toString());
      }

      // Write job file to submit dir    
      // core-default  hdfs-default  
      // mapred-default yarn-default 4个xml配置
      // 还有切片和切片元信息和校验文件都在这个文件夹下
      // 把配置文件写在job临时文件夹下
      writeConf(conf, submitJobFile);
      
      // 
      // Now, actually submit the job (using the submit name)
      //
      printTokens(jobId, job.getCredentials());
      status = submitClient.submitJob(
          jobId, submitJobDir.toString(), job.getCredentials());
      if (status != null) {
        return status;
      } else {
        throw new IOException("Could not launch job");
      }
    } finally {
      if (status == null) {
        LOG.info("Cleaning up the staging area " + submitJobDir);
        if (jtFs != null && submitJobDir != null)
          jtFs.delete(submitJobDir, true);

      }
    }
  }
```

`writeSplits()`

```java
private int writeSplits(org.apache.hadoop.mapreduce.JobContext job,
      Path jobSubmitDir) throws IOException,
      InterruptedException, ClassNotFoundException {
    JobConf jConf = (JobConf)job.getConfiguration();
    int maps;
    if (jConf.getUseNewMapper()) {
      maps = writeNewSplits(job, jobSubmitDir);
    } else {
      maps = writeOldSplits(jConf, jobSubmitDir);
    }
    return maps;
  }
```

`writeNewSplits()`

```java
 private <T extends InputSplit>
  int writeNewSplits(JobContext job, Path jobSubmitDir) throws IOException,
      InterruptedException, ClassNotFoundException {
    Configuration conf = job.getConfiguration();
    // inputformat的一个实例
    InputFormat<?, ?> input =
      ReflectionUtils.newInstance(job.getInputFormatClass(), conf);
	// inputformat进行切片
    List<InputSplit> splits = input.getSplits(job);
    T[] array = (T[]) splits.toArray(new InputSplit[splits.size()]);

    // sort the splits into order based on size, so that the biggest
    // go first
    // 根据大小将分割的部分排序，以便最大的先走
    Arrays.sort(array, new SplitComparator());
    JobSplitWriter.createSplitFiles(jobSubmitDir, conf, 
        jobSubmitDir.getFileSystem(conf), array);
    return array.length;
  }
```

`getSplits()`

```java
 public List<InputSplit> getSplits(JobContext job) throws IOException {
    Stopwatch sw = new Stopwatch().start();
     // minSize=1
    long minSize = Math.max(getFormatMinSplitSize(), getMinSplitSize(job));
     // maxSize = long
    long maxSize = getMaxSplitSize(job);

    // generate splits
    List<InputSplit> splits = new ArrayList<InputSplit>();
     // 获取job文件集的列表
    List<FileStatus> files = listStatus(job);
     // 先遍历文件，
    for (FileStatus file: files) {
      Path path = file.getPath();
      long length = file.getLen();
      if (length != 0) {
        BlockLocation[] blkLocations;
        if (file instanceof LocatedFileStatus) {
          blkLocations = ((LocatedFileStatus) file).getBlockLocations();
        } else {
          FileSystem fs = path.getFileSystem(job.getConfiguration());
          blkLocations = fs.getFileBlockLocations(file, 0, length);
        }
        // 判断文件可不可以切，不可切分的压缩文件就不可以切
        if (isSplitable(job, path)) {
          // 获取文件块大小--128M
          long blockSize = file.getBlockSize();
          // 基本上每次都会取到128m
          // 假设我们不想按照128M分，想取maxsize就让max比128m小，想取minsize就让minsize比128m大
          long splitSize = computeSplitSize(blockSize, minSize, maxSize);
		  // 当前文件的剩余的大小
          long bytesRemaining = length;
            // textinputformat解决数据倾斜的问题解决办法
          // 如果当前文件剩余大小大于我切片大小的1.1倍我才会切
          while (((double) bytesRemaining)/splitSize > SPLIT_SLOP) {
            int blkIndex = getBlockIndex(blkLocations, length-bytesRemaining);
            splits.add(makeSplit(path, length-bytesRemaining, splitSize,
                        blkLocations[blkIndex].getHosts(),
                        blkLocations[blkIndex].getCachedHosts()));
            bytesRemaining -= splitSize;
          }

          if (bytesRemaining != 0) {
            int blkIndex = getBlockIndex(blkLocations, length-bytesRemaining);
            // 把切片的规则写在splits里面
            splits.add(makeSplit(path, length-bytesRemaining, bytesRemaining,
                       blkLocations[blkIndex].getHosts(),
                       blkLocations[blkIndex].getCachedHosts()));
          }
        } else { // not splitable
          splits.add(makeSplit(path, 0, length, blkLocations[0].getHosts(),
                      blkLocations[0].getCachedHosts()));
        }
      } else { 
        //Create empty hosts array for zero length files
        splits.add(makeSplit(path, 0, length, new String[0]));
      }
    }
    // Save the number of input files for metrics/loadgen
    job.getConfiguration().setLong(NUM_INPUT_FILES, files.size());
    sw.stop();
    if (LOG.isDebugEnabled()) {
      LOG.debug("Total # of splits generated by getSplits: " + splits.size()
          + ", TimeTaken: " + sw.elapsedMillis());
    }
    return splits;
  }
```

> **InputFormat**是把文件变为切片，每个切片之后再**变成（k，v）对**

- **默认的TextInputFormat** --
  - 切片方法：直接用的**FileInputFormat**的**切片方法**
  - k,v方法：自己重写

`getRecordReader()`

```java
public RecordReader<LongWritable, Text> getRecordReader(
                                          InputSplit genericSplit, JobConf job,
                                          Reporter reporter)
    throws IOException {
    
    reporter.setStatus(genericSplit.toString());
    // 分隔符
    String delimiter = job.get("textinputformat.record.delimiter");
    byte[] recordDelimiterBytes = null;
    if (null != delimiter) {
      recordDelimiterBytes = delimiter.getBytes(Charsets.UTF_8);
    }
    return new LineRecordReader(job, (FileSplit) genericSplit,
        recordDelimiterBytes);
  }
```

`LineRecordReader()`

```java
  public LineRecordReader(Configuration job, FileSplit split,
      byte[] recordDelimiter) throws IOException {
    this.maxLineLength = job.getInt(org.apache.hadoop.mapreduce.lib.input.
      LineRecordReader.MAX_LINE_LENGTH, Integer.MAX_VALUE);
    start = split.getStart();
    end = start + split.getLength();
    final Path file = split.getPath();
    compressionCodecs = new CompressionCodecFactory(job);
    codec = compressionCodecs.getCodec(file);

    // open the file and seek to the start of the split
    final FileSystem fs = file.getFileSystem(job);
    fileIn = fs.open(file);
    if (isCompressedInput()) {
      decompressor = CodecPool.getDecompressor(codec);
      if (codec instanceof SplittableCompressionCodec) {
        final SplitCompressionInputStream cIn =
          ((SplittableCompressionCodec)codec).createInputStream(
            fileIn, decompressor, start, end,
            SplittableCompressionCodec.READ_MODE.BYBLOCK);
        in = new CompressedSplitLineReader(cIn, job, recordDelimiter);
        start = cIn.getAdjustedStart();
        end = cIn.getAdjustedEnd();
        filePosition = cIn; // take pos from compressed stream
      } else {
        in = new SplitLineReader(codec.createInputStream(fileIn,
            decompressor), job, recordDelimiter);
        filePosition = fileIn;
      }
    } else {
      fileIn.seek(start);
      in = new SplitLineReader(fileIn, job, recordDelimiter);
      filePosition = fileIn;
    }
    // If this is not the first split, we always throw away first record
    // because we always (except the last split) read one extra line in
    // next() method.
    if (start != 0) {
      start += in.readLine(new Text(), 0, maxBytesToConsume(start));
    }
    this.pos = start;
  }
```

即实现一个指定的Map映射函数，用来把一组键值对映射成新的键值对，再把新的键值对发送个Reduce规约函数，用来保证所有映射的键值对中的每一个共享相同的键组

![image-20200703152714665](C:%5CUsers%5Clenovo%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20200703152714665.png)