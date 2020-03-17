# RPC & Go

## 1. Threads
Go routines = Threads
- 一个进程里的多个线程共用一套地址空间
- 多个线程拥有各自的Stack、Stack Counter等等
- 事实上线程间可以访问各自的栈，但是一般不这么做

### Reasons for Using Threads
- I/O Concurrency：多个任务读取or写入数据可以同时进行
- Parallelism
- Convenience
  - periodic operations（check whether a work is alive）

### Coordination
如何在内部组织进程间何时交互、如何交互

Go 内部的一些工具
- Channel：Go 线程间传递数据
- waitGroup：?
- sync.cond:?

## 2. Web Crawler
1. 递归抓取网页可能会造成死循环，因为网页间的Graph可能是cyclic的，线程需要知道哪些网页已经访问了。
2. 知道何时爬虫需要停止

  
## Question
OS如何协调多个Thread在CPU的运行时间？

## Terms
**Overhead**（额外开销）：In computer science, overhead is any combination of excess or indirect computation time, memory, bandwidth, or other resources that are required to perform a specific task.

**fire off/up**：fire up 8 threads
