package com.wyw.dataModel;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.util.ReflectionUtils;

import java.io.IOException;
import java.net.URI;

/**
 * @Author Leo
 * @Date 2019/5/6 9:49
 **/
public class SequenceFileOps {
    private static Configuration conf=new Configuration();

    private static String url="hdfs://niceday:9000";

    private static String[] data={"a,b,c,d,e,f,g","e,f,g,h,j,k","l,m,n,o,p,q,r,s","t,u,v,w,x,y,z"};

    public static void main(String[] args) throws IOException {
        write();
        read();
    }

    public static void write() throws IOException {
        // io.seqfile.compression.type=RECORD  记录压缩
        // io.seqfile.compression.type=BLOCK  块压缩
        conf.set("io.seqfile.compression.type","BLOCK");
        // 获取文件系统
        FileSystem fs= FileSystem.get(URI.create(url),conf);
        // 定义输出路径
        Path output=new Path("/tmp/myseqfile.seq");
        // 定义key和value
        IntWritable key=new IntWritable();
        Text value=new Text();
        // 创建写入流
        SequenceFile.Writer writer=SequenceFile.createWriter(fs,conf,output,IntWritable.class, Text.class);
        // 循环将数据写入
        for (int i=0;i<10;i++){
            key.set(i);
            // 不断将data的0-4放入writer中， 随便写点文件写入
            value.set(data[i%data.length]);
            writer.append(key,value);
        }
        // 关闭资源
        IOUtils.closeStream(writer);
    }
    private static void read() throws IOException {
        // 获取文件系统
        FileSystem fs= FileSystem.get(URI.create(url),conf);
        // 定义读取路径
        Path input=new Path("/tmp/myseqfile.seq");
        // 定义一个读入流
        SequenceFile.Reader reader=new SequenceFile.Reader(fs,input,conf);
        // 定义一个读入的key和value
        Writable key= (Writable) ReflectionUtils.newInstance(reader.getKeyClass(),conf);
        Writable value= (Writable) ReflectionUtils.newInstance(reader.getValueClass(),conf);

        while(reader.next(key,value)){
            System.out.println("key:"+key);
            System.out.println("value:"+value);
            System.out.println("position:"+reader.getPosition());// 偏移量

        }
    }
}
