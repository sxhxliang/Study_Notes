# GFS

## Introduction
1. Component failures are the norm rather than the exception.
  - GFS 包含上千台机器，机器都是便宜的零部件组装的
  - 机器的数量与质量导致了故障在任何时间都会发生，某些节点永远无法恢复
2. Fles are huge by traditional standards.
  - 数以TB计的网络数据
3. Most files are mutated by appending new data rather than overwriting existing data.
  - 随机写基本不存在，基本上是尾部append、线性读取
  - 如APP的数据流、大规模存档数据、运算中间结果等
4. Co-designing the applications and the ﬁle system API beneﬁts the overall system by increasing our ﬂexibility.
  - 如某些业务使用relaxed consistency model，某些业务使用支持可并发写入版本的GFS
  
***实际需求：***
1. Big & Fast
2. Global Access
3. Sharding
4. Automatic Recovering

## A Paradox Loop
Performance -> Shading -> Fault -> Tolerance -> Multi-Replication -> Consistency -> Low Performace. 

本质上是悖论，实则起点（整体性能）和终点（overhead）是两个纬度。



## Architecture

``` 
Client_1                               Chunk Server 1
Client_2        Master(secondary)      Chunk Server 2
...                 ...                Chunk Server 3
Client_n-1      Master(primary)             ...
Client_n                               Chunk Server K
```

## 数据流与控制流
GFS的数据流与控制流解耦
- 控制流由Client直接发送到各个server
- 数据流通过链式结构线性传播
    - 先通过IP地址找到离client最近的server并传输数据，再依次传递给最近下一个server
    - 避免了单一节点网络带宽成为瓶颈
    - 双工网络链接保证接受数据同时**立刻**传输数据给下一个，总延时为 B/T + RL（B数据量，T吞吐量，R备份数目，L网络延迟）

## Master
### Master's Metadata
```
v：volatile 存储在内存中，断电消失
nv：non-volatile 存储在磁盘中，断电不消失

1. The file and chunk namespace
2. Map[filename]-> chunk handels (nv)
3. Locations of all chunkservers
4. Map[chunk handel] -> {list of chunkservers, (v) # master 重启后询问所有chunk server 确认状态)
                         chunk version number, (nv)
                         primary server, (v)       # 重启后可以等待60s lease time 后重新分配primary
                         lease expiration          # 一台server可以在租约限定时间内作为primary
                        }
```

master 中的所有数据都是存在 memory 里，所以操作速度很快，然而缺点是整个系统的 capacity 就被 master 的内存容量限制了。

GFS对此的解决方案：一个64MB的chunk 的 metadata < 64byte；文件命名空间进行前缀压缩，File metadata < 64byte，所以metadata所需空间并不大，单纯地增加内存容量即可。

一个简单计算：1TB 的 memory 能装 2^24 个 metadata，目前由于单机最多可以插192张内存条，最大内存是24TB，也就是索引3亿多个文件。

### Chunk Location
Master 不去同步维护每个 chunk 的位置，而是：
1. 在 Boot 之后自动拉取所有在线的 chunkserver 及其 chunks 的状态
2. 运行时间歇式地通过 HeartBeat 监控 chunkservers

### Log & Checkpoints
Master 的故障恢复主要靠两个文件：
1. Operation Log
- 在本地存储, 并在Secondary Master备份
- 每次会flush out 一批 log records，只有当本地和远端都flush到磁盘之后，master才会相应client的请求。

2. checkpoint
- 存储整个file system state。
- 以B-Tree方式存储，可直接映射到内存中，恢复速度快可用性强。
- 重启后以最新的checkpoint作为初始化，replay recent operation logs。

## 租约机制
Master 通过给 chunkserver 赋予租约以减小其自身的管理开支。数据在不同replica之间的的写入顺序以及一致性由拥有租约的server代理。

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

## Snapshot
当数据需要备份以应对未来的回滚（roll back）时，chunkserver将会进行snapshot operation，这里采用了**copy-on-write**机制。

1. master直接copy一份当前文件的metadata，指向当前chunks
2. 当某clinet发出修改chunks C 的请求时，master确认该chunk是否涉及snapshot的引用，若有引用则开辟一块新的chunk C'，复制C->C'；随后返回 C' 的 primary server 给 client。
3. 大幅增加了快照速度（几乎立刻完成），只对修改过的文件进行拷贝（充分信任文件系统的备份机制）。

# References
1. [HDFS 和 GFS 的设计差异](https://blog.csdn.net/xiaofei0859/article/details/53466008)

# Terms
- **volatile**: volatile is used to describe memory content that is lost when the power is interrupted or switched off. 
- **Stale Version**: An old version of data. like a month ago or so.
