# Operating System 操作系统

## 目录

1. [系统调用](#anchor1)
    - API与系统调用
    - 用户态与内核态
    - 常见的系统调用
2. [死锁相关](#anchor1)
3. [进程间通讯](#anchor3)
    - Socket
    - 管道
    - 共享内存
    - 消息队列
4. [进程与线程](#anchor4)
    - 多线程
    - 多进程
5. [线程调度](#anchor5)


## <span id = "anchor1">系统调用</span> 
[系统调用详解](https://blog.csdn.net/gatieme/article/details/50779184)

linux内核中设置了一组用于实现系统功能的子程序，称为系统调用。系统调用和普通库函数调用非常相似，只是系统调用由操作系统核心提供，运行于内核态，而普通的函数调用由函数库或用户自己提供，运行于用户态。

一般地，系统调用都是通过软件中断实现的，x86系统上的软件中断由`int $0x80`指令产生，而128号异常处理程序就是系统调用处理程序`system_call()`。

### 2.1 API 与 系统调用
- 程序员调用的是API（API函数），然后通过与系统调用共同完成函数的功能，因此，**API是一个提供给应用程序的接口**，一组函数，是与程序员进行直接交互的。
- 系统调用则不与程序员进行交互的，它根据API函数，通过一个软中断机制向内核提交请求，以获取内核服务的接口。
- 并不是所有的API函数都一一对应一个系统调用，有时，一个API函数会需要几个系统调用来共同完成函数的功能，甚至还有一些API函数不需要调用相应的系统调用（因此它所完成的不是内核提供的服务）

### 2.2.1 内核态 与 用户态
![](https://upload-images.jianshu.io/upload_images/2744546-2b78e131a118b774.png?imageMogr2/auto-orient/strip|imageView2/2/w/366/format/webp)

**内核态与用户态是进程在操作系统中的两种运行级别。**

intel cpu提供Ring0-Ring3三种级别的运行模式。Ring0级别最高，Ring3最低。当一个任务(进程)执行系统调用而陷入内核代码中执行时，我们就称进程处于内核运行态(或简称为内核态)。此时处理器处于特权级最高的(0级) 内核代码中执行。当进程处于内核态时，执行的内核代码会使用当前进程的内核栈。每个进程都有自己的内核栈。当进程在执行用户自己的代码时，则称其处于用户运行态(用户态)。即此时处理器在特权级最低的(3级)用户代码中运行。

- 内核态：cpu可以访问内存的所有数据，包括外围设备，例如硬盘，网卡；且所占用的CPU是不允许被抢占的。
- 用户态：只能受限的访问内存，且不允许访问外围设备；且所占用的CPU是可以被抢占的。
- 系统调用：为了使上层应用能够访问到这些资源，内核为上层应用提供访问的接口。

![](https://upload-images.jianshu.io/upload_images/2744546-cc53e9112a785a83.png?imageMogr2/auto-orient/strip|imageView2/2/w/742/format/webp)


### 2.2.2 用户态与内核态的切换
用户态切换为内核态的三种情况：
- 系统调用 (软中断)
- 异常事件： 当CPU正在执行运行在用户态的程序时，突然发生某些预先不可知的异常事件，这个时候就会触发从当前用户态执行的进程转向内核态执行相关的异常事件，典型的如缺页异常。
- 外围设备的中断(硬中断)：当外围设备完成用户的请求操作后，会像CPU发出中断信号，此时，CPU就会暂停执行下一条即将要执行的指令，转而去执行中断信号对应的处理程序，如果先前执行的指令是在用户态下，则自然就发生从用户态到内核态的转换。

系统调用的本质其实也是中断，相对于外围设备的硬中断，这种中断称为**软中断**。从触发方式和效果上来看，这三种切换方式是完全一样的，都相当于是执行了一个中断响应的过程。但是从触发的对象来看，系统调用是进程主动请求切换的，而异常和硬中断则是被动的。


### 2.3 常见的系统调用
常见的unix系统调用主要分为三类：文件操作系统的系统调用，控制类的系统调用，信号和时间类的调用。

1. 文件操作的系统调用
- create ，open，read，write，close，link，unlink，lseek，chmod，rename (打开，关闭，读写，链接，取消链接，建立文件)
- lseek 设定文件的读写位置
- chmod 改变对文件的访问权限
- rename 更改文件名

2. 控制类系统调用
- fork 创建一个子进程
- wait 父进程等待子进程终止
- exit 终止子进程的执行
- exec 启动执行一个指定文件

3. 信号与时间的系统调用
UNIX把出现的异常情况或异步事件以传送信号的方式进行，与信号有关的系统调用主要有：
- kill 把信号传送给一个或几个相关进程
- sigaction 声明准备接收的信号类型
- sigreturn 从信号返回，继续执行被信号中断的操作

4. UNIX用于时间管理的系统调用主要有：
- stime 设置日历时间
- time 获得日历时间
- times 获得执行所花费的时间

## <span id = "anchor2">死锁</span>
死锁: 多个进程因循环等待资源而造成无法执行的现象。

死锁会造成进程无法执行，同时会造成系统资源的极大浪费(资源无法释放)。

死锁产生的4个必要条件：

1. 互斥使用(Mutual exclusion)

指进程对所分配到的资源进行排它性使用，即在一段时间内某资源只由一个进程占用。如果此时还有其它进程请求资源，则请求者只能等待，直至占有资源的进程用毕释放。

2. 不可抢占(No preemption)

指进程已获得的资源，在未使用完之前，不能被剥夺，只能在使用完时由自己释放。

3. 请求和保持(Hold and wait)

指进程已经保持至少一个资源，但又提出了新的资源请求，而该资源已被其它进程占有，此时请求进程阻塞，但又对自己已获得的其它资源保持不放。

4. 循环等待(Circular wait) 

指在发生死锁时，必然存在一个进程——资源的环形链，即进程集合{P0，P1，P2，···，Pn}中的P0正在等待一个P1占用的资源；P1正在等待P2占用的资源，……，Pn正在等待已被P0占用的资源。

### 死锁避免：银行家算法

思想: 判断此次请求是否造成死锁若会造成死锁，则拒绝该请求

## <span id = "anchor3">进程间通讯 IPC</span>
常见的进程间通讯(Inter-Process Communication)主要有以下几种方式：
- Socket
- 管道
- 消息队列
- 信号量
- 共享内存

### 3.1 Socket

[Golang socket 编程实战](https://tonybai.com/2015/11/17/tcp-programming-in-golang/)

下面举一个简单的例子构建基于 unix-socket 的 server-client 模型。

```golang
// ------- server.go ------- 
package main

import (
	"bufio"
	"log"
	"net"
	"os"
)

func handelConn(conn net.Conn) {
	defer conn.Close()
	for {
		var buf = make([]byte, 10)
		n, err := conn.Read(buf)
		if err != nil {
			log.Println("Read Error: ", err)
			break
		}
		log.Printf("read %d bytes, content is %s\n", n, string(buf[:n]))
	}
}

func closeServer(listener net.Listener) {
	inputReader := bufio.NewReader(os.Stdin)
	for {
		input, err := inputReader.ReadString('\n')
		if err != nil {
			log.Println("User input err: ", err)
		}
		if input == "close" {
			listener.Close()
			return
		}
	}
}

func main() {
	log.Println("start listening")
	listener, err := net.Listen("unix", ":8889")

	if err != nil {
		log.Println("listen err:", err)
		return
	}
	go closeServer(listener)

	cnt := 0
	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Println("accept err: ", err)
			break
		}
		log.Println("accept connection ", cnt)

		go handelConn(conn)
		cnt += 1
	}
}
```

```golang
\\ --------- client.go ----------
package main

import (
	"log"
	"net"
	"strconv"
	"time"
)

func main (){
	log.Println("begin dail")
	conn, err := net.Dial("unix", ":8889")
	if err != nil {
		log.Println("connection err: ", err)
		return
	}
	defer conn.Close()

	for i := 0; i < 10; i++ {
		message := "message " + strconv.Itoa(i)
		
		n, err := conn.Write([]byte(message))
		if err != nil {
			log.Println("Write socket err: ", err)
			continue
		}
		
		log.Printf("Write %d bytes, content is %s\n", n, message)
		time.Sleep(2 * time.Second)
	}
}
```

这时候我们分别启动 server 和 多个 clients, 链接就构建起来啦！

```bash
>>> go run server.go
2020/04/23 13:24:10 start listening
2020/04/23 13:24:10 accept connection 0
2020/04/23 13:24:12 read 9 bytes, content is message 0
2020/04/23 13:24:13 accept connection 1
2020/04/23 13:24:13 read 9 bytes, content is message 0
2020/04/23 13:24:14 read 9 bytes, content is message 1
2020/04/23 13:24:15 read 9 bytes, content is message 1
2020/04/23 13:24:16 read 9 bytes, content is message 2
2020/04/23 13:24:17 read 9 bytes, content is message 2
...

-----------------------------
>>> go run client.go & go run client.go & go run client.go

2020/04/23 13:24:12 begin dail
2020/04/23 13:24:12 write 9 bytes, content is message 0
2020/04/23 13:24:13 begin dail
2020/04/23 13:24:13 write 9 bytes, content is message 0
2020/04/23 13:24:14 write 9 bytes, content is message 1
2020/04/23 13:24:15 write 9 bytes, content is message 1
2020/04/23 13:24:16 write 9 bytes, content is message 2
2020/04/23 13:24:17 write 9 bytes, content is message 2
2020/04/23 13:24:18 write 9 bytes, content is message 3
...
```

go socket编程还涉及到以下问题，详细参阅上文链接。
- listen backlog 满了怎么办？ 
    - client dail 阻塞，backlog size 最大默认 128
- 网络延迟较大，Dial 阻塞并超时怎么办？ 
    - `conn, err := net.DialTimeout("tcp", "104.236.176.96:80", 2*time.Second)`
- Socket 中无数据，或者比期望读取数据size小怎么办？
    - 阻塞/读部分数据
- 读取操作超时？ 
    - `conn.SetReadDeadline()`


### 3.2 管道 [link](https://blog.csdn.net/qq_35116371/article/details/71843606)

![](https://img-blog.csdn.net/20170513173717717?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvcXFfMzUxMTYzNzE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

调用pipe函数时在内核中开辟一块缓冲区(称为管道)用于通信,它有一个读端一个写端,然后通过fds参数传出给用户程序两个文件描述符,filedes[0]指向管道的读端,filedes[1]指向管道的写端(很好记,就像0是标准输入1是标准输出一样)。所以管道在用户程序看起来就像一个打开的文件,通过read(fds[0]);或者write(fds[1]);向这个文件读写数据其实是在读写内核缓冲区。pipe函数调用成功返回0,调用失败返回-1。

```bash
>>> go env | grep GOROOT
```

举个例子，这里 go env会启动一个进程， 而grep命令也会产生一个进程，grep的进程会在go env的标准输出中进行检索GOROOT的行的信息然后显示出来，而负责这两个进程间的通信的正是管道。两个进程通过一个管道只能实现单向通信。

很多的人都知道`|`这个符号是一种管道 ，我们就会发现`|`这是一种匿名的管道: 首先它没有创建新的管道文件；再者它通信的进程虽然不是父子进程，但是可以看成是兄弟进程（同是shell创建的子进程）。

#### 3.2.1 匿名管道

**匿名管道**的一些特点是：
1. 只能进行单向通信；
2. 管道依赖于文件系统，进程退出，管道随之退出，即生命周期是随进程的；
3. 常用于父子进程间的通信，这种管道只能用于具有亲缘关系的进程；
4. 管道是基于流的，是按照数据流的方式读写的；
5. 同步访问，即管道访问是自带同步机制的。

```golang
package main

import "fmt"
import "os/exec"
import "bufio"
import "bytes"

func main() {
        //create cmd
        cmd_go_env := exec.Command("go", "env")
        cmd_grep := exec.Command("grep", "GOROOT")

        stdout_env, env_error := cmd_go_env.StdoutPipe()
        if env_error != nil {
                fmt.Println("Error happened about standard output pipe ", env_error)
                return
        }

        if env_error := cmd_go_env.Start(); env_error != nil {
                fmt.Println("Error happened in execution ", env_error)
                return
        }
        
        //get the output of go env
        stdout_buf_grep := bufio.NewReader(stdout_env)

        //create input pipe for grep command
        stdin_grep, grep_error := cmd_grep.StdinPipe()
        if grep_error != nil {
                fmt.Println("Error happened about standard input pipe ", grep_error)
                return
        }

        //connect the two pipes together
        stdout_buf_grep.WriteTo(stdin_grep)

        //set buffer for reading
        var buf_result bytes.Buffer
        cmd_grep.Stdout = &buf_result

        if grep_error := cmd_grep.Start(); grep_error != nil {
                fmt.Println("Error happened in execution ", grep_error)
                return
        }

        err := stdin_grep.Close()
        if err != nil {
                fmt.Println("Error happened in closing pipe", err)
                return
        }

        //make sure all the infor in the buffer could be read
        if err := cmd_grep.Wait(); err != nil {
                fmt.Println("Error happened in Wait process")
                return
        }
        fmt.Println(buf_result.String())

}
```
#### 3.2.2 命名管道

管道的一个不足之处是没有名字，因此，只能用于具有亲缘关系的进程间通信，在命名管道（ named pipe或FIFO）提出后，该限制得到了克服。FIFO不同于管道之处在于它提供一个路径名与之关联，以FIFO的文件形式存储于文件系统中。命名管道是一个设备文件，因此，即使进程与创建FIFO的进程不存在亲缘关系，只要可以访问该路径，就能够通过FIFO相互通信。值得注意的是，FIFO(first input first output)总是按照先进先出的原则工作，第一个被写入的数据将首先从管道中读出。

Linux下有两种方式创建命名管道。

1. 一是在Shell下交互地建立一个命名管道，二是在程序中使用系统函数建立命名管道。Shell方式下可使用mknod或mkfifo命令，下面命令使用mknod创建了⼀个命名管道：

```bash
mknod namedpipe
```

2. 创建命名管道的系统函数有两个： mknod和mkfifo。两个函数均定义在头文件sys/stat.h

函数原型如下：
```cpp
#include <sys/types.h>
#include <sys/stat.h>
int mknod(const char *path,mode_t mod,dev_t dev);
int mkfifo(const char *path,mode_t mode); 
```

#### 3.2.3 共享内存
共享内存是进程间通信中高效方便的方式之一。共享内存允许两个或更多进程访问同一块内存，就如同 malloc() 函数向不同进程返回了指向同一个物理内存区域的指针，两个进程可以对一块共享内存进行读写。

共享内存并未提供进程同步机制，使用共享内存完成进程间通信时，需要借助互斥量或者信号量来完成进程的同步。

**Notice:** 我们经常使用的 `sync.Mutex`，`sync.WaitGroup` 其实是进行线程间通讯的，用来协调多个goroutine对临界区的访问，原因是线程之间可以共享一块地址空间，所以互斥量与信号量的改变可以被各个线程感知。

这里**共享内存 + Mutex**实现的是进程间通讯，共享内存为各个进程提供了一块share的地址空间，从而可以感知到锁的变化。

```cpp
#include <sys/shm.h>

// shmget 用一个多个进程统一的 key 来申请指定位置的共享内存
int shmget(key_t key, size_t size, int shmflg);

// shmat 是用来允许本进程访问一块共享内存的函数，将这个内存区映射到本进程的虚拟地址空间。
void *shmat(int shm_id, const void *shm_addr, int shmflg);

// shmctl控制对这块共享内存的使用
int shmctl(int shm_id, int cmd, struct shmid_ds *buf);

// 当一个进程不再需要共享内存时，需要把它从进程地址空间中脱离。
int shmdt(const void *shm_addr);
```

### 3.3 消息队列

消息队列允许应用之间通过发消息的方式异步通讯，简单来说，发送者和消费者的生产效率通常是不一致的，那么我们就需要一种抽象模型去解耦，因此这里就可以引入消息队列，将任务暂时写入消息中间件，待消费者慢慢处理。消息中间件目前已经有了很多选择，例如RocketMQ、Kafka、Pulsar等等，Message queue带来很多便利的同时，也引入了一些技术上的复杂性，就像一个黑盒子一样，如果不能理解其原理，如果碰到了问题查起来也很蛋疼，今天我们就来看看如何着手实现一个简单的消息队列。

#### 存储
消息队列最核心的组件之一就是存储层，消息如何落地、如何读取，这里的技术选型是比较重要的一点。
例如
- RocketMQ 以及 Kafka 都是选择存储到本机，也就是本地文件系统；
- Pulsar 则是选择存储到分布式文件系统 bookKeeper 中
- 也有一些选择了分布式KV系统甚至是数据库，例如 Redis 自身也是支持 publish/consume 模型的
具体的选择哪一种实现方式只要还是看自己的业务场景，例如如果可靠性要求较高但对性能并不那么敏感的场景可以选择数据库作为存储介质。

### 3.4 线程间通讯
由于多线程共享地址空间和数据空间，一个线程的数据可以直接提供给其他线程使用，而不必通过操作系统内核的调度，但要做好同步/互斥mutex, 保护共享的全局变量。

- java 并发原语
    - 以JAVA为例，忙等待耗费CPU时间，wait-notify机制能够避免这一问题
    - `wait()`: 
        - wait()方法使得当前线程沉睡在某个锁上，等到另外一个线程调用notify()或者notifyAll()方法。
        - 线程必须拥有某对象的锁
        - 线程调用wait()方法，释放它对锁的拥有权，然后等待另外的线程来通知它
    - `notify()`:
        - notify()方法会唤醒一个等待当前对象的锁的线程。
        - 在执行notify()方法后，当前线程不会马上释放该对象锁，呈wait状态的线程也不能马上获取该对象锁，要等到执行notify()方法的线程将程序执行完，也即是退出synchronized代码块后，当前线程才会释放锁。
    - `notifyAll()`:
        - 唤醒所有沉睡在锁上的线程，被唤醒的的线程便会进入该对象的锁池中，锁池中的线程会去竞争该对象锁。
        - 调用了notify后只要一个线程会由等待池进入锁池，而notifyAll会将该对象等待池内的所有线程移动到锁池中，等待锁竞争。

- golang 并发原语
    - `sync.Cond`:
        - `c := sync.NewCond(&sync.Mutex{})` 初始化
        - `sync.Cond.Wait()` 方法在调用之前一定要使用获取互斥锁，否则会触发程序崩溃；
        - `sync.Cond.Signal()` 方法唤醒的 Goroutine 都是队列最前面、等待最久的 Goroutine；
        - `sync.Cond.Broadcast()` 会按照一定顺序广播通知等待的全部 Goroutine；
    - `sync.WaitGroup`:
        - 用于等待一组 goroutine 的结束
        - `wg := &sync.WaitGroup{}` 初始化
        - `sync.WaitGroup.Wait()` 当前goroutine等待计数器归零后继续运行
        - `sync.WaitGroup.Add(n)` 计数器+n
        - `sync.WaitGroup.Done()` 只是对Add方法的简单封装，计数器-1
        - 可以同时有多个 Goroutine 等待当前 sync.WaitGroup 计数器的归零，这些 Goroutine 会被同时唤醒；

# <span id = "anchor4">线程与进程</span>

- [一文看尽Python多线程与多进程](https://zhuanlan.zhihu.com/p/46368084)
- [线程、进程、调度基本概念梳理](https://www.jianshu.com/p/91c8600cb2ae)

线程与进程的关系：
- 进程是资源管理的最小单元；
- 线程是程序执行的最小单元。

即线程作为调度和分配的基本单位，进程作为资源分配的基本单位。一个进程的组成实体可以分为两大部分：线程集和资源集。进程中的线程是动态的对象；代表了进程指令的执行。资源，包括地址空间、打开的文件、用户信息等等，由进程内的线程共享。


### 进程的分类
进程通常有两种分类方式，一种是以运行状态分类，一种是以内核态和用户态划分。

1. 根据运行状态：

![](https://pic3.zhimg.com/80/v2-ef7510c1993010da8edf4c6416afd402_1440w.jpg)
- **运行**：该进程此刻正在执行。
- **等待(就绪)**：该进程能够运行，但是可能现在没轮到它执行，CPU 当前被分配给另一个进程。
- **睡眠**：进程正在睡眠无法运行，它在等待一个外部事件，调度器无法在下次任务切换的时候选择该进程，只有当外部事件到来之后，内核将该进程的状态改为等待状态，之后调度器才有机会选择它作为下一个运行的进程。
- **终止**：当进程退出时，会处于终止状态。

2. 根据用户态和内核态：
- 进程通常处于用户状态，只能访问自己的数据，无法干扰其他进程，甚至感知不到其他进程的存在。

- 如果进程想要访问系统资源或者功能，则必须切换到核心态。前面提到过进程可以通过系统调用的方式切换到内核态，除此之外，还有一种机制是中断，虽然系统调用也是通过软中断的方式实现，但是这里我们特指硬中断，系统调用是应用程序有意触发的，而中断的发生或多或少是不可预测的。通常这种中断的发生和正在运行的应用程序之间没有任何关系。例如当网络包到来时，可能和当前正在运行的进程不相干。当这种情况发生时，当前运行中的进程是无法感知到的，因为内核通过抢占调度的方式来处理中断。

### 线程的分类
线程一般分为内核级线程和用户级线程，这里主要介绍内核线程。

**内核线程**： 是直接由内核本身启动的进程。内核线程实际上是将内核函数委托给独立的进程，它与内核中的其他进程”并行”执行。内核线程经常被称之为内核守护进程。

他们执行下列任务

- 周期性地将修改的内存页与页来源块设备同步
- 如果内存页很少使用，则写入交换区
- 管理延时动作,　如２号进程接手内核进程的创建
- 实现文件系统的事务日志 

内核线程主要有两种类型

- 线程启动后一直等待，直至内核请求线程执行某一特定操作。
- 线程启动后按周期性间隔运行，检测特定资源的使用，在用量超出或低于预置的限制时采取行动。

内核线程由内核自身生成，其特点在于

- 它们在CPU的内核态执行，而不是用户态。
- 它们只可以访问虚拟地址空间的内核部分（高于TASK_SIZE的所有地址），但不能访问用户空间

### 计算密集型 & IO密集型
计算密集型任务的特点是要进行大量的计算，消耗CPU资源，比如计算圆周率、对视频进行高清解码等等，全靠CPU的运算能力。这种计算密集型任务虽然也可以用多任务完成，但是任务越多，花在任务切换的时间就越多，CPU执行任务的效率就越低，所以，要最高效地利用CPU，计算密集型任务同时进行的数量应当等于CPU的核心数。计算密集型任务由于主要消耗CPU资源，因此，代码运行效率至关重要。Python这样的脚本语言运行效率很低，完全不适合计算密集型任务。对于计算密集型任务，最好用C语言编写。

第二种任务的类型是IO密集型，涉及到网络、磁盘IO的任务都是IO密集型任务，这类任务的特点是CPU消耗很少，任务的大部分时间都在等待IO操作完成（因为IO的速度远远低于CPU和内存的速度）。对于IO密集型任务，任务越多，CPU效率越高，但也有一个限度。常见的大部分任务都是IO密集型任务，比如Web应用。IO密集型任务执行期间，99%的时间都花在IO上，花在CPU上的时间很少，因此，用运行速度极快的C语言替换用Python这样运行速度极低的脚本语言，完全无法提升运行效率。对于IO密集型任务，最合适的语言就是开发效率最高（代码量最少）的语言，脚本语言是首选，C语言最差。

综上，Python多线程相当于单核多线程，多线程有两个好处：CPU并行，IO并行，单核多线程相当于自断一臂。所以，在Python中，可以使用多线程，但不要指望能有效利用多核。如果一定要通过多线程利用多核，那只能通过C扩展来实现，不过这样就失去了Python简单易用的特点。不过，也不用过于担心，Python虽然不能利用多线程实现多核任务，但可以通过多进程实现多核任务。多个Python进程有各自独立的GIL锁，互不影响。

### 如何判断自己的任务是CPU密集型还是IO密集型？
multiprocessing这个module有一个dummy的sub module，它是基于multithread实现了multiprocessing的API。

假设你使用的是multiprocessing的Pool，是使用多进程实现了concurrency
```python
from multiprocessing import Pool
```
如果把这个代码改成下面这样，就变成多线程实现concurrency
```python
from multiprocessing.dummy import Pool
```
两种方式都跑一下，哪个速度快用哪个就行了。

## 多进程
### 基础调用
1. apply_async
- 函数原型：apply_async(func[, args=()[, kwds={}[, callback=None]]])
- p.apply_async(long_time_task, args=(i,))
- 其作用是向进程池提交需要执行的函数及参数， 各个进程采用非阻塞（异步）的调用方式，即每个子进程只管运行自己的，不管其它进程是否已经完成。这是默认方式。

2. map()
- 函数原型：map(func, iterable[, chunksize=None])
- Pool类中的map方法，与内置的map函数用法行为基本一致，它会使进程阻塞直到结果返回。 注意：虽然第二个参数是一个迭代器，但在实际使用中，必须在整个队列都就绪后，程序才会运行子进程。

3. map_async()
- 函数原型：map_async(func, iterable[, chunksize[, callback]])
- 与map用法一致，但是它是非阻塞的。其有关事项见apply_async。

4. close()
- 关闭进程池（pool），使其不在接受新的任务。

5. terminate()
- 结束工作进程，不在处理未处理的任务。

6. join()
- 主进程阻塞等待子进程的退出， join方法要在close或terminate之后使用。

```python
from multiprocessing import Pool, cpu_count
import os
import time


def long_time_task(i):
    print('子进程: {} - 任务{}'.format(os.getpid(), i))
    time.sleep(2)
    print("结果: {}".format(8 ** 20))


if __name__=='__main__':
    print("CPU内核数:{}".format(cpu_count()))
    print('当前母进程: {}'.format(os.getpid()))
    start = time.time()
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('等待所有子进程完成。')
    p.close()
    p.join()
    end = time.time()
    print("总共用时{}秒".format((end - start)))
```

### 进程池

```python
from multiprocessing import Pool, cpu_count
import os
import time


def long_time_task(i):
    print('子进程: {} - 任务{}'.format(os.getpid(), i))
    time.sleep(2)
    print("结果: {}".format(8 ** 20))


if __name__=='__main__':
    print("CPU内核数:{}".format(cpu_count()))
    print('当前母进程: {}'.format(os.getpid()))
    start = time.time()
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    p.close() 
    p.join()
```

- 对Pool对象调用join()方法会等待所有子进程执行完毕，主线程自身才结束，程序退出
- 调用join()之前必须先调用close()或terminate()方法，让其不再接受新的Process了。

# <span id = "anchor5">线程调度</span>

**linux内的线程调度 就是 进程调度：**

在Linux中，线程是由进程来实现，线程就是轻量级进程（ lightweight process ），因此在Linux中，线程的调度是按照进程的调度方式来进行调度的，也就是说线程是调度单元。Linux这样实现的线程的好处的之一是：线程调度直接使用进程调度就可以了，没必要再搞一个进程内的线程调度器。在Linux中，调度器是基于线程的调度策略（scheduling policy）和静态调度优先级（static scheduling priority）来决定那个线程来运行。

**linux进程分类：**

- 软实时进程：是硬实时进程的弱化，尽管仍然需要尽快完成实时任务，但是稍微晚一点也不会影响太大。不过这种软实时进程拿到的 CPU 时间至少要好过普通进程。

- 普通进程：大多数进程是没有特定时间约束的普通进程，但仍然需要根据其重要性分配优先级。

在 Linux 中进程会分为两大类，软实时进程和普通进程，当软实时进程存在时，会立即抢占普通进程的执行，此外软实时进程之间也有优先度的划分，优先级高的软实时进程会抢占优先级低的软实时进程。当没有软实时进程时，普通进程开始运作，它们根据优先级的不同划分不同大小的 CPU 时间执行，这很类似前面提到的基于时间片的简要模型。

### 调度策略类型
- **分时调度**：所有线程轮流使用 CPU 的使用权，平均/按优先级NICE值分配每个线程占用 CPU 的时间。
- **抢占式调度**：优先让优先级高的线程使用 CPU，如果线程的优先级相同，那么会随机选择一个(线程随机性)，Java使用的为抢占式调度。

### Linux 线程调度策略
在Linux中，调度器是基于线程的调度策略（scheduling policy）和静态调度优先级（static scheduling priority）来决定那个线程来运行。

Linux系统的三种调度策略：
1. **SCHED_OTHER**：分时调度策略（Linux线程默认的调度策略）。
2. **SCHED_FIFO**：实时调度策略，先到先服务。该策略简单的说就是一旦线程占用CPU则一直运行，一直运行直到有更高优先级任务到达或自己放弃。
3. **SCHED_RR**：实时调度策略，时间片轮转。给每个线程增加了一个时间片限制，当时间片用完后，系统将把该线程置于队列末尾。放在队列尾保证了所有具有相同优先级的RR任务的调度公平。

### 调度策略原则：
- 实时调度策略大于分时调度策略；
- 当实时进程/线程准备就绪后，如果当前CPU正在运行分时进程/线程，则实时进程/线程立即抢占分时进程/线程。
- 同样都是实时调度策略，优先级高的先执行。

### 策略详解　
**SCHED_OTHER 分时调度策略**：
1. 创建任务指定采用分时调度策略，并指定优先级nice值(-20~19)。
2. 将根据每个任务的nice值确定在CPU上的执行时间(counter)。
3. 如果没有等待资源，则将该任务加入到就绪队列中。
4. 调度程序遍历就绪队列中的任务，通过对每个任务动态优先级的计算(counter+20-nice)结果，选择计算结果最大的一个去运行，当这个时间片用完后(counter减至0)或者主动放弃CPU时，该任务将被放在就绪队列末尾(时间片用完)或等待队列(因等待资源而放弃CPU)中。
5. 此时调度程序重复上面计算过程，转到第4步。
6. 当调度程序发现所有就绪任务计算所得的权值都为不大于0时，重复第2步。


**SCHED_FIFO 实时调度策略**：
1. 创建进程时指定采用FIFO，并设置实时优先级rt_priority(1-99)。
2. 如果没有等待资源，则将该任务加入到就绪队列中。
3. 调度程序遍历就绪队列，根据实时优先级计算调度权值(1000+rt_priority),选择权值最高的任务使用cpu，该FIFO任务将一直占有CPU直到有优先级更高的任务就绪(即使优先级相同也不行)或者主动放弃(等待资源)。
4. 调度程序发现有优先级更高的任务到达(高优先级任务可能被中断或定时器任务唤醒，再或被当前运行的任务唤醒，等等)，则调度程序立即在当前任务堆栈中保存当前CPU寄存器的所有数据，重新从高优先级任务的堆栈中加载寄存器数据到CPU，此时高优先级的任务开始运行。重复第3步。
5. 如果当前任务因等待资源而主动放弃CPU使用权，则该任务将从就绪队列中删除，加入等待队列，此时重复第3步。

**SCHED_RR 实时调度策略**：
1. 创建任务时指定调度参数为RR，并设置任务的实时优先级和nice值(nice值将会转换为该任务的时间片的长度)。
2. 如果没有等待资源，则将该任务加入到就绪队列中。
3. 调度程序遍历就绪队列，根据实时优先级计算调度权值(1000+rt_priority),选择权值最高的任务使用CPU。
4. 如果就绪队列中的RR任务时间片为0，则会根据nice值设置该任务的时间片，同时将该任务放入就绪队列的末尾。重复步骤3。
5. 当前任务由于等待资源而主动退出CPU，则其加入等待队列中。重复步骤3。

[Linux 线程调度浅析](https://blog.csdn.net/s13335358730/article/details/86257259?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-3&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-3)