# Numpy
## 随机数生成
    v1 = np.random.randn(d1,d2,d3,...)  标准正态分布
    v2 = np.random.random(tuple)        
    v3 = np.random.randint(L, R, tuple) 

# 基本运算
## 求和
    np.sum(A, axis = 1, keepdims=True) 列求和
- 0-base
- 不指定axis则求全部元素和
- Notice: keepdims = false -> 求和向量是1-d的，即可认为是row也可以是col

## 乘法

### 元素乘 
    
    A*B

### 矩阵乘 

    A.dot(B)
    np.dot(A, B)
    np.multiply(A, B)

## 除法
    if A = [a1, a2, a3], b = (b1, b2, b3)
    A/b = [a1./b1, a2./b2, a3./b3]

## 求逆
    np.linalg.inv(A)


# Functions
    np.exp(A)

    np.max(A, axis=1) 每行最大值组成的列向量