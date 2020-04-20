# 算法
准备阿里面试时候发现自己基础算法太薄弱了，故加以整理。

## 排序
[十大经典排序算法](https://www.cnblogs.com/onepixel/p/7674659.html)
![](https://uploadfiles.nowcoder.com/images/20160824/616717_1472008641084_2F78A57BC1F1F11FDF7DA1A97FAF8049)


### 冒泡排序 bubblesort
![](https://images2017.cnblogs.com/blog/849589/201710/849589-20171015223238449-2146169197.gif)

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

![](https://images2017.cnblogs.com/blog/849589/201710/849589-20171015230936371-1413523412.gif)

快速排序的基本思想：通过一趟排序将待排记录分隔成独立的两部分，其中一部分记录的关键字均比另一部分的关键字小，则可分别对这两部分记录继续进行排序，以达到整个序列有序。

```python
def quickSort(arr, left, right): 
    if left < right:
        partitionIndex = partition(arr, left, right)
        quickSort(arr, left, partitionIndex - 1)
        quickSort(arr, partitionIndex + 1, right)
    return arr
}
 
function partition(arr, left ,right):   // 分区操作
    pivot = left                  // 设定基准值（pivot）
    index = pivot + 1
    for i in range(index, right+1):
        if arr[i] < arr[pivot]:
            arr[i], arr[index] = arr[index], arr[i]
            index += 1

    arr[pivot], arr[index - 1] = arr[index - 1], arr[pivot]
    return index - 1
```

- 最差情况是数组有序，每次自区间只减少pivot位置的元素，`O(N^2)`
- 最优情况和平均情况为 `O(NlogN)`

### 桶排序 bucketsort

- 设置一个定量的数组当作空桶；
- 遍历输入数据，并且把数据一个一个放到对应的桶里去；
- 对每个不是空的桶进行排序；
- 从不是空的桶里把排好序的数据拼接起来。 

![](https://images2017.cnblogs.com/blog/849589/201710/849589-20171015232107090-1920702011.png)

```python
def bucketsort(arr, bucketsize):
    minval, maxval = min(arr), max(arr)
    buckets_num = (maxval - minval) // bucketsize + 1 
    buckets = [[] for _ in range(buckets_num)]
    for a in arr:
        buckets[(a - minval) // bucketsize].append(a)
    
    result = []
    for bucket in buckets:
        if bucket:
            result.extend(sorted(bucket))
    return result
```

- `O(N)+O(M * (N/M) * log(N/M))=O(N + N * (logN-logM)) = O(N + NlogN - NlogM)`
- 最优情况下，桶的个数M=N个,每个桶里面有一个数据，这样时间复杂度为O(N)
- 桶的数目越多，空间越大，时间复杂度越低


### 选择排序 selectsort
![](https://images2017.cnblogs.com/blog/849589/201710/849589-20171015224719590-1433219824.gif)

```python
def selectionSort(arr):
    for i in range(len(arr)):
        minIndex = i;
        for j in range(i+1, len(arr)):
            if(arr[j] < arr[minIndex]):     // 寻找最小的数
                minIndex = j;                 // 将最小数的索引保存
        arr[i], arr[minIndex] = arr[minIndex], arr[i]
    return arr
```

- 无论数据初始状态如何，都要查找N次最小值，故最优最差复杂度均为 `O(N^2)`

### 归并排序 mergesort
![](https://images2017.cnblogs.com/blog/849589/201710/849589-20171015230557043-37375010.gif)

归并排序是建立在归并操作上的一种有效的排序算法。该算法是采用分治法（Divide and Conquer）的一个非常典型的应用。将已有序的子序列合并，得到完全有序的序列；即先使每个子序列有序，再使子序列段间有序。若将两个有序表合并成一个有序表，称为2-路归并。 

```python
def mergeSort(arr) {
    if (len(arr) < 2):
        return arr
    middle = len(arr) // 2
    left = arr[:middle]
    right = arr[middle:]
    return merge(mergeSort(left), mergeSort(right))
}
 
function merge(left, right) {
    result = []
 
    while len(left) > 0 and len(right) > 0:
        if left[0] <= right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
 
    result.extend(left)
    result.extend(right)
    return result
}
```

- 归并排序是一种稳定的排序算法，不受数据初始化状态影响
- 由于一共要进行logN次归并，每次归并都对全部数据进行操作，所以复杂度为`O(NlogN)`

### 插入排序 insertsort
![](https://images2017.cnblogs.com/blog/849589/201710/849589-20171015225645277-1151100000.gif)

插入排序（Insertion-Sort）的算法描述是一种简单直观的排序算法。它的工作原理是通过构建有序序列，对于未排序数据，在已排序序列中从后向前扫描，找到相应位置并插入。

```python
def insertionSort(arr):
    for i in range(len(arr)):
        preIndex = i - 1;
        current = arr[i];
        while preIndex >= 0 and arr[preIndex] > current:
            arr[preIndex + 1] = arr[preIndex]
            preIndex--
        arr[preIndex + 1] = current;
    return arr
```

- 和冒泡排序相似，当数组有序时，只需要遍历一次数组，最优复杂度 `O(N)`
- 最差复杂度和平均复杂度都是 `O(N^2)`

### 希尔排序 Shellsort

![](https://images2015.cnblogs.com/blog/1024555/201611/1024555-20161128110416068-1421707828.png)

希尔排序是把记录按下标的一定增量(GAP)分组，对每组使用直接插入排序算法排序；随着增量逐渐减少，每组包含的关键词越来越多，数组也越来越有序；当增量减至1时，整个文件恰被分成一组，算法便终止。

```python
def shellSort(arr): 
    n = len(arr)
    gap = int(n/2)
  
    while gap > 0: 
        for i in range(gap, n): 
            temp = arr[i] 
            j = i 
            while j >= gap and arr[j-gap] >temp: 
                arr[j] = arr[j-gap] 
                j -= gap 
            arr[j] = temp 
        gap = gap // 2
```

- 最优时间复杂度：`O(n*log(n))`
- 最坏时间复杂度：`O(n^2)`，间隔序列取得很糟糕；`O(n*(log(n))^2)`，间隔序列取得已知条件下比较好
- 平均时间复杂度：取决于间隔序列如何取
- 最坏空间复杂度：总共`O(n)`，辅助`O(n)`
