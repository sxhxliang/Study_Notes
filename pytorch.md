## 保存和加载整个模型  
```python
torch.save(model_object, 'model.pth')  
model = torch.load('model.pth')  
```

## 仅保存和加载模型参数  
```python
torch.save(model_object.state_dict(), 'params.pth')  
model_object.load_state_dict(torch.load('params.pth'))
```
