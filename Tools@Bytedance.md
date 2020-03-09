# 一些实习需要学习的工具

## 1. Euler - 基于Thrift的微服务框架
微服务框架风格是一种通过一组小的服务开发新的应用的方式，这些微服务在其自己的进程中运行并通过轻量级方式如HTTP进行通讯。

In short, the microservice architectural style is an approach to developing a single application as a suite of small services, each running in its own process and communicating with lightweight mechanisms, often an HTTP resource API. These services are built around business capabilities and independently deployable by fully automated deployment machinery. There is a bare minimum of centralized management of these services, which may be written in different programming languages and use different data storage technologies.
### Consul 服务发现
Consul是由HashiCorp基于Go语言开发的支持多数据中心分布式高可用的服务发布和注册服务软件，采用Raft算法保证服务的一致性，且支持健康检查。

Consul采用主从模式的设计，使得集群的数量可以大规模扩展，集群间通过RPC的方式调用(HTTP和DNS)。在本地（尤其是使用 mac 机器）调用远程服务时发生，原因是调用远程服务时需要使用 consul 进行服务发现，但是本地机器没有 consul 服务。解决：在环境变量中添加 CONSUL_HTTP_HOST=YOUR_DEVBOX_IP

[Consul 服务发现详解](https://www.jianshu.com/p/f8746b81d65d)

### Thrift

Thrift是一套包含序列化功能和支持服务通信的RPC框架，主要包含三大部分：代码生成、序列化框架、RPC框架，大致相当于protoc + protobuffer + grpc，并且支持大量语言，保证常用功能在跨语言间功能一致，是一套全栈式的RPC解决方案。整体架构图：
![](figures/thrift.png)
### IDL和代码生成
Interface Definition Languages 接口描述语言

The Apache Thrift framework is entirely focused on enabling programmers to design and construct **cross-language, distributed computing interfaces**. Interfaces consist of two principle parts:

- User-defined types (UDTs)—The things exchanged between systems
- Services—Sets of methods exposing cohesive functionality

![](figures/idl.jpg)

Interface Definition Languages are designed to allow programmers to define interface contracts in an abstract fashion, **independent of** any programming language or system platform. IDL contracts ensure that all parties communicating over an interface know exactly what will be exchanged and how to exchange it. This allows tools to do the busy work of generating code to interoperate over the interface. **IDLs allow developers to focus on the problem domain, not the mechanics of remote procedure calls or cross-language serialization.**

## 2. MapReduce

```
/opt/tiger/yarn_deploy/hadoop/bin/hadoop jar /opt/tiger/yarn_deploy/hadoop/./share/hadoop/tools/lib/hadoop-streaming-2.6.0-cdh5.4.4.jar     \
-D mapred.job.name=${JOB_NAME} \            # 任务名
-D mapred.reduce.memory.limit=3000 \
-D mapred.map.memory.limit=3000 \
-D stream.memory.limit=3000 \               # 任务内存限制
-D mapred.map.capacity.per.tasktracker=1 \
-D mapred.reduce.capacity.per.tasktracker=1 \
-D mapred.map.tasks=${MAP_TASKS} \              # map个数，数目大于等于输入文件数
-D mapred.job.map.capacity=${MAP_CAPACITY} \    # map容量，一般与map个数一致
-D mapred.reduce.tasks=${RED_TASKS} \           # reduce个数
-D mapred.job.reduce.capacity=${RED_CAPACITY} \ # reduce容量，一般与reduce容量一致
-D mapred.job.priority=${MAPRED_PRIORITY} \     # 任务优先级
-D mapred.userlog.retain.hours=${LOG_RETAIN_HOURS} \
-D stream.num.map.output.key.fields=3 \         # map的结果按前三列排序
-D num.key.fields.for.partition=1 \             # 第一列相同的数据分配到同一个reducer
-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
-input /log/1079/cpro_pblog_noah/20110814/*/pb.log* \ # 输入
-input /log/1079/cpro_pblog_noah/20110815/*/pb.log* \ # 输入
-input /log/3148/shifen_bdclk_noah/20110814/*/dcharge.bd.*.log* \ # 输入
-input /log/3148/shifen_bdclk_noah/20110815/*/dcharge.bd.*.log* \ # 输入
-output ${REDUCE_OUT} \ # 输出
-mapper "java6/bin/java -classpath ad_trade com.baidu.cm.ufs.Mapper testno.txt" \   # mapper程序
-reducer "java6/bin/java -classpath ad_trade com.baidu.cm.ufs.Reducer" \            # reducer程序
-file ad_trade \ # 要上传分发的文件
-file testno.txt \
-cacheArchive /app/ecom/cm/nova.ufs/u-wangyou/java6.tar.gz#java6 # hdfs上要分发的压缩包，解压后的文件夹名为java6
```

[深入了解SQL Join机制](https://www.jianshu.com/p/9e1d3793cba6)

## 3. HDFS
```
# 命令行操作
hdfs dfs -ls /user/xiaoyunxuan
hdfs dfs -text /user/xiaoyunxuan/part* | head -10
hdfs dfs -rm -r /user/xiaoyunxuan/trash

# 上传文件
hdfs dfs -put local_file hdfs_dir 
hdfs dfs -get remote_file localdir
```


## 4. HIVE SQL
```SQL
INSERT OVERWRITE DIRECTORY 'hdfs://haruna/user/xiaoyunxuan/data/compass/compass_celebrity_info-20200229'
SELECT
    name,
    compass_id
FROM
    dm_content.compass_celebrity_info
WHERE
    date = "20200229"
```
