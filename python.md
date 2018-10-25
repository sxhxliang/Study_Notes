## 命令行参数
usage: python [option] ... [-c cmd | -m mod | file | -] [arg] ...
Options and arguments (and corresponding environment variables):  
   
-B     : don't write .pyc files on import

**-c cmd** : program passed in as string (terminates option list)  
```python 
  python -c "print((2 + 3)/5)" 
```

**-h**     : print this help message and exit (also --help) 
```python
python3 -m http.server -h
```

**-m mod** : run library module as a script (terminates option list)  

arg ...: arguments passed to program in sys.argv[1:]  

查阅全部命令行参数请输入
```python
python --help
```

## package 结构
假设我们有如下package， 每个py 脚本中都仅有 print(__name__) 语句  [其中__init__.py 脚本在import此级目录时会被自动执行]
```python
a
├── b
|   |—— d.py
│   ├── c.py
│   └── __init__.py
└── __init__.py
```
1. 运行 import a.b.c 之后的输出为

```
a
a.b
a.b.c
```
2. 单独执行 python c.py 则得到输出
```
__main__
```

所以__name__是反映包的结构的内置变量，而当前运行的module会被指定为__main__。

## module 和 package
在python中，每个文件、文件夹都是一个module，package是一个特殊的module。  
而package则是一个拥有__init__.py的文件夹。所以
```python
import b
```
会执行b文件夹下的__init__.py, 然而并不会载入模块c，若要载入模块c需要：import b.c。

### 当前命令路径$(PSD)与import的相对性没有任何关系。
在b文件夹下运行 python c.py
```python
# c.py
from . import d
```
程序报错：没有指定father package，因为我当前module的最高等级就是c。此时应该在a文件夹下执行 
```
python -m b.c
```

## 指定程序入口
python的import机制其实是将module copy到当前脚本的头部，所以无论如何脚本的最顶层代码（0缩进）都会被运行。为了区分作为模块导入 or 作为脚本运行，我们使用如下语句：
```python
if __name__ == "__main__":
    blablabla....
```
此时被导入模块的顶层代码不会被执行。

## 星号与双星号
首先区分keyword arguments和positional arguments

- keyword arguments  
  fooA(1,2,3,4,5)
- positional arguments  
  fooB(a=1,b=2,c=3,d=4)

星号 \*arg 将本位置往后的所有参数合并为一个tuple
双星号 \*\*kwargs 将所有本位置以后的键值对作为dict传入函数
**注意：由于\*arg ,\*\*kwargs 向后包含，所以定义函数时应写成def func(\*args, \*\*kwargs)**

```python
>> func([1,2,3], {"a":"1"}, 4, pos=123, length=1234))

def func(**kwargs, *args):
   print(len(args))     # 3 
   print(args)          # ([1, 2, 3], {'a': '1'}, 4)
   print(kwargs)        # {'pos': 123, 'length': 1234}
   return
```

## Assert 断言
用于debug 抛出异常，布尔表达式后面加报错信息
```python
assert len(lists) >=5,'列表元素个数小于5'
assert 2==1,'2不等于1'
```
