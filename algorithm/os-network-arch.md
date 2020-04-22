# 操作系统和网络

## 1. TCP-IP 三次握手和四次握手

![](https://pic3.zhimg.com/80/v2-e8aaab48ff996e5cd8a5b39dc450bd6a_1440w.jpg)

- 服务器接收到 SYN 包时，此时的 TCP 链接称作半链接，将被服务端内核放入半链接队列
- 服务器接收到 ACK 包时，将会从半链接队列中找到该链接，弹出它，并添加到完成三次握手的链接队列中。

### 1.1 为什么会有 TIME_WAIT ?

从TCP状态迁移图可知，只有首先调用close()发起主动关闭的一方才会进入TIME_WAIT状态，而且是必须进入。从图中还可看到，进入TIME_WAIT状态的TCP连接需要经过2MSL才能回到初始状态，其中，MSL是指`Max Segment Lifetime`，即数据包在网络中的最大生存时间。每种TCP协议的实现方法均要指定一个合适的MSL值，如RFC1122给出的建议值为2分钟，又如Berkeley体系的TCP实现通常选择30秒作为MSL值。这意味着TIME_WAIT的典型持续时间为1-4分钟。

### 1.2 TIME_WAIT状态的存在有两个理由:

1. 让4次握手关闭流程更加可靠：4次握手的最后一个ACK是是由主动关闭方发送出去的，若这个ACK丢失，被动关闭方会再次发一个FIN过来。若主动关闭方能够保持一个2MSL的TIME_WAIT状态，则有更大的机会重新发送之前丢失的ACK包。

2. 防止lost duplicate对后续新建正常链接的传输造成破坏：lost duplicate在实际的网络中非常常见，经常是由于路由器产生故障，路径无法收敛，导致一个packet在路由器A，B，C之间做类似死循环的跳转。IP头部有个TTL，限制了一个包在网络中的最大跳数，因此这个包有两种命运，要么最后TTL变为0，在网络中消失；要么TTL在变为0之前路由器路径收敛，它凭借剩余的TTL跳数终于到达目的地。TCP通过超时重传机制重发FIN + ACK包，使得这些旧的 lost package 被抛弃。

## 2. 系统调用 
[系统调用详解](https://blog.csdn.net/gatieme/article/details/50779184)

linux内核中设置了一组用于实现系统功能的子程序，称为系统调用。系统调用和普通库函数调用非常相似，只是系统调用由操作系统核心提供，运行于内核态，而普通的函数调用由函数库或用户自己提供，运行于用户态。

一般地，系统调用都是通过软件中断实现的，x86系统上的软件中断由`int $0x80`指令产生，而128号异常处理程序就是系统调用处理程序`system_call()`。

### 2.1 API 与 系统调用
- 程序员调用的是API（API函数），然后通过与系统调用共同完成函数的功能，因此，**API是一个提供给应用程序的接口**，一组函数，是与程序员进行直接交互的。
- 系统调用则不与程序员进行交互的，它根据API函数，通过一个软中断机制向内核提交请求，以获取内核服务的接口。
- 并不是所有的API函数都一一对应一个系统调用，有时，一个API函数会需要几个系统调用来共同完成函数的功能，甚至还有一些API函数不需要调用相应的系统调用（因此它所完成的不是内核提供的服务）

### 2.2.1 内核态 与 用户态
![](https://upload-images.jianshu.io/upload_images/2744546-2b78e131a118b774.png?imageMogr2/auto-orient/strip|imageView2/2/w/366/format/webp)
- 内核态：控制计算机的硬件资源，并提供上层应用程序运行的环境。
- 用户态：上层应用程序的活动空间，应用程序的执行必须依托于内核提供的资源。
- 系统调用：为了使上层应用能够访问到这些资源，内核为上层应用提供访问的接口。

![](https://upload-images.jianshu.io/upload_images/2744546-cc53e9112a785a83.png?imageMogr2/auto-orient/strip|imageView2/2/w/742/format/webp)


### 2.2.2 用户态与内核态的切换
用户态切换为内核态的三种情况：
- 系统调用 (软中断)
- 异常事件： 当CPU正在执行运行在用户态的程序时，突然发生某些预先不可知的异常事件，这个时候就会触发从当前用户态执行的进程转向内核态执行相关的异常事件，典型的如缺页异常。
- 外围设备的中断：当外围设备完成用户的请求操作后，会像CPU发出中断信号，此时，CPU就会暂停执行下一条即将要执行的指令，转而去执行中断信号对应的处理程序，如果先前执行的指令是在用户态下，则自然就发生从用户态到内核态的转换。

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

## 3. 死锁
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

## 3. 进程间通讯
Socket，管道、消息队列、信号量、共享内存
### 3.1 Socket

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







