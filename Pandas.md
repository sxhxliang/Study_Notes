# Pandas
## 开始：构建DataFrame  
### 1.读文件方式实例化 
```pandas.read_csv('data,\*sv',sep = '\*')```  sep为文件分隔符   
```pandas.read_excel('data.xlsx')```  

### 2.通过numpy对象实例化  
``` pandas.DataFrame(data=data,columns=[ , , ])```  


## 一、数据概览
1.观察少量DataFrame样本  
```df.head()```  

2.列名称  
```df.columns```    

3.每列数据类型  
```df.dtypes ```  

4.Simple and Dirty plot  
借助matplotlib.pyplot做出横坐标为index的粗略图线（观察数据及其有效）  

```df.plot()```  
```Series.plot()```  

## 二、DataFrame的定位与切割:  

### 1.Label Based indexing  
取行  ```row = df.loc[[2,3,4]]```  

取列  ```col = df.loc[:,[4,3,2]]```  

取子矩阵  ```subset = df.loc[['A','D','K'],['year','month','date']]```   

### 2.Positional indexing  
*仅可以使用integer/integer list进行索引  

取行  
```row = df.iloc[[1,2,3]]```  

取列  
```col = df.iloc[:,[3,2,1]]```  

取子矩阵  
```subset = df.iloc[[1,2,3],[3,2,1]]```   

### 3.全能方法 ———— ix  

自主推断参数为 index_name 还是 index_num   

```subset = df.ix[['A','B','C'],[3,2,1]]```  

## 三、Groupby组操作  

### 单column操作:  

```df.groupby('year')['lifeExp']```  

利用year列每一个unique的元素进行分组，定位到lifeExp数据  
（此时返回结果是一个groupby对象，不是实际值）   

等价表达```[df[df.year == year_i].lifeExp.mean()]```  


```Group = df.groupby('year')['lifeExp'].mean()```  

调用GroupBy对象求平均操作，返回一个Series  

### 多columns操作:  

```A = df.groupby(['year','continent'])['lifeExp'].mean()```   

此时返回一个Series，一个 Hierarchical Structure  

```>>> A.index```
```
MultiIndex(levels=[[1952, 1957, 1962, 1967, 1972, 1977, 1982, 1987, 1992, 1997, 2002, 2007, 'YEAAH'], ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania']],
           labels=[[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 12], [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 2]],
           names=['year', 'continent'])
```  

## 四、多个DataFrame Concat 与 Merge:   

### 1.Concat    

```Con_data = pd.concat([df1,df2,df3],axis=1)```   

axis = 1横向连接，axis = 0纵向连接  

pandas非常智能的是，纵向连接它将整合相同的columns，将缺失的数据记为NAN  

然而我们可以预先更改columns name使得他们变得一致  

```df1.columns = ['A','B','C','D']```  

### 2.Merge  

根据两个DataFrame的某一列进行merge，填充具备的数据  

```df1.merge(df2,left_on = 'name',right_on = 'site') ```  

df1在左，df2在右，填写对应column name  

```
	name	lat	long	ident	site	dated
0	DR-1	-49.85	-128.57	619	DR-1	1927-02-08
1	DR-1	-49.85	-128.57	622	DR-1	1927-02-10
2	DR-1	-49.85	-128.57	844	DR-1	1932-03-22
3	DR-3	-47.15	-126.72	734	DR-3	1939-01-07
4	DR-3	-47.15	-126.72	735	DR-3	1930-01-12
5	DR-3	-47.15	-126.72	751	DR-3	1930-02-26
6	DR-3	-47.15	-126.72	752	DR-3	NaN
7	MSK-4	-48.87	-123.40	837	MSK-4	1932-01-14
```  
## 数据的遍历
[https://blog.csdn.net/ls13552912394/article/details/79349809]
### 出现NaN数据怎么办？  

1.先定位  

```pd.isnull(df1.dated)```  返回一个bool数组  

2.通过ix定位并填充你希望的数据  

```df1.ix[pd.isnull(df1.dated),] = fill_data```






