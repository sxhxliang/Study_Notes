# VMware Fault Tolerant VM

## Overview
本节介绍了VMware的一个自动容错的虚拟机主从备份系统。

实现应用程序的**零停机**和**零数据丢失**，与GFS关注于保证数据一致性的容错机制不同，VMware FT 拷贝了整台机器的运行状态（包括内存，寄存器等），其主要目的是保障某些重要应用始终可用。

重要设定：
1. 备份的对象是虚拟机。直接同步两台物理机非常困难，而虚拟机运行在物理机上，管理程序（hypervisor）可以全盘空置虚拟机的运行便于保证主从系统的一致性。
2. 虚拟机被限制为单核系统。多核系统存在不确定性，无法保证指令的运行顺序，会导致内存及输出不同步。
3. 主从机公用同一块磁盘。

## Deterministic state machine
备份一个虚拟机可以被建模成维护一个确定状态自动机，其主要难点在于：
1. 正确地捕捉 所有的输入 以及 non-deterministc操作 
2. 将 输入 以及 non-deterministc操作 正确地应用在备份机,以保证其确定性地执行
3. 防止性能下降太多

## 介绍

![](https://lh3.googleusercontent.com/proxy/qvyarRSOQPmpXRu0Ja_Mn4qnYY3f1bMqfwGGJLfIeGKUl0HL5mlmc6uGjrVViNoldER-ppA7ckV1w1V1LJefOBO-8RPoPoU9DKO8hOqZo9qNZySPt3UuIBie36KyUfzl_w)

一般会有两台机子，primary作为主机，backup作为备份机，正常情况下，外部事务（external events）都是由primary处理，同时primary通过logging channel传递log entries，这里传递的其实就是上面所说的operations，和raft的策略相同。

实际上是由"goes live"的机子来处理外部事务，类比一下raft里的leader。

#### 什么时候主机会发送信息给备份机？即什么时候会开始备份？

有可能会影响他们操作不一致时
不是deterministic executions的时候（比如说时钟中断/IO中断）。
这里的deterministic execution的意思应该是，输入x必定会输出一个确定的值，但像中断就不是这类指令，它完全是由外部决定的。

#### VM FT在什么情况下会产生不一致

在一般的情况下，大多的指令在主机和备份机上都是相同的。在第一节中介绍过，VM FT的replication的level是在machine level上的。即如果寄存器和内存的内容都控制得相同的话，指令也是保持一致的。

1. 来自外部的输入
- 比如说由dma运载的数据，或者中断。前者i/o接口直接向dma提出请求，会改变内存或者寄存器中的内容，后者会改变指令执行的顺序。

2. 不是状态函数的指令
- 即使主机备份机有相同状态的情况下也会输出不同结果的指令，比如说读取当前时间。

3. 多核竞争的情况
- 如果有多核竞争的话，指令最后被哪个cpu运行是不确定的，所以寄存器和内存也不可控。会产生分歧。

#### VM FT 如何处理这些不一致的情况？

1. 时钟中断
- 目标是让中断指令在备份机的log entries也在正确的点出现。
- 简单来说，VM FT会在指令x之前记录下这个中断，然后分别传递给primary和backup。backup会关闭它自身的timer hardware，ft能在指令x来之前，看到传递给它的带有中断指令的log entry，然后ft会告诉cpu，在x指令执行前，需要执行一次中断。back实际上模拟了一次这个过程，自身的timer hardware已经关闭了。

2. 外部数据
- ft处理的外部数据仅仅是网络包。
- 对于主机来说, ft会通过nic（网卡）把数据包先复制到自己的"bounce buffer"处。（不会直接进入内存）
- 然后让nic执行dma和中断写入buffer（注：每个网卡都有自己的dma engine，网络包通过dma直接和内存打交道，不需要通过cpu，如下图，只要在数据流通结束时（接受完，发送完）才会以中断的形式告诉cpu）
- 等ft获得了中断（意味着数据接受完毕了）ft会先暂停primary，然后把bounce buffer内的数据直接拷贝到内存中，然后ft会在主机中模拟nic产生的中断。
- 在主机中完成后，会把数据包和中断传递给备份机。备份机的操作和时钟中断一致，加了一项拷贝数据包进内存。

#### Brain-Split Situation

裂脑问题：来源于医学上的裂脑人问题，裂脑人用于左右脑沟通的胼胝体先天不完善或后天切除，导致左右脑互相不知道对方的存在，从而诞生出"两个意识"的情况。

在图1中可以看到，primary和backup的联通主要依靠的是logging channel，如果此时logging channel的网络出现问题，primary和backup都认为对方挂了。

注意到primary和backup共用一个disk，此时disk充当他们沟通的媒介，disk有自动的test-and-set：
- 如果primary和backup都认为对方挂了，但都没挂，那么就会开始test-and-set，会有一方胜出。
- 或者本来就只有一个goes live的，一个挂了，那直接goes live这个的胜出。

## FT Protocal
Output Requirement：如果备份机在主机宕机后起用，那么备份机必须以一种与主机已输出的信息完全一致的方式运行。

也就是切换后对client来说察觉不到任何中断/不一致/或者丢失信息的情况。

![](https://mr-dai.github.io/img/primary-backup-replication/ft-protocol.png)

实现方式如图2，OS采用非阻塞的网络与磁盘输出，异步中断。主机的每条指令都会存入log buffer，不必等待备份机接收指令；同时主机通过延迟输出（delay output）可以不停机地继续执行下面的指令，当备份机发来ack后再进行输出。

即使如此，还是会存在重复输出与丢失输出的情况：
- ACK由于网络原因丢失导致主机不输出。
- 备份机不能确定主机宕机前是否发出了最后一条输入，所以备份机会再发一次。
- 好在TCP协议有相应机制处理丢包和重复发包


## Terms
**A virtual machine (VM)**： is a virtual environment that functions as a virtual computer system with its own CPU, memory, network interface, and storage, created on a physical hardware system. Software called a hypervisor separates the machine’s resources from the hardware and distributes them appropriately so they can be used by the VM.

**DMA**: (Direct Memory Access，直接存储器访问) 是所有现代电脑的重要特色，它允许不同速度的硬件装置来将数据从一个地址空间复制到另外一个地址空间，而不需要依赖于 CPU 的大量中断负载。否则，CPU 需要从来源把每一片段的资料复制到暂存器，然后把它们再次写回到新的地方。在这个时间中，CPU 对于其他的工作来说就无法使用。 

所以在执行DMA时DMA控制器直接从CPU手里掌管总线，CPU挂起或者只执行内部操作，等数据传输完后向CPU发出I/O中断，交还总线控制权给CPU。

**NIC**：网络接口控制器（Network Interface Controller），即网卡，是一块被设计用来允许计算机在计算机网络上进行通讯的计算机硬件。每一个网卡都有一个被称为MAC地址的独一无二的48位串行号，它使得用户可以通过电缆或无线相互连接。