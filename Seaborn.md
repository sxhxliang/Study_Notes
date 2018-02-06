# Seaborn  

Seaborn 所有作图基于pandas.DataFrame,其dtypes对作图机制产生了很大的影响  

## 1.Bar Plot  

假如我们通过numpy矩阵生成了一个DataFrame，却并没有指定其dtype  

```df = pandas.DataFrame(data = data,columns=['value','name'])```   

此时所有column的dtypes = object  

绘制一张横向直方图  

```sns.barplot(data = df,x = 'value',y = 'name')```  

报错了！``` TypeError: unsupported operand type(s) for /: 'str' and 'int' ```  

因为作图至少需要一个数字类型的column，而现在的object类型无法被比较大小  

``` df['value'] = df['value'].astype('float64')```   

``` df.sort_values('value',ascending = False) ```

再次调用barplot画出如下图像  



