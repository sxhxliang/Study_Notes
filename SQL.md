
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
