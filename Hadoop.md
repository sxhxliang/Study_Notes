# Hadoop

[An Introduction to Apache Hadoop](https://opensource.com/life/14/8/intro-apache-hadoop-big-data)

## Terminology
### NameNode
The NameNode is the centerpiece of an HDFS file system. It keeps the **directory tree** of all files in the file system, and tracks where across the cluster the file data is kept. It does not store the data of these files itself.

### Commodity Hardware
The Hadoop Distributed File System (HDFS) is a distributed file system designed to run on hardware based on **open standards** or what is called **commodity hardware**. This means the system is capable of running different operating systems (OSes) such as Windows or Linux without requiring special drivers.

### Rack
A Rack is **a collection nodes** usually in 10 of nodes which are closely stored together and all nodes are connected to **a same Switch**. When an user requests for a read/write in a large cluster of Hadoop in order to improve traffic the namenode chooses a datanode that is closer this is called **Rack Awareness**.
