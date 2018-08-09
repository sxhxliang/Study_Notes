## 命令行参数
usage: python [option] ... [-c cmd | -m mod | file | -] [arg] ...
Options and arguments (and corresponding environment variables):  

-b     : issue warnings about str(bytes_instance), str(bytearray_instance)
         and comparing bytes/bytearray with str. (-bb: issue errors)  
       
-B     : don't write .pyc files on import; also PYTHONDONTWRITEBYTECODE=x  

**-c cmd** : program passed in as string (terminates option list)  
```python 
  python -c "print((2 + 3)/5)" 
```
-d     : debug output from parser; also PYTHONDEBUG=x  

-E     : ignore PYTHON* environment variables (such as PYTHONPATH)  

**-h**     : print this help message and exit (also --help) 
```python
python3 -m http.server -h
```

-i     : inspect interactively after running script; forces a prompt even
         if stdin does not appear to be a terminal; also PYTHONINSPECT=x  
         
-I     : isolate Python from the user's environment (implies -E and -s)  

**-m mod** : run library module as a script (terminates option list)  

-O     : remove assert and debug-dependent statements; add .opt-1 before
         .pyc extension; also PYTHONOPTIMIZE=x  
         
-OO    : do -O changes and also discard docstrings; add .opt-2 before
         .pyc extension  
         
-q     : don't print version and copyright messages on interactive startup  

-s     : don't add user site directory to sys.path; also PYTHONNOUSERSITE  

-S     : don't imply 'import site' on initialization  
 
-u     : force the binary I/O layers of stdout and stderr to be unbuffered;
         stdin is always buffered; text I/O layer will be line-buffered;
         also PYTHONUNBUFFERED=x
-v     : verbose (trace import statements); also PYTHONVERBOSE=x
         can be supplied multiple times to increase verbosity  
         
-V     : print the Python version number and exit (also --version)
         when given twice, print more information about the build  
         
-W arg : warning control; arg is action:message:category:module:lineno
         also PYTHONWARNINGS=arg  
         
-x     : skip first line of source, allowing use of non-Unix forms of #!cmd  

-X opt : set implementation-specific option  

file   : program read from script file  
-      : program read from stdin (default; interactive mode if a tty)  

arg ...: arguments passed to program in sys.argv[1:]  


## 星号与双星号
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
