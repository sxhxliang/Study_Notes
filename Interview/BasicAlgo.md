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
 
def partition(left, right, arr):
    pivot_val = arr[right]
    store_idx = left
    for i in range(left, right):
        if arr[i] < pivot_val:
            arr[i], arr[store_idx] = arr[store_idx], arr[i]
            store_idx += 1
    arr[store_idx], arr[right] = arr[right], arr[store_idx]
    return store_idx
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

## KMP 算法
![KMP详解](http://www.ruanyifeng.com/blog/2013/05/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm.html)

KMP算法用来匹配字符串S中子串P的出现次数，时间复杂度为`O(N+P)`

```python
        def constructdp(pattern):
            dp = [{c:0 for c in chardict} for _ in range(len(pattern) + 1)]
            X = 0
            dp[0][pattern[0]] = 1  # i 先走一步，保证领先于影子X
            for i in range(1, len(pattern)):
                for ch in chardict:
                    if ch == pattern[i]:
                        dp[i][ch] = i + 1
                    else:
                        dp[i][ch] = dp[X][ch]
                    
                X = dp[X][pattern[i]]
            return dp
        
        def search(seq, dp):
            j = 0
            for i, ch in enumerate(seq):
                if ch in chardict:
                    j = dp[j][ch]
                else:
                    j = 0
                if j == len(dp) - 1:
                    return i + 2 - len(dp)
            return -1
            
        dp = constructdp(needle)
        return search(haystack, dp)
```

## 查找有序序列被swap的两个数字

Swap 有两种情况：
- `[1,4,3,2,5]`：间隔调换，逆序对有两组（4，3），（3，2），涉及调换的是 第一组的前一个，第二组的后一个
- `[1,3,2,4,5]`：相邻调换，逆序对有一组（3，2），第一组的第一个，第一组的第二个


```python
def f(nums):
    x = y = None
    for i in range(len(nums)-1):
        if nums[i] > nums[i+1]:
            y = nums[i + 1]     # 找到第一/二组第二个
            if x is None:
                x = nums[i]     # 找到第一组第一个
    return x, y
```

**典型题：**
- leetcode 99 恢复二叉搜索树：其实就是inorder遍历二叉树节点（类比遍历数组），按上述算法找到逆序的两个元素。

## 二分查找

使用统一的双闭区间实现 `binarySearch`, `lowerbound`, `upperbound`.
只要搞清楚我们缩小区间的方向，以及终止时lo,hi指针的位置即可。

```python
def binarySearch(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        elif nums[mid] > target:
            right = mid - 1
    return -1

"""
e.g. leftbound(num, target=4)
返回的坐标左侧元素均小于target
[1,1,3,3,3,4,5] target=2 - return 2

[1,1,3,3,3,4,5] target=3 - return 2

"""

# 核心思想：左侧都是小于target的元素，相等时缩小右侧区间边界
def leftbound(nums, target):
    left = 0
    right = len(nums)
    while left < right:
        mid = left + (right - left) // 2
        print(left, right, mid)
        if nums[mid] == target:
            right = mid     # 缩小右侧边界
        elif nums[mid] > target:
            right = mid
        elif nums[mid] < target:
            left = mid + 1  # 左侧均小于target
    return left

"""

e.g. upperbound(num, target=4)

返回的坐标位置元素小于等于target
[1,1,3,3,3,4,5] target=3 - return 4

[1,1,3,3,3,4,5] target=4 - return 4
"""
# 核心思想，右侧均是大于target元素，相等缩小左侧边界，可能越界
def rightbound(nums, target):
    left = 0
    right = len(nums)
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            left = mid + 1      # 缩小左侧边界
        elif nums[mid] < target:
            left = mid + 1
        elif nums[mid] > target:
            right = mid
    return left - 1     # 可能越界            
```

## 回溯法

回溯法的套路模版, 本质上就是寻找一个N叉树的所有可行路径

```python
def backtrack(first=0):
    if first == len(arr):
        result.append(path[:])  # 拷贝并存储一个可行解
    
    for i in range(first, len(arr)):  # 从start本身开始，遍历剩余可行路径
        if valid(arr[i]):
            path.append(i)  # 扩增路径
            mark_visited(i) # 标记已经访问
            backtrack(first + 1)
            path.pop(-1)
            unmark_visited(i)

result = []
path = []
backtrack(0)
return result

```

### 1. N皇后问题 [Leetcode 51](https://leetcode.com/problems/n-queens/)
```python
# 核心代码
def backtrack(first=0):
    if first == n:
        result.append(path[:])
    for i in range(n):
        if col_valid[i] and uphill_valid[first+i] and downhill_valid[first-i]:
            path.append(i)
            col_valid[i] = uphill_valid[first+i] = downhill_valid[first-i] = False
            backtrack(first + 1)
            path.pop(-1)
            col_valid[i] = uphill_valid[first+i] = downhill_valid[first-i] = True
```

### 2. 数独问题 [Leetcode 37](https://leetcode.com/problems/sudoku-solver/submissions/)
```python
# 核心代码
def backtrack(first):
    if first == len(queue):
        return True
    x, y, block = queue[first]
            
    for i in range(1, 10):
        i = str(i)
        if not row_used[x][i] and not col_used[y][i] and not block_used[block][i]:
            path.append(i)
            row_used[x][i] = col_used[y][i] = block_used[block][i] = True
            
            if backtrack(first + 1):  # 仅需找到一个可行解
                return True
                
            path.pop(-1)
            row_used[x][i] = col_used[y][i] = block_used[block][i] = False
     return False
```

### 层次化遍历二叉树

基本想法是使用队列，每次队头弹出元素，队尾加入该元素的左右子节点，保证子节点加入顺序是按层次的。

```python
level = ptr = 0
result = []
queue = [[root, 1]]
while ptr < len(queue):
    node, l = queue[ptr]
    if l > level:
        level += 1
        result.append([])
    result[-1].append(node.val)
    if node.left:
        queue.append([node.left, l + 1])
    if node.right:
        queue.append([node.right, l + 1])
    ptr += 1
return result
```

### 拓扑排序

是判断一张图是否是 DAG 的方式，如果有向图无环，那么最终所有节点都将被计入的拓扑排序序列。

算法思想是每次删除一个入度为0的节点，更新其他节点的入度，直到无法删除节点为止。（火星词典）

### 区间调度

#### 1. 最多区间调度：
最简单版本，求出最多的不重叠区间数量，这里可以使用贪心（动规的特例），因为dp数组的单调递增性质。

设定 `dp[k]` 为前`i`个区间最多不重叠区间的数量，转移方程为：
- `dp[i] = max(dp[i-1], dp[j] + 1)`
- 决策：
    - 不选第i个区间: `dp[i-1]` 
    - 选第i个区间: `dp[j] + 1`, `j`为左边最近的一个与i不重叠的区间。

那么如何找j呢？暴力方法是线性搜索，这样总的复杂度是n2; 但是! 我们注意到dp数组的单调递增性, 每一次只增加1或不增加：

```
1,1,1,2,2,3,3,4,4,4,?
              ^     ^
              j     i
```
假设`dp[i-1] == 4`, 那么如果想让`dp[j]+1 > dp[k-1]`，必须要使得值为4的第一个区间与当前区间不重叠!

我们可以记录一个位置数组 pos[dp_val] = id, 这样就可以在O（1）时间下找到最近的起始区间，进而判断是否重叠。

简化一下我们发现完全不用dp数组了，线性地扫一遍即可，每次发现一个不重叠区间就cnt+=1

#### 2. 最长区间调度

进阶版本，求出最长的不重叠区间长度。

这里就必须使用dp了，因为现在的dp数组虽然是单调递增的，但该序列不是连续增加的：

```
1,3,7,10,14,20
```

假设当前区间长度为 `int[i]`，那么我们必然要找 `dp[j] + int[i] > dp[i-1]` 的 j，这样的j有很多。

举个例子，现在`dp[i-1]=20, int[i] = 15`, 那么 7，10，14 都有可能是可行解，然而并不能通过记录数组找到第一个符合条件的`j`。

这时就只能进行二分查找了，花`O(logn)`找到最近的不重叠区间，或者不存在。

转移方程为：`dp[i] = max{dp[i-1], int[i] + (dp[j] if j exists else 0)}`


#### 3. 带权区间调度

进阶版本，每个区间现在带有一个价值权重，求最大化收益。

方法和最长区间调度一样啦，只是要乘一个权重而已： `dp[i] = max{dp[i-1], int[i]*V[i] + (dp[j] if j exists else 0)}`

#### 4. 最小区间覆盖

假设有一组区间，要求求出覆盖 `[s，t]` 所需的最少的区间数目。

贪心的想法，每次根据左侧起点去切割重叠区间，更新左侧起点为重叠区间最远end位置。

假设按照区间结束位置排序：
```
              s---------------t
1         =---------=
2                 =------=
3      =--------------------=
```
则第一次切到1号区间，更新s；再切到二号线，更新s；再切到3号线，更新s，结果为3。

然而我们发现其实并不需要12号线，只用3号就可以了，这样按终止位置排序是无法得到正确答案的。

假设按照区间开始位置排序：
```
              s---------------t
1      =--------------------=
2          =----------=
3                 =------=
4                     =---------=
```

第一次切到1号线和2号线，更新s；第二次切过4号线，掠过3号线，结果正确。

```python
def minCover(intervals, s, t):
    # 假设

```






















