## screen
```
screen -S yourname  -> 新建一个叫yourname的session
screen -ls          -> 列出当前所有的session
screen -r yourname  -> 回到yourname这个session
ctrl + a + d        -> detach 这个session
exit()              -> 删除这个session
```

## 批量删除空文件
```
find . -name "*" -type f -size 0c | xargs -n 1 rm -f
```

## 
