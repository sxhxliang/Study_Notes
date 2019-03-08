# codalab机制介绍
codalab存在的目的是解决机器学习模型performance 难以复现的问题，通过在container里面构建整个framework的可运行流程图以公平地展示模型表现。  
- codalab的file bundle是只读的， run bundle引入的文件夹也是只读的，只有run bundle的最外层目录是可写的。
- codalab线上运行可允许申请的最大gpu数=1， 最大memory=14g， 最大cpu数=6
- 

# 登陆
```
cl work
```

# 上传bundle
```
cl upload YOUR_FILES -n BUNDLE_NAME
```

# 创建run bundle
```
cl run --request-docker-image yunxuanxiao/hotpot-test:v1-
       --request-cpus 5
       --request-gpus 1
       --request-memory 50g
       models:bert_models run_settings:run_settings input.json:0xbdd8f3 :run.sh  # dependencies
       'YOUR CMD' -n 'BUNDLE_NAME'
```

# 合并bundle
```
cl make DEPENDENCY NAME
```
