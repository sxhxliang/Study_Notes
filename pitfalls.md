## 梯度消失
- 使用Verifier模型训练hotpot sentence selection时，模型梯度消失
  - 具体情况为:
    - 在前10个steps上，gradient由正常逐渐减小到0
    - 调整batch size, lr, dropout无效（理论上也确实无效 gradient与之无关）
  - 解决方法：
    - 发现训练数据正负例比例为1：3，不均衡，模型很快收敛到局部最优
    - 通过调整loss的权重，CrossEntropyLoss(weight=torch.Tensor([1, 3]).cuda()) 梯度恢复

## .detach 与 .data的区别
首先明确一点，detach和data都是引用传递，也就是说修改了它们原来节点的数据同步会改变。(p.s. 拷贝的话需要用.clone())
```python
>>> a = torch.tensor([1,2,3.], requires_grad = True)
>>> out = a.sigmoid()
>>> c = out.detach()
>>> c.zero_()  
tensor([ 0.,  0.,  0.])

>>> out  # modified by c.zero_() !!
tensor([ 0.,  0.,  0.])

>>> out.sum().backward()  # Requires the original value of out, but that was overwritten by c.zero_()
RuntimeError: one of the variables needed for gradient computation has been modified by an inplace operation
```
将该Variable从计算图中隔离，若梯度回传经过它则报错，所以更安全

```python
>>> a = torch.tensor([1,2,3.], requires_grad = True)
>>> out = a.sigmoid()
>>> c = out.data
>>> c.zero_()
tensor([ 0.,  0.,  0.])

>>> out  # out  was modified by c.zero_()
tensor([ 0.,  0.,  0.])

>>> out.sum().backward()
>>> a.grad  # The result is very, very wrong because `out` changed!
tensor([ 0.,  0.,  0.])
```
.data不会监督发生的改变，会造成错误的梯度回传


