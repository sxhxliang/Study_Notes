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

