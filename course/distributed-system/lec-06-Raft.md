# Raft 一致性算法

## What is a consistency algorithm ?
一致性是分布式容错系统的基本功能，例如在分布式共享文件系统中，通常有多台服务器向客户提供文件服务，当客户通过其中一台服务器A向文件系统存储了一个文件，如何保证能从服务器B获取刚刚保存的文件？其核心问题在于多台机器就某个值达成一致，一旦某个值达成了一致，客户向整个集群的任何一台机器请求该值时都会得到同一个值。

一致性算法通常产生于多副本状态机情景中，多副本状态机即集群中每个服务器维护一个状态机，它们维护同一数据状态的相同副本。例如在使用GFS, HBase的大型系统中，集群的Leader节点管理全系统配置信息，这些信息在Master 当掉时必须能够恢复, 这些系统通常使用多副本状态机来管理Leader选举和配置信息存储。Chubby和ZooKeeper都是多副本状态机。GFS使用Chubby, 而HBase使用ZooKeeper。


## Terms
**Network Partition** （网络分裂）: A network partition refers to a network split between nodes due to the failure of network devices. Example: When switch between two subnets fails, there is a partition between nodes.

![](https://blog.yugabyte.com/wp-content/uploads/2019/05/How-Does-YugaByte-DB-Handle-Network-Partitions-and-Failover-blogpreview.png)