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
