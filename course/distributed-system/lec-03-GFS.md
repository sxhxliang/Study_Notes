# GFS

## Introduction
1. Component failures are the norm rather than the exception.
  - GFS 包含上千台机器，机器都是便宜的零部件组装的
  - 机器的数量与质量导致了故障在任何时间都会发生，某些节点永远无法恢复
2. Fles are huge by traditional standards.
  - 数以TB计的网络数据
3. Most ﬁles are mutated by appending new data rather than overwriting existing data.
  - 随机写基本不存在，基本上是尾部append、线性读取
  - 如APP的数据流、大规模存档数据、运算中间结果等
4. Co-designing the applications and the ﬁle system API beneﬁts the overall system by increasing our ﬂexibility.
  - 如某些业务使用relaxed consistency model，某些业务使用支持可并发写入版本的GFS

## A Paradox Loop
Performance -> Shading -> Fault -> Tolerance -> Replication -> Consistency -> Low Performace. 

## Requirements
1. Big & Fast
2. Global Access
3. Sharding
4. Automatic Recovering

## Architecture

``` 
C1                  Chunk Server 1
C2                  Chunk Server 2
...       Master    Chunk Server 3
Cn-1                ...
Cn                  Chunk Server K
```

### 2.6 Master MetaData:
```
1. The file and chunk namespace
2. Map[File name]-> chunk handels (nv)
3. Locations of all chunkservers
3. Map[chunk handel] -> {list of chunkservers contains replicants, (v: master 重启后询问所有chunk server 确认状态)
                          chunk version number, (nv)
                          primary server, # one among the list (v：重启后可以等待60s lease time 后重新分配primary)
                          lease expiration  # one server can be primary for a certain time (v)
                        }
```

### 2.6.1 In-Memory data structure
master 节点中的所有数据都是存在内存里，所以操作速度很快，然而缺点是整个系统的capacity就被master节点的内存容量限制了。

GFS对此的解释是：对一个64MB的chunk，其metadata只需要64byte；GFS也对文件名进行了前缀压缩，使得文件命名空间metadata也只需要64byte，所以metadata所需空间并不大，单纯地增加内存容量即可。

### 2.6.2 Chunk Location
Master节点不去同步维护每个chunk的位置，而是：
1. Master Boot之后自动拉取所有在线的chunkserver的状态
2. 运行时间歇式地通过HeartBeat监控chunkserver

### 2.6.3 Log & Checkpoints
Master 的故障恢复主要靠两个文件：
1. Operation Log
- 在本地存储并在远端备份
- 每次会flush a batch of log records，只有当本地和远端flush到磁盘之后，master才会相应client的请求。

2. checkpoint
- 存储整个file system state。
- 以B-Tree方式存储，可直接映射到内存中，恢复速度快可用性强。
- 重启后以最新的checkpoint作为初始化，replay recent operation logs。

### 读取数据
1. Client 发送文件名与 offset 给 master
2. Master 调取对应的 chunk server list 告知Client
3. Client 向对应的 chunk server 获取数据

### 写入数据
![](https://thetechangle.github.io/images/GFS_flow.png)

若该文件replicas无primary
1. 询问master拥有最新数据的chunk servers
2. 将其指定为primary，赋予其租约（lease）

若该文件replicas已有primary

3. 增加version number，告知primary 和 secondaries 最新的 version number
4. client向primary传输数据并在offset处写入数据
5. Primary replicas通知所有Secondary写入数据
6. Secondaries 写入数据，返回'成功'或'失败'
7. 如果所有replicas均成功，则primary向client报告'成功'，否则返回'失败'

问题：如果某些replicas写入了数据而有些没写，会造成数据不同步的问题，如何解决？

答：可能因为各种原因导致某些replicas写入失败，那么这些将会被master弃用，并起用全新的secondary server with up-to-date data。

### 并发追加写入
传统的随机并发写入是不可序列化的，会导致文件中包含来自各个client的碎片化数据。而追加写入是可以序列化的，GFS使用了 **multi-producer/one-comsumer** 的模型去处理并发的追加写入。

**过程：**
1. Client 将数据推送至所有 chunkservers，向 Primary 发出写入请求
2. Primary 确认写
    - 若当前chunk剩余空间不足，则用padding补全，通知secondary进行相同操作，通知Client重试。
    - 若当前chunk剩余空间充足，直接追加写入，secondary相同操作
3. 若某chunkserver写入失败，则通知client重写

**要点：**
1. 追加写入操作是原子的（atomically）
2. GFS只保证每个chunkserver都有至少一次原子写入，所以某些server上会有重复的records
3. 如果不需要重复，则可以通过每个records的附加信息过滤掉duplicates

```
ori:    A   A   A
append: AB  AX  AB
retry:  ABB AXB ABB
```

# Terms
- **volatile**: volatile is used to describe memory content that is lost when the power is interrupted or switched off. 
- **Stale Version**: An old version of data. like a month ago or so.
