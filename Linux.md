## screen
```
screen -S yourname  -> 新建一个叫yourname的session
screen -ls          -> 列出当前所有的session
screen -r yourname  -> 回到yourname这个session
ctrl + a + d        -> detach 这个session
ctrl + option + d       -> 删除这个session
``` 
## 查看文件夹内文件大小

```
ls -lht
```

## 压缩文件
```
tar -zcvf /home/DIR.tar.gz /DIR
```

## 批量删除空文件/按正则文法删除某些文件夹
```
find . -name "*" -type f -size 0c | xargs -n 1 rm -f
ls | grep -P "^A.*[0-9]{2}$" | xargs -d"\n" rm
```
## SCP
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

## TMUX
[Cheet Sheet](https://gist.github.com/ryerh/14b7c24dfd623ef8edc7)
```
新建会话 tmux [new -s 会话名 -n 窗口名]
attach一个会话 tmux a -t SESSION-ID
开启鼠标滚动 set-window-option -g mouse on
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

## 修改用户密码
```
passwd
```

## 添加环境变量
```
export PATH=/home/yunxuan/MAC/anaconda3/bin:$PATH
```

## 查看cuda与cudnn版本
```
cat /usr/local/cuda/version.txt
cat /usr/local/cuda/include/cudnn.h | grep CUDNN_MAJOR -A 2
```

## 添加conda-forge源
```
conda config --add channels conda-forge 
```
