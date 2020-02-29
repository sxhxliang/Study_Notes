# Hadoop

[An Introduction to Apache Hadoop](https://opensource.com/life/14/8/intro-apache-hadoop-big-data)

## Terminology
### NameNode
The NameNode is the centerpiece of an HDFS file system. It keeps the **directory tree** of all files in the file system, and tracks where across the cluster the file data is kept. It does not store the data of these files itself.

### Commodity Hardware
The Hadoop Distributed File System (HDFS) is a distributed file system designed to run on hardware based on **open standards** or what is called **commodity hardware**. This means the system is capable of running different operating systems (OSes) such as Windows or Linux without requiring special drivers.

### Rack
A Rack is **a collection nodes** usually in 10 of nodes which are closely stored together and all nodes are connected to **a same Switch**. When an user requests for a read/write in a large cluster of Hadoop in order to improve traffic the namenode chooses a datanode that is closer this is called **Rack Awareness**.


### 什么是Yarn
Yarn是一个资源调度平台。我们将一批机器组成一个资源池供大家共同使用，这样一来闲置的资源就可以共享给其他人使用，增加资源的使用效率。同时，我们也存在一些隔离机制，使得已经申请使用的资源保证能够分配给用户使用。

关于Yarn的更多信息，可以参考开源项目网站：http://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/YARN.html

### Yarn和HDFS的关系
Yarn和HDFS共同属于Hadoop开源项目，两者相互协作完成任务调度和执行的功能。HDFS是一个分布式文件存储系统，用户要提交的任务首先打包上传到HDFS系统中，然后再由Yarn进行调度。Yarn将任务调度到某台具体的机器上，在该机器上从HDFS下载打包的用户任务，然后再执行任务。

### Yarn和MapReduce/Spark/Flink的关系
MapReduce/Spark/Flink均为分布式计算框架，是一个抽象层用于帮助用户编写分布式计算程序。编写好的分布式计算程序需要运行在某个能够提供计算资源的平台上，Yarn就是这样的一个平台。同类的平台还有Mesos和Kubernetes。

### 资源组
Resource Group（资源组），是一个虚拟的组，也是HDFS Quota审计和成本审计的单位，目的是将组织架构上的Team和HDFS quota进行解耦，更加方便的用户的拆分，成本系统的对接，INodeQuota的上线，以及更加标准化，规范化的使用HDFS服务。

主要区别：
1. 将Team与HDFS quota解耦，用户不再直接对Team申请quota。
3. 一个Team可以有一个或多个资源组，一个用户可以处在多个资源组中。

### 队列
对于很豪的公司来说，每个用户(团队)自己有一个hadoop集群，这样可以提高自身的稳定性和资源供应，但是确降低了资源利用率，因为很多集群大多数时间都是空闲的。CapacityScheduler能实现这样的功能：每个组固定享有集群里的一部分资源，保证低保，同时如果这个固定的资源空闲，那么可以提供给其他组来抢占，但是一旦这些资源的固定使用者要用，那么立即释放给它使用。这种机制在实现上是通过queue（队列）来实现的。当然CapacityScheduler还支持子队列（sub-queue），

参数包括 CPU配额（低保线）、CPU上限、内存配额与上限、最大允许作业数，是否允许抢占等

## 配置环境
1. 先安装Java，再安装yarn_deploy部署库，安装hadoop
2. 申请加入资源组（HDFS）
3. 申请加入一个队列（YARN）
4. 提交任务

## MapReduce
MapReduce is a software framework for processing large datasets in a distributed fasion over a several machines. The core idea behind MapReduce is mapping your dataset into a collection of <key, value> pairs, and then reducing over all pairs with the same key.

Take **wordcount** as an example:

- The purpose of the map script is to model the data into <key, value> pairs for the reducer to aggregate. (text to <word, 1>)
- Emitted kv pairs are "shuffled" or grouped based on the keys. (groupby word)
- The reduce script takes a collection of kv pairs and reduce them. (sum over counts)

![](figures/mapreduce.png)
