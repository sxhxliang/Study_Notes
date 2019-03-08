# 把dockerhub上的image 拉到本地, 启动docker
```
docker pull aturner/python-java
docker start aturner/python-java
```

# 查看本地docker
```
docker images
```

# 进入docker
```
docker run -t -i -v /newNAS/Workspaces/.../xyx:/usr/share/xyx d98cff309821 /bin/bash
```

# 提交docker更新
- 首先要在run docker时记住本次的docker id， 如 root@8c5a8da5fa1
```
Usage: docker commit [OPTIONS] CONTAINER [REPOSITORY:TAG]
Example: docker commit -m 'MESSAGE' -a 'Author Name' 8c5a8da5fa1 yunxuanxiao/test:v2
```

# push
```
docker push yunxuanxiao/test:v2
```
