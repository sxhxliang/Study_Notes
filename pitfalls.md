## 梯度消失
- 使用Verifier模型训练hotpot sentence selection时，模型梯度消失
  - 具体情况为:
    - 在前10个steps上，gradient由正常逐渐减小到0
    - 调整batch size, lr, dropout无效（理论上也确实无效 gradient与之无关）
  - 解决方法：
    - 发现训练数据正负例比例为1：3，不均衡，模型很快收敛到局部最优
    - 通过调整loss的权重，CrossEntropyLoss(weight=torch.Tensor([1, 3]).cuda()) 梯度恢复
