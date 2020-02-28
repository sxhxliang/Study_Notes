# Hadoop

[An Introduction to Apache Hadoop](https://opensource.com/life/14/8/intro-apache-hadoop-big-data)

## Terminology
### NameNode
The NameNode is the centerpiece of an HDFS file system. It keeps the directory tree of all files in the file system, and tracks where across the cluster the file data is kept. It does not store the data of these files itself.

### Commodity Hardware
The Hadoop Distributed File System (HDFS) is a distributed file system designed to run on hardware based on **open standards** or what is called **commodity hardware**. This means the system is capable of running different operating systems (OSes) such as Windows or Linux without requiring special drivers.

### Rack
A Node is simply a computer. This is typically non-enterprise, commodity hardware for nodes that contain data. Storage of Nodes is called as rack. A rack is a collection of 30 or 40 nodes that are physically stored close together and are all connected to the same network switch. Network bandwidth between any two nodes in rack is greater than bandwidth between two nodes on different racks. A Hadoop Cluster is a collection of racks.

The main purpose of Rack awareness is:

- Increasing the availability of data block
- Better cluster performance
- Data protection against rack failure
