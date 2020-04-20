# 算法
准备阿里面试时候发现自己基础算法太薄弱了，故加以整理。

## 排序
[十大经典排序算法](https://www.cnblogs.com/onepixel/p/7674659.html)
![](https://uploadfiles.nowcoder.com/images/20160824/616717_1472008641084_2F78A57BC1F1F11FDF7DA1A97FAF8049)


### 冒泡排序 bubblesort
```python
def bubbleSort(arr):
    flop = 0    
    for i in range(len(arr)):
        for j in range(len(arr) - 1 - i):
            if arr[j] > arr[j+1]:                       // 相邻元素两两对比
                arr[j], arr[j+1] = arr[j+1], arr[j]        // 元素交换
                flop += 1
        if flop == 0:
            break
    return arr
```

- 最优情况为已经排序好，只需要冒泡一遍, `O(N)`
- 最差情况是顺序反向，需要冒泡N次，`O(N^2)`

### 快速排序 quicksort

### 桶排序 bucketsort



### 选择排序 selectsort

### 归并排序 mergesort

### 插入排序 insertsort
