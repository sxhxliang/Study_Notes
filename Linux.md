## screen
```
screen -S yourname  -> 新建一个叫yourname的session
screen -ls          -> 列出当前所有的session
screen -r yourname  -> 回到yourname这个session
ctrl + a + d        -> detach 这个session
ctrl + option + d       -> 删除这个session
``` 

## 批量删除空文件
```
find . -name "*" -type f -size 0c | xargs -n 1 rm -f
```

## TMUX
```
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
