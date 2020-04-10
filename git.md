### Command line instructions
```
Git global setup
git config --global user.name "肖云轩"
git config --global user.email "xiaoyunxuan@bytedance.com"
```
### Create a new repository
```
git clone git@code.byted.org:xiaoyunxuan/entityalignment.git
cd entityalignment
touch README.md
git add README.md
git commit -m "add README"
git push -u origin master
```

### Existing folder
```
cd existing_folder
git init
git remote add origin git@code.byted.org:xiaoyunxuan/entityalignment.git
git add .
git commit -m "Initial commit"
git push -u origin master
```

### Existing Git repository
```
cd existing_repo
git remote rename origin old-origin
git remote add origin git@code.byted.org:xiaoyunxuan/entityalignment.git
git push -u origin --all
git push -u origin --tags
```

## 基础教程

[动态教程](https://learngitbranching.js.org/?locale=zh_CN)

### Git Branch
```
git branch <name> # 开一个新分支
git checkout <name> # 切换到新分支, <name> 可以是 tag 也可以是SHA
```

### Git Merge
在 Git 中合并两个分支时会产生一个特殊的提交记录，它有两个父节点。翻译成自然语言相当于：“我要把这两个父节点本身及它们所有的祖先都包含进来。”
```
git merge fixBug
```

### Git Rebase
第二种合并分支的方法是 git rebase。Rebase 实际上就是取出一系列的提交记录，“复制”它们，然后在另外一个地方逐个的放下去。

Rebase 的优势就是可以创造更线性的提交历史，这听上去有些难以理解。如果只允许使用 Rebase 的话，代码库的提交历史将会变得异常清晰。

![](figure/git2.png)


### HEAD
HEAD 指向你正在其基础上进行工作的提交记录。

HEAD 总是指向当前分支上最近一次提交记录。大多数修改提交树的 Git 命令都是从改变 HEAD 的指向开始的。

```
cat .git/HEAD # 查看HEAD
git checkout bugFix # 将HEAD指向bugFix
git chechout HEAD^  # 上溯到HEAD一级父亲
git checkout HEAD~3 # 上溯到HEAD三级父亲
```

### 撤销变更
#### Git Reset 
- `git reset` 通过把分支记录回退几个提交记录来实现撤销改动。你可以将这想象成“改写历史”。
- `git reset` 向上移动分支，原来指向的提交记录就跟从来没有提交过一样。

```
git reset HEAD^ # 本地回退一个版本，当前分支指针前推
```

虽然在本地分支中使用 git reset 很方便，但是这种“改写历史”的方法对远程分支是无效的哦，因为如果照此做所有人必须全部回退到相同分支。

#### Git Revert
```
git revert HEAD
# C1->C2  变为 C1->C2->C2'
```
如果说 Reset 是减，Revert就是加，`git revert` 在我们要撤销的提交记录后面多了一个新提交！这是因为新提交记录 C2' 引入了更改 —— 这些更改刚好是用来撤销 C2 这个提交的。也就是说 C2' 的状态与 C1 是相同的。

revert 之后就可以把你的更改推送到远程仓库与别人分享啦。

