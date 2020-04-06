# Raft

[Illustration](http://thesecretlivesofdata.com/raft/)

## Leader Election

1. Election Timeout
- Election Timeout 是一个follower 在成为 candidate 之前的等待时间，通常为 150ms - 300ms。
- 这段时间是随机的，如果这段时间内都未收到 heartbeat，则开启新的 Election Term，向其他节点发送 RequestVote。
- 若某节点在当前 Term 未投票，则投给该 candidate，并重置其 election timeout。

2. HeartBeat Timeout
- 一个 leader 节点每隔一段固定时间会向所有 followers 发送 AppendEntry，这段时间长短就是 HeartBeat Timeout。

## Commit
leader 接收 client request，发送给每个follower；当收到大部分 follower 接收到entry的回应后，leader 执行并将结果返回 client，同时告知所有 followers 该条 entry 已被commit。

## Split Vote
当恰巧多个 follower 同时发起了 Election Vote，各自都得不到 majority 的票数时，就发生了 split vote。
如何结束 split vote？
