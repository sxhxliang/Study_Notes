# 星号与双星号
首先区分keyword arguments和positional arguments

- keyword arguments  
  fooA(1,2,3,4,5)
- positional arguments  
  fooB(a=1,b=2,c=3,d=4)

```python
def one(a,*b):
    """a is normal args，*b is positional args"""
    print(b)
    
one(1,2,3,4,5,6)
#-----------------------------
def two(a=1,**b):
    """a is normal args，**b is keyword args"""
    print(b)
    
two(a=1,b=2,c=3,d=4,e=5,f=6)

# 第一个输出为 tuple：
(2, 3, 4, 5, 6)

# 第二个输出为 dict：
{'b': 2, 'c': 3, 'e': 5, 'f': 6, 'd': 4}
```
