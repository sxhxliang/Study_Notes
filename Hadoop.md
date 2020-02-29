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
