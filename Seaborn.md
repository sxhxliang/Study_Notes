# Seaborn  

Seaborn 所有作图基于pandas.DataFrame,其dtypes对作图机制产生了很大的影响  

内置数据集请参阅 https://github.com/mwaskom/seaborn-data  

```python  
data = sns.load_dataset('dataset_name')
```

## 1.Bar Plot  

假如我们通过numpy矩阵生成了一个DataFrame，却并没有指定其dtype  

```python 
df = pandas.DataFrame(data = data,columns=['value','name'])
```   

此时所有column的dtypes = object  

### 绘制一张横向直方图  

```python   
sns.barplot(data = df,x = 'value',y = 'name')
```

报错了！

``` TypeError: unsupported operand type(s) for /: 'str' and 'int' ```  

因为作图至少需要一个数字类型的column，而现在的object类型无法被比较大小  

```python
df['value'] = df['value'].astype('float64')  
df.sort_values('value',ascending = False) 
```

再次调用barplot画出如下图像  

![](figures/barplot1.png)

### 其他attributes  

```python
sns.barplot(x='value',y='name',order=[ , , ],pallete = 'spring',estimator = median, hue='sex')
```

1.order 决定作图横坐标展示顺序  

![](figures/order.png)  

2.estimator 根据何种量度确定直方图数值(如：中位数，平均数)  

![](figures/estimator.png)  

3.hue 对比模式，若hue对应column中有k种元素，则分k列为一组表示  

![](figures/hue.png)  

4.color + saturation 调整纯色饱和度  

5.capsize 表示置信区间的I字形横杠的宽度
