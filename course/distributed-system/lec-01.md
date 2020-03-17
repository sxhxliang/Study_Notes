# Distributed System

## Major Topics
- Fault Tolerance
  - Availability：即便某些节点fails，仍然可以继续provide services
  - Recoverability：如果许多节点fails导致整个系统停止服务，仍然可以修复并保持正确性
- Consistency
  - Put/Get Operation
  - Strong Consistency：保证get到最新数据，节点间需要很多"chitchat"，需要 very heavy spec operation
  - Weak Consistency：不保证get到的是最新的数据
  - Different Copies：保持多个备份，地理上相互隔离防止同时crash


## MapReduce
### 目的
Google 在刚成立之初需要处理巨量数据，如给整个Web的网页进行indexing，那时互联网的整体数据量也有tens of Tyrabytes。当时的处理方式是雇佣大量有经验的SDE，人工设计在集群上的计算任务设计、分配、收集等等。然而这需要大量人力成本，如何能够使得不懂分布式原理的ordinary people也能使用集群进行计算呢？这就是MapReduce这一分布式计算框架诞生的需求。
