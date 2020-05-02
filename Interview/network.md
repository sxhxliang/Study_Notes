# Network 计算机网络

## 0. 计算机网络4/7层协议体系

### 0.1 理清概念
#### TCP/IP
TCP/IP是Transmission Control Protocol/Internet Protocol的简写，译名为传输控制协议/因特网协议，是Internet最基本的协议。TCP/IP是这个协议族的统称，它采用了4层的层级结构，**而不是指TCP + IP两个协议的总和**！！

#### IP
IP协议包含源主机地址、目标主机地址，还有TCP数据信息。但IP协议没有做任何事情来确认数据包是否按顺序发送或者包是否被破坏，所以IP数据包是不可靠的。

#### TCP
面向连接的通信协议，通过三次握手建立连接（socket通过TCP/IP连接时就是经过3次握手），通信完成后要关闭连接，它只用于端对端的通讯
TCP协议通过3次握手建立起一个可靠的连接，通过将数据包进行排序以及检验的方式，可以提供一种可靠的数据流服务
TCP可以限制数据的发送速度，间接地控制流量

#### UDP
面向无连接的通讯协议，UDP数据包括原端口号信息以及目标端口号信息，它可以实现广播发送
由于UDP通讯不需要接收方确认，所以属于不可靠的传输，可能会出现丢包现象

![](https://img-blog.csdn.net/20180807153922338?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0JleW9uZF8yMDE2/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

- 4层是指TCP/IP四层模型，主要包括：应用层、运输层、网络层和网络接口层。
- 7层是指OSI七层协议模型，主要是：应用层、表示层、会话层、传输层、网络层、数据链路层、物理层。

![](https://img-blog.csdn.net/20180807154323965?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0JleW9uZF8yMDE2/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

要点：
1. TCP 属于传输层协议，IP 属于网络层协议
2. HTTP 属于应用层协议，我们通常请求网络就是使用HTTP，不需要直接使用TCP和IP这两个协议


## 1. TCP 三次握手和四次握手

![](https://pic3.zhimg.com/80/v2-e8aaab48ff996e5cd8a5b39dc450bd6a_1440w.jpg)

- 服务器接收到 SYN 包时，此时的 TCP 链接称作半链接，将被服务端内核放入半链接队列
- 服务器接收到 ACK 包时，将会从半链接队列中找到该链接，弹出它，并添加到完成三次握手的链接队列中。

### 1.1 为什么会有 TIME_WAIT ?

从TCP状态迁移图可知，只有首先调用close()发起主动关闭的一方才会进入TIME_WAIT状态，而且是必须进入。从图中还可看到，进入TIME_WAIT状态的TCP连接需要经过2MSL才能回到初始状态，其中，MSL是指`Max Segment Lifetime`，即数据包在网络中的最大生存时间。每种TCP协议的实现方法均要指定一个合适的MSL值，如RFC1122给出的建议值为2分钟，又如Berkeley体系的TCP实现通常选择30秒作为MSL值。这意味着TIME_WAIT的典型持续时间为1-4分钟。

### 1.2 TIME_WAIT状态的存在有两个理由:

1. 让4次握手关闭流程更加可靠：4次握手的最后一个ACK是是由主动关闭方发送出去的，若这个ACK丢失，被动关闭方会再次发一个FIN过来。若主动关闭方能够保持一个2MSL的TIME_WAIT状态，则有更大的机会重新发送之前丢失的ACK包。

2. 防止lost duplicate对后续新建正常链接的传输造成破坏：lost duplicate在实际的网络中非常常见，经常是由于路由器产生故障，路径无法收敛，导致一个packet在路由器A，B，C之间做类似死循环的跳转。IP头部有个TTL，限制了一个包在网络中的最大跳数，因此这个包有两种命运，要么最后TTL变为0，在网络中消失；要么TTL在变为0之前路由器路径收敛，它凭借剩余的TTL跳数终于到达目的地。TCP通过超时重传机制重发FIN + ACK包，使得这些旧的 lost package 被抛弃。
