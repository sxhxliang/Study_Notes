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
for i:=0; i<10; i++ {
  func()
}

// 省略初始化条件与后处理，相当于while
for i < 100 {
  func()
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
var s []int = primes[1:3] // 现有数组切片

array := [6]int{2, 3, 5, 7, 11, 13} // 新建一个数组

slice := []int{2, 3, 5, 7, 11, 13} // 先新建一个数组，再建立一个引用它的切片

fmt.Println(len(s), cap(s))
```



