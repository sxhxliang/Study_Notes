# Go 语言学习笔记

## 基本语法
### 判断
```go
if  i > 0 {
  func1()
} else {
  func2()
}

// 可以在判断前初始化一个变量，作用域内有效
switch os := runtime.GOOS; os {
	case "darwin":
		fmt.Println("OS X.")
	case "linux":
		fmt.Println("Linux.")
	default:
		fmt.Printf("%s.\n", os)
	}
  
```
### 循环
```go
// C-Style 循环
for i:=0; i<10; i++ {
  func()
}

// 相当于 while 循环
for i < 100 {
  func()
}

// Range-Style 循环
for i, x := range lst {
    dosomething()
}
```

### 数组
- Go的数组不可以改变大小
- 数组长度同样是数据类型的一部分

```go
var s = [10]string
primes := [6]int{2, 3, 5, 7, 11, 13}
```

### 切片
- 在某种程度上说是变长的
- 切片不存储数据，只是原数组中一部分的引用
- len() 切片的长度, cap() 切片底层数组长度

```
b := make([]int, 0, 5) // len(b)=0, cap(b)=5

var s []int = primes[1:3] // 现有数组切片

array := [6]int{2, 3, 5, 7, 11, 13} // 新建一个数组

slice := []int{2, 3, 5, 7, 11, 13} // 先新建一个数组，再建立一个引用它的切片

fmt.Println(len(s), cap(s))
```

### Channel 通道
Channel通过解决数据共享问题，让并发编程变得更加清晰。

通道是一个通信管道，它用于go协程之间传递数据。换句话说，go协程可以通过通道，传递数据给另外一个go协程。其结果就是，在任何时候，仅有一个go协程可以访问数据。

```go
c1 := make(chan int)      \\ Zero Channel
c2 := make(chan int, 10)  \\ 有缓冲通道

go func1(ch chan int){
	ch <- 10  \\ 阻塞，接受者未准备
}(c1)

go func2(ch chan int){
	c2 <- 10  \\ 不阻塞，存进入缓冲区
}(c2)

<- c1     \\ c1接收准备好了，func1 继续执行
```

- 对于无缓冲通道，必须在接收端准备好了才能发送，否则会造成死锁。

```
// Deadlock, All goroutines are asleep 
ch := make(chan int)
ch <- 9
fmt.Println(<-ch) 

// No deadlock
ch := make(chan int)
go func(){
    fmt.Println(<-ch) 
}()
ch <- 9
```
**遍历channel的方式**
```
ch := make(chan int, 10)
for i := range ch {
    fmt.Println(i)
}
// 这样写也会报错，all goroutines are asleep
// 原因是只有当ch被关闭之后才能跳出循环
```


### Panic
[Golang: 深入理解panic and recover](https://ieevee.com/tech/2017/11/23/go-panic.html)
Golang里比较常见的错误处理方法是返回error给调用者，但如果是无法恢复的错误，返回error也没有意义，此时可以选择主动触发panic。

除了代码中主动触发的panic，程序运行过程中也会因为出现某些错误而触发panic（例如数组越界、往关闭的channel发送数据等）。

panic会停掉当前正在执行的程序（注意，不只是协程），但是与os.Exit(-1)这种直愣愣的退出不同，panic的撤退比较有秩序，他会以后进先出的方式处理完当前goroutine已经defer挂上去的任务，执行完毕后再退出整个程序。

```go
func main() {
	var user = os.Getenv("USER_")
	go func() {
		defer func() {
			fmt.Println("defer here")
		}()
		if user == "" {
			panic("should set user env.")
		}
	}()
	time.Sleep(1 * time.Second)
	fmt.Printf("get result %d\r\n", result)
}

\\ ------------------------------------
\\ 可输出“defer here”，不输出“get result”
\\ ------------------------------------
```

