## 主键与外键

### Primary Key

对于关系表，有个很重要的约束，就是任意两条记录不能重复。不能重复不是指两条记录不完全相同，而是指能够通过某个字段唯一区分出不同的记录，这个字段被称为主键。

对主键的要求，最关键的一点是：记录一旦插入到表中，主键最好不要再修改！由于主键的作用十分重要，如何选取主键会对业务开发产生重要影响。如果我们以学生的身份证号作为主键，似乎能唯一定位记录。然而，身份证号也是一种业务场景，如果身份证号升位了，或者需要变更，作为主键，不得不修改的时候，就会对业务产生严重影响。

所以，选取主键的一个基本原则是：**不使用任何业务相关的字段作为主键**。

常见的可作为主键字段的类型有：
- 自增整数类型：数据库会在插入数据时自动为每一条记录分配一个自增整数，这样我们就完全不用担心主键重复，也不用自己预先生成主键；
- 全局唯一GUID类型：使用一种全局唯一的字符串作为主键，类似`8f55d96b-8acc-4636-8cb8-76bf8abc2f57`。GUID算法通过网卡MAC地址、时间戳和随机数保证任意计算机在任意时间生成的字符串都是不同的，大部分编程语言都内置了GUID算法，可以自己预算出主键。

### Foreign Key
当我们用主键唯一标识记录时，我们就可以在students表中确定任意一个学生的记录：

|id|	name|	other columns...|
|---|---|---|
|1|	小明|	...|
|2|	小红|	...|

我们还可以在classes表中确定任意一个班级记录：

|id|	name|	other columns...|
|---|---|---|
|1|	一班|	...|
|2|	二班|	...|

为了表达这种一对多的关系，我们需要在students表中加入一列class_id，让它的值与classes表的某条记录相对应：

|id	|class_id	|name	|other columns...|
|---|---|---|---|
|1	|1	|小明	|...|
|2	|1	|小红	|...|
|5	|2	|小白	|...|

```sql
ALTER TABLE students
ADD CONSTRAINT fk_class_id
FOREIGN KEY (class_id)
REFERENCES classes (id);
```
其中，外键约束的名称`fk_class_id`可以任意，`FOREIGN KEY (class_id)`指定了`class_id`作为外键，`REFERENCES classes (id)`指定了这个外键将关联到`classes`表的`id`列（即`classes`表的主键）。

通过定义外键约束，关系数据库可以保证无法插入无效的数据。即如果classes表不存在id=99的记录，students表就无法插入class_id=99的记录。

## OVER(PARTITION BY X ORDER BY Y) Clause
[partition by 详解](https://www.sqlshack.com/sql-partition-by-clause-overview/)

- GROUP BY 语句仅能对每个group返回一行records，无法增添更多columns
- PARTITION BY 语句对数据根据X进行分组，然后进行聚合计算，能保存所有records

```sql
SELECT Customercity, 
       AVG(Orderamount) OVER(PARTITION BY Customercity) AS AvgOrderAmount, 
       MIN(OrderAmount) OVER(PARTITION BY Customercity) AS MinOrderAmount, 
       SUM(Orderamount) OVER(PARTITION BY Customercity) AS TotalOrderAmount
FROM [dbo].[Orders];
```

![fig](https://www.sqlshack.com/wp-content/uploads/2019/04/example-of-sql-partition-by-clause.png)
