# gerrit_query
> query the changes of specific condition in gerrit server

> 使用封装好的gerrit query接口对gerrit服务器进行查询，可以查询特定分支，仓库，owner，时间等条件

## 使用方法:  
> Ubuntu16.04 为例
### 1、可以打开example.py作为参考

### 2、导入模块
    from gerrit_query import GerritQuery

### 3、输入参数
#### &emsp;     i.必要参数(3个)
    url: gerrit服务器的url
    username, password: 登录服务器所需的账号和密码
#### &emsp;     ii.可选参数
    status: 所查询change状态
    owner: change所属owner
    branch: 查询的分支
    project: 查询的仓库名称
    mergedafter, mergerbefore: 以合入时间为条件进行查询 eg:2022-10-1
**注: 严格按照时间格式 `2022-10-1`**
    

## 更新日志

### 1.0
&emsp;更新为初始脚本
