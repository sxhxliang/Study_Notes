# Linux 命令笔记

## 目录
- [Screen 命令](#screen)
- [SCP 命令](#scp)
- [TMUX 操作](#tmux)
- [Conda & Cuda](#dl)
- [Shell 命令](#shell)
- [新用户配置](#newuser)
- [MISC](#misc)
  

## <span id = "screen">Screen 命令</span>
```
screen -S yourname  -> 新建一个叫yourname的session
screen -ls          -> 列出当前所有的session
screen -r yourname  -> 回到yourname这个session
ctrl + a + d        -> detach 这个session
ctrl + option + d       -> 删除这个session
``` 

## <span id = "scp">SCP 命令</span>
1. 从服务器下载文件
```
scp username@servername:/path/filename /tmp/local_destination
```
例如scp codinglog@192.168.0.101:/home/kimi/test.txt  把192.168.0.101上的/home/kimi/test.txt 的文件下载到 /tmp/local_destination

2、上传本地文件到服务器
```
scp /path/local_filename username@servername:/path  
```
例如scp /var/www/test.php  codinglog@192.168.0.101:/var/www/  把本机/var/www/目录下的test.php文件上传到192.168.0.101这台服务器上的/var/www/目录中
  
3、从服务器下载整个目录
```
scp -r username@servername:remote_dir/ /tmp/local_dir 
```
例如:scp -r codinglog@192.168.0.101 /home/kimi/test  /tmp/local_dir

4、上传目录到服务器
```
scp  -r /tmp/local_dir username@servername:remote_dir
```

## <span id = "tmux">TMUX 命令</span>
[Cheet Sheet](https://gist.github.com/ryerh/14b7c24dfd623ef8edc7)
```
新建会话 tmux [new -s 会话名 -n 窗口名]
attach一个会话 tmux a -t SESSION-ID
开启鼠标滚动 set-window-option -g mouse on 或者 setw -g mouse on
将当前面板上下分屏：Ctrl + b,"  
将当前面板左右分屏：Ctrl + b,%  
选择当前窗口中下一个面板：Ctrl + b,o  
移动光标选择对应面板：Ctrl + b,方向键 
向前置换当前面板：Ctrl + b,{  
向后置换当前面板：Ctrl + b,}  
逆时针旋转当前窗口的面板：Ctrl + b,Alt+o    
顺时针旋转当前窗口的面板：Ctrl + b,Ctrl+o  
显示面板编号：Ctrl + b,q  
关闭当前分屏：Ctrl + b,x  
将当前面板置于新窗口, 即新建一个窗口, 其中仅包含当前面板：Ctrl + b,!  
以 1 个单元格为单位移动边缘以调整当前面板大小：Ctrl + b,Ctrl+方向键  
以 5 个单元格为单位移动边缘以调整当前面板大小：Ctrl + b,Alt+方向键  
切换默认面板布局：Ctrl + b,空格键  
最大化当前所在面板：Ctrl + b,z，tmux 1.8 新特性  
```

## <span id="newuser">新用户相关</span>
#### 修改用户密码
```
passwd
```

#### 新添加用户无法使用命令行上下键以及tab键
```
sudo vi /etc/passwd
***/bin/sh -> ***/bin/bash
```

#### 添加环境变量
```
export PATH=/home/yunxuan/MAC/anaconda3/bin:$PATH
```

## <span id = "dl">深度学习环境配置</span>
#### 查看cuda与cudnn版本
```
cat /usr/local/cuda/version.txt
cat /usr/local/cuda/include/cudnn.h | grep CUDNN_MAJOR -A 2
```
#### 查看驱动版本
```
cat /proc/driver/nvidia/version
```

#### 添加conda-forge源
```
conda config --add channels conda-forge 
```


## <span id = "shell">Shell 脚本</span>
### 文件描述符 File Descriptor
- 0 号描述符： stdin, 代表输入设备, 进程从它读入数据;
- 1 号描述符： stdout, 进程往其中写入数据;
- 2 号描述符： stderr, 进程会往其中写入错误信息;

Shell 中对文件描述符的操作由三部分组成: **(Left, Operation, Right)**:

- Left 可以是 0-9 的数字, 代表第 n 号文件描述符;
  - Left 还可以为 &, 表示同时操作 stdout 和 stderr
- Right 可以是文件名或 0-9 的数字, 当 Right 是数字时必须要加上 & 符号, 表示引用第 n 号文件描述符;
  - Right 还可以为 &-, 此时表示关闭 Left 描述符, 例如 2<&- 表示关闭 stderr;
- Operation 可以为 < 或 >;
  - 为 < 时表示以读模式复制 Right 到 Left, 此时如果没有指定 Left 的话, 则为默认值 0;
  - 当为 > 表示以写模式复制 Right 到 Left, 此时如果没有指定 Left 的话, 则为默认值 1;
- Operation 和 Left 之间不能有空格; (2>, 1>)
- 当 Right 为文件名时, Operation 和 Right 可以有空格, 否则也不能有空格; (> out.txt)

#### > 重定向 (Redirecting)
重定向语法为： [FILEDESCRIPTOR]> ， []内默认为1。

```bash
# 将cmd的输出转入stderr
>&2 cmd 
cmd >&2

# More
cmd >&n 把输出送到文件描述符n 
cmd m>&n 把输出 到文件符m的信息重定向到文件描述符n 
cmd >&- 关闭标准输出 
cmd <&n 输入来自文件描述符n 
cmd m<&n m来自文件描述各个n 
cmd <&- 关闭标准输入 
cmd <&n- 移动输入文件描述符n而非复制它。（需要解释） 
cmd >&n- 移动输出文件描述符 n而非复制它。（需要解释） 
注意： >&实际上复制了文件描述符，这使得cmd > file 2>&1与cmd 2>&1 >file的效果不一样。

# 将 stderr 重定向至文件error.txt
cat nop.txt 2> error.txt 

# 分别重定向 stderr 和 stdout 
python test.py 2> err.txt 1> out.txt
```

### IF 表达式

```bash
if [ command ];then
   符合该条件执行的语句
elif [ command ];then
   符合该条件执行的语句
else
   符合该条件执行的语句
fi
```
- bash shell会按顺序执行if语句，如果command执行后且它的返回状态是0，则会执行符合该条件执行的语句，否则后面的命令不执行，跳到下一条命令。
- 当有多个嵌套时，只有第一个返回0退出状态的命令会导致符合该条件执行的语句部分被执行,如果所有的语句的执行状态都不为0，则执行else中语句。
- 返回状态：最后一个命令的退出状态，或者当没有条件是真的话为0。

### find
查找符合条件的文件 or 目录，[详解](https://math2001.github.io/article/bashs-find-command/)

- 简化版操作 `find PATH [expression]`
```bash
# 找相同后缀文件
find . -name "*.go"
# 找目录
find . -type d -name "*local*" 
```

- 组合expression
  - 子表达式的操作符包括 `-type f/d`, `-name "REGEX"`, `-path "REGEX"` 等
  - 子表达式可以通过 `-and`, `-or`, `-not(!)` 进行组合
  - 每个子表达式只与右边结合，所以 `expr1 or expr2 and expr3` 等效于 `(expr1 or expr2) and expr3`.
  
```bash
find conf/ -type f ! -name "*_local.*"          # ! 视为 -not 的简写
find . -name "*.js" -or -name "*.css" -type f   # 省略链接符视为 -and
```

### xargs
The `xargs` command in UNIX is a command line utility for building an execution pipeline from standard input. Whilst tools like `grep` can accept standard input as a parameter, many other tools cannot. Using `xargs` allows tools like `echo` and `rm` and `mkdir` to accept standard input as arguments. [详解](https://shapeshed.com/unix-xargs/)

```
# 与 mkdir 组合
echo 'one two three' | xargs mkdir
ls
> one two three

# 与 find 组合
find ./foo -type f -name "*.txt" | xargs rm

# -t 参数显示执行的命令
echo 'one two three' | xargs -t rm
> rm one two three

# -p 参数执行命令前询问，确保安全性
echo 'one two three' | xargs -p rm
> rm one two three?...

# -I (strrepl) 任意字符代替参数
find . -name "*.py" | xargs -t -I % rm %
> rm a.py
> rm b.py
> rm c.py
```


### $ 钱号(dollar sign) 
变量替换(Variable Substitution)的代表符号。 
```bash
vrs=123
echo "vrs = $vrs" # vrs = 123 
```
$符号除引用变量、执行子命令外，还有许多晦涩但又有用的黑魔法。其经常出现在shell脚本、makefile文件中，因此非常有必要掌握。
```bash
$$       # 当前脚本的进程id
$!       # 上一个后台进程的id
$#       # 参数个数
$[0-n]   # 第0-n个参数，第0个参数即命令本身
$?：     # 上一条命令的退出码，用来判断命令是否执行成功
$_：     # 上一条命令的最后一个单词，命令行中与!$相同
$@：     # 全部参数（数组）
**$***： # 全部参数（字符串）

${array[@]:first:length}  # 截取第 [first, first + length) 个元素
${@:2:3}                  # 截取第 [2, 5) 个运行参数
```

### 井号 (comments) 
1. 井号一般是注释作用

2. 井号也常出现在一行的开头: 脚本语言的特性，说明下面的脚本是用什么解释器执行的；若不加这段话，则用默认的$SHELL执行。
```bash
bash 脚本第一行
#!/bin/bash 
#!/bin/sh

python 脚本第一行
#!/usr/bin/python3
```

### ~ 帐户的 home 目录 
算是个常见的符号，代表使用者的 home 目录
```bash
~+ 当前的工作目录，这个符号代表当前的工作目录，她和内建指令 pwd的作用是相同的。 
echo ~+/var/log 
~- 上次的工作目录，这个符号代表上次的工作目录。 
echo ~-/etc/httpd/logs 
```

### ; 分号 (Command separator) 
在 shell 中，担任\"连续指令\"功能的符号就是\"分号\"。譬如以下的例子：
```bash
cd ~/backup ; mkdir startup ; cp ~/.* startup/. 
```

### ;; 连续分号 (Terminator) 
专用在 case 的选项，担任 Terminator 的角色。
```bash
case "$fop" in
  help) echo "Usage: Command -help -version filename" ;;
  version) echo "version 0.1" ;;
esac 
```

### \`command\` 倒引号 (backticks) 
在前面的单双引号，括住的是字串，但如果该字串是一列命令列，会怎样？答案是不会执行。要处理这种情况，我们得用倒单引号来做。 
```bash
fdv=`date + %F`
echo "Today $fdv" 
```
在倒引号内的 date + %F 会被视为指令，执行的结果会带入 fdv 变数中。  


### 'string' 单引号 (single quote) 
被单引号用括住的内容，将被视为单一字串。在引号内的代表变数的$符号，没有作用，也就是说，他被视为一般符号处理，防止任何变量替换。 
```bash
heyyou=homeecho 
echo '$heyyou' # We get $heyyou 
```

### "string" 双引号 (double quote) 
被双引号用括住的内容，将被视为单一字串。它防止通配符扩展，但允许变量扩展。这点与单引数的处理方式不同。 
```bash
heyyou=homeecho 
echo "$heyyou" # We get homeecho 
```
### (()) double parentheses
进行算数运算
```bash
(( myvar = 6 + 6 )); echo $myvar  # Got 12
echo $(( myvar = 6 + 6, k = 19 )) # Got 19, 双括号表达式的值为最后一个子表达式的结果
```

### , 逗点 (comma，标点中的逗号) 
这个符号常运用在运算当中当做\"区隔\"用途。如下例 
```bash
#!/bin/bash
let "t1 = ((a = 5 + 3, b = 7 - 1, c = 15 / 3))"
echo "t1= $t1, a = $a, b = $b"  
# Got: t1=5, a=6, b=5
```

### / 斜线 (forward slash) 
在路径表示时，代表目录。 

cd /etc/rc.dcd ../..cd / 

通常单一的 / 代表 root 根目录的意思；在四则运算中，代表除法的符号。 
```bash
let "num1 = ((a = 10 / 2, b = 25 / 5))" 
```

### | 管道 (pipeline) 
pipeline 是 UNIX 系统，基础且重要的观念。连结上个指令的标准输出，做为下个指令的标准输入。 
```bash
who | wc -l 
```
善用这个观念，对精简 script 有相当的帮助。 


### ! 惊叹号(negate or reverse) 
- 通常它代表反逻辑的作用，譬如条件侦测中，用 != 来代表\"不等于\" 
```bash
if [ "$?" != 0 ]then
echo "Executes error"
exit 1
fi 
```
- 在规则表达式中她担任 \"反逻辑\" 的角色 
```bash
ls a[!0-9] 
```
上例，代表显示除了a0, a1 .... a9 这几个文件的其他文件。 


### * 星号 (wild card) 
相当常用的符号。在文件名扩展(Filename expansion)上，她用来代表任何字元，包含 null 字元。 

```bash
ls a*a 
# a1 access_log 
```

在运算时，它则代表 \"乘法\"。 
```bash
let "fmult=2*3" 
```
除了内建指令 let，还有一个关于运算的指令expr，星号在这里也担任\"乘法\"的角色。不过在使用上得小心，他的前面必须加上escape 字元。 


### ** 次方运算 
两个星号在运算时代表 \"次方\" 的意思。 
```bash
let "sus=2**3"
echo "sus = $sus" # sus = 8 
```

### & 后台工作 
单一个& 符号，且放在完整指令列的最后端，即表示将该指令列放入后台中工作。 
```bash
tar cvfz data.tar.gz data > /dev/null& 
```
也可用来并发 N 个任务
```bash
python master.py
python worker.py --id=1 &
python worker.py --id=2 &
python worker.py --id=3 &
python worker.py --id=4
```

## <span id = "misc">MISC</span>
#### 管道
通过管道操作，可以指定一个程序的输出为另一个程序的输入，即将一个程序的标准输出与另一个程序的标准输入相连，这种机制就称为管道。

通常，管道操作的预防格式如下：

程序1 | 程序2 | 程序3…… | 程序n


```bash
cat input.txt | python test1.py | python test2.py 
```

#### 查看文件夹内文件大小

```
ls -lht
```

#### 压缩文件
```
tar -zcvf /home/DIR.tar.gz /DIR
```

#### 批量删除空文件/按正则文法删除某些文件夹
```
find . -name "*" -type f -size 0c | xargs -n 1 rm -f
ls | grep -P "^A.*[0-9]{2}$" | xargs -d"\n" rm
```
