package com.wyw.dataModel;

import org.apache.hadoop.fs.Path;
import org.apache.parquet.example.data.Group;
import org.apache.parquet.example.data.simple.SimpleGroup;
import org.apache.parquet.example.data.simple.SimpleGroupFactory;
import org.apache.parquet.hadoop.ParquetFileWriter;
import org.apache.parquet.hadoop.ParquetReader;
import org.apache.parquet.hadoop.ParquetWriter;
import org.apache.parquet.hadoop.example.ExampleParquetWriter;
import org.apache.parquet.hadoop.example.GroupReadSupport;
import org.apache.parquet.schema.MessageType;
import org.apache.parquet.schema.MessageTypeParser;


import java.io.IOException;

/**
 * @Author Leo
 * @Date 2019/5/7 11:49
 **/
public class ParquetOps {

    public static void main(String[] args) {
        try {
//            write();
            read();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void write() throws IOException {
        // 定义输出路径
        Path file = new Path("/tmp/user-parquet/1.parquet");
        // 定义schema信息
        String schemaStr="message User{\n" +
                "    required binary name (UTF8);\n" +
                "    required int32 age;\n" +
                "    repeated group family{\n" +
                "        repeated binary father (UTF8);\n" +
                "        repeated binary mother (UTF8);\n" +
                "        optional binary sister (UTF8);\n" +
                "    }\n" +
                "}\n";
        // 解析schema信息，将我们定义的schema信息解析成系统能看懂的schema信息
        MessageType schema=MessageTypeParser.parseMessageType(schemaStr);
        // 创建一个写入流
        ParquetWriter<Group> writer= ExampleParquetWriter.builder(file)
                .withWriteMode(ParquetFileWriter.Mode.OVERWRITE)
                .withType(schema).build();
        // 创建一个组
        SimpleGroupFactory groupFactory = new SimpleGroupFactory(schema);
        Group group1=groupFactory.newGroup();
        // 向组中添加列和值
        group1.add("name","jason");
        group1.add("age",9);
        // 嵌套组，列簇
        Group cGroup1=group1.addGroup("family");
        cGroup1.add("father","XXX");
        cGroup1.add("mother","XXX");

        Group group2=groupFactory.newGroup();
        group2.add("name","tom");
        group2.add("age",18);
        //添加子组
        group2.addGroup("family")
                .append("father","ZZZ")
                .append("mother","ZZZ");//append与add返回值不同
        writer.write(group1);
        writer.write(group2);
        writer.close();

    }
    private static void read() throws IOException {
        // 创建一个读入路径
        Path file = new Path(
                "hdfs://192.168.56.101:9000/tmp/parquet");
        // 创建一个读取流
        ParquetReader.Builder<Group> builder = ParquetReader.builder(new GroupReadSupport(), file);
        ParquetReader<Group> reader = builder.build();
        // 读入数据
        SimpleGroup group =(SimpleGroup) reader.read();
        System.out.println("schema:" + group.getType().toString());
        while(group!=null) {
            // fieldindex=0 第一列 ，index 第一列的第一个元素，确定了一个单元格
            System.out.println("username:" + group.getString(0, 0));
            System.out.println("age:" + group.getInteger(1, 0));
//            System.out.println("family.father:" + group.getGroup(2, 0).getString(0, 0));
            System.out.println(group.toString());
            group =(SimpleGroup) reader.read();
        }
    }
}
