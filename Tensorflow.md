## Tensorboard
```python
with tf.Session() as sess:
    writer = tf.summary.FileWriter(path, sess.graph)
    ...
writer.close()
```
命令行输入：
```shell
tensorboard --logdir = path
```
打开浏览器localhost:6006端口即可

## 分布  
### 平均分布
```python
    tf.random_uniform(shape, minval=0, maxval=None, dtype) 
```
- shape为1d数组或list
- 生成[minval, maxval)的平均分布 

### 截断正态分布
```python
tf.truncated_normal(shape, mean=0.0, stddev=1.0, dtype=tf.float32)
```
- 去掉距离均值大于2倍标准差的值

## Embedding
>一个embedding是从离散对象（discrete objects, 比如：单词）到实数向量的一个映射。 
```python 
blue:  (0.01359, 0.00075997, 0.24608, ..., -0.2524, 1.0048, 0.06259)
blues:  (0.01396, 0.11887, -0.48963, ..., 0.033483, -0.10007, 0.1158)
orange:  (-0.24776, -0.12359, 0.20986, ..., 0.079717, 0.23865, -0.014213)
oranges:  (-0.35609, 0.21854, 0.080944, ..., -0.35413, 0.38511, -0.070976)
```
### tf.nn.embedding_lookup
```python
tf.nn.embedding_lookup(params, ids, partition_strategy='mod', name=None, validate_indices=True, max_norm=None)
```
- params: 完整的Embedding Tensor
- ids: 你需要查看的Embedding vector序号
- Return: A Tensor with the same type as the tensors in params.  

