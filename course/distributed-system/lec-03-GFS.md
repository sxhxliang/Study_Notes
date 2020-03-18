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

Master Data:
```
Map[File name]-> chunk handels (nv)
Map[chunk handel] -> {list of chunkservers contains replicants, (v: master 重启后询问所有chunk server 确认状态)
                      chunk version number, (nv)
                      primary server, # one among the list (v：重启后可以等待60s lease time 后重新分配primary)
                      lease expiration  # one server can be primary for a certain time (v)
                      }
```
Master 在disk上维护了两个文件：
1. 一个Log文件，每次在尾部append曾进行的操作，如更改了primary，某个新的chunk存储在哪个server等。
2. 一个checkpoint，存储整个磁盘的状态，重启后在以最新的checkpoint作为初始化，进行log里此时间点后的操作进行恢复。

### 读取数据
1. Client 发送文件名与 offset 给 master
2. Master 调取对应的 chunk server list 告知Client
3. Client 向对应的 chunk server 获取数据

### 写入数据
![](https://thetechangle.github.io/images/GFS_flow.png)

若该文件replicas无primary
1. 询问master拥有最近的version的chunk server
2. 将其指定为primary，赋予其 lease
3. 增加version number，告知primary 和 secondaries 最新的 version number

若该文件replicas有primary
4. client向primary传输数据并在offset处写入数据
5. Primary replicas通知所有Secondary写入数据
6. Secondaries 写入数据，返回yes或no
7. 如果所有replicas返回‘yes’，primary向client返回‘success’，否则返回‘fail’



# Terms
- **volatile**: volatile is used to describe memory content that is lost when the power is interrupted or switched off. 
- **Stale Version**: An old version of data. like a month ago or so.
