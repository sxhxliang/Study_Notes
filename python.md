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

def func(*args, **kwargs):
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

## 类与继承
pytorch代码写作过程中遇到，子类的书写规范
```python
class LayerNorm(nn.Module):
    def __init__(self, n_state, e=1e-5):
        super(LayerNorm, self).__init__() #首先找到 LayerNorm 的父类（就是类 nn.Module），然后把类LayerNorm的对象 self 转换为类 nn.Module 的对象
        self.g = nn.Parameter(torch.ones(n_state))
        self.b = nn.Parameter(torch.zeros(n_state))
        self.e = e

    def forward(self, x):
        super(LayerNorm, self).somefunction() # 子类对象调用父类方法
        u = x.mean(-1, keepdim=True)
        s = (x - u).pow(2).mean(-1, keepdim=True)
        x = (x - u) / torch.sqrt(s + self.e)
        return self.g * x + self.b
```

## bug of pip
修改pip/__main__.py文件
```python 
from __future__ import absolute_import

import os
import sys

# If we are running from a wheel, add the wheel to sys.path
# This allows the usage python pip-*.whl/pip install pip-*.whl
if __package__ == '':
    # __file__ is pip-*.whl/pip/__main__.py
    # first dirname call strips of '/__main__.py', second strips off '/pip'
    # Resulting path is the name of the wheel itself
    # Add that to sys.path so we can import pip
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)

from pip._internal import main as _main  # isort:skip # noqa

if __name__ == '__main__':
    sys.exit(_main())
```

更新一下：改成下面的更简洁也OK

```python
import sys
from pip import __main__
if __name__ == '__main__':
    sys.exit(__main__._main())
```

## 字符编码
1. ASCII：
   - 计算机是美国人发明的，所以最早只考虑了简单的26个字母 + 一些控制字符，所以只用7个bit组合出2^7=128个组合，编号0-127。
   - 存储的时候凑整成1byte。
2. GB2312：
   - 但是这个组合根本没有考虑其他国家，比如汉字明显不止128个，于是中国为了对汉字编码发明了GB2312编码；
   - 其他国家也为自己国家的文字发明了各种编码。这些工作并行，互相不兼容。
   - 举例：“中文”：`\xd6\xd0\xce\xc4`
3. UNICODE：
   - 为了统一，提出了unicode编码，包含了各个国家的文字，对每个字符都用2个bytes来表示。
   - 具体规则：对于英文字符（其实是ascii127可以表示的字符），就是在ascii编码的字节左边再加一个0000 0000；对于汉字，1个汉字用2个byte表示。
   - 举例：“中”：`\u4e2d` 
4. UTF-8:
   - 但如果要编码的全是英文字符，那么用unicode其实就浪费了，本来用ascii 1个字节可以搞定，现在变成了2个，而且全是无意义的0。
   - 为了解决这个问题，发明了**不定长的编码** utf-8，1个字符可能会被编码成1-6个字节。
   - 具体来说，在utf-8里面，英文字符还是1个字节，汉字变成了3个字节，只有生僻的才会在4个字节以上。
   - 举例：“中”：`\xe4\xb8\xad` (\x 表示16进制，1Byte = 两个16进制数，这里是三个Byte)
   
![](https://pic3.zhimg.com/80/v2-6d2207cb5cf9d64d96db3e778e639aea_1440w.jpg)

```python
# '\u4e2d'是unicode表示的字符，unicode只是表示它的一个形式，
# 本质上被表示的对象还是字符，是 str 而不是 bytes
>>> '\u4e2d'
'中文'

>>> '中文'.encode('utf-8')
b'\xe4\xb8\xad\xe6\x96\x87'

>>> '中文'.encode('gb2312')
b'\xd6\xd0\xce\xc4'

>>> '\u4e2d\u6587'.encode('utf-8')
b'\xe4\xb8\xad\xe6\x96\x87'

# 爬虫拿到的是0101的bytes，首先会制定一个编码做decode，这时候可能会碰到部分不符合出错，加上ignore试试
>>> b'\xe4\xb8\xad\xff'.decode('utf-8', errors='ignore')  #  忽略了\xff
'中'
```

总结：
1. 看到 `\u` 是 unicode 编码，看到 `\x` 可能是 utf-8 或者 gb2312
1. python3 内部使用unicode编码
