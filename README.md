# pingAdmin
 pingAdmin是一款结合saltAPI的自动化运维平台，集成了用户中心、资产管理、作业调度和任务编排功能。 
 
 目前功能比较简单，之后会慢慢扩展和完善。 

## 开发环境
 [![](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/)
 [![](https://img.shields.io/badge/django-2.1-brightgreen.svg)](https://www.djangoproject.com/)
 [![](https://img.shields.io/badge/redis-3.2-red.svg)](https://redis.io/)
 [![](https://img.shields.io/badge/bootstrap-3.3-cdbfe3.svg)](https://getbootstrap.com)
 
## 功能说明
 ![image](https://github.com/Xpitz/pingAdmin/blob/master/docs/img/功能说明.png)
 
## 项目部署
### 环境准备
 | 项目 | 版本 | 说明 |
 | :------: | :------: | :------: |
 | Python | 3.6 | 后端开发语言 |
 | Redis | 3.2 | 异步任务存储 |
 | SaltAPI | 2015.5.10 | 批量执行工具 |
 
 以上项目请自行安装。
 
### 安装模块
 `pip install requirements.txt`
 
### 生成数据
 ```
 python manage.py makemigrations 
 python manage.py migrate
 ```
 
 目前数据库配置为sqlite，需要使用mysql可自行修改settings.py。
 
### 创建用户
 `python manage.py createsuperuser`

 依次输入用户名、昵称、邮箱和密码创建超级用户账号。
 
### 修改配置
 ```
 # vim pingAdmin/apps/utils/config.ini
 
 [salt]
 url = <salt_url>
 user = <salt_user>
 password = <salt_password>

 [para]
 hostname = <para_hostname>
 port = <para_port>
 user = <para_user>
 password = <para_password>

 [file]
 src = <file_src>
 dst = <file_dst>
 ```
 
 * `[salt]`配置saltAPI相关信息。
 * `[para]`调用paramiko模块，实现脚本和sls文件上传、同步。
 * `[file]`指定脚本和sls文件生成和上传的路径，末尾以`/`或`\`结尾。
 
### 启动项目
 `python manage.py runserver 0.0.0.0:8000`
 
 项目启动后，浏览器中输入`<ip>:<8000>/login/` 即可登录访问。
 
### 启动Celery
 `celery -A pingAdmin worker -B -c 2 -l info`
 
 确保redis已正常启动且setttings.py中djcelery配置无误。
 
## 控制面板
 ![image](https://github.com/Xpitz/pingAdmin/blob/master/docs/img/控制面板.png)
 
## 用户中心
### 用户列表 
 ![image](https://github.com/Xpitz/pingAdmin/blob/master/docs/img/用户列表.png)
 
### 用户角色 
 ![image](https://github.com/Xpitz/pingAdmin/blob/master/docs/img/用户角色.png)
 
 注意：
 * 权限是基于django的auth设计，相当于是移植了后台分配权限的功能。目前还不支持对象级别的控制。
 * 如果将用户设置为超级用户，用户将获得所有权限，包括调用API及访问django自带的后台。
 
## 资产管理
### 资产列表
 ![image](https://github.com/Xpitz/pingAdmin/blob/master/docs/img/资产列表.png)
 
 注意：
 * 表单上方的五个图标分别表示`创建`、`同步`、`删除`、`导入`、`导出`。
   * `创建`：填写基本信息创建新资产。
   * `同步`：通过saltAPI同步资产系统信息。
   * `删除`：批量删除资产。
   * `导入`：通过csv文件导入资产。
   * `导出`：导出相关资产信息，支持自定义列和导出范围。
 
### 资产组
 ![image](https://github.com/Xpitz/pingAdmin/blob/master/docs/img/资产组.png) 
 
 注意：
 * 资产可以不加入到资产组中，但是无资产组的资产将无法导出。
 
## 作业调度
### 执行命令
 ![image](https://github.com/Xpitz/pingAdmin/blob/master/docs/img/执行命令.png)
 
 注意：
 * `执行命令`页面允许用户远程执行命令、脚本和sls文件。
 * 目前`执行命令`的操作是同步的，对于耗时的作业可以放到任务编排中执行。
 
### 作业列表
 ![image](https://github.com/Xpitz/pingAdmin/blob/master/docs/img/作业列表.png)
 
 注意：
 * 新增作业（脚本或sls）后需要点击`上传`按钮手动上传。
 * 新增作业时请务必加上作业名的后缀，如`test.sh`、`test.py`或`test.sls`。
 
 
### 作业类型
 ![image](https://github.com/Xpitz/pingAdmin/blob/master/docs/img/作业类型.png)
 
 注意：
 * 目前仅支持`script`和`SLS`两种作业类型，因此需要手动添加，后期考虑优化。
 
## 任务编排
> 任务编排是移植了后台的djcelery，并对部分功能做了精简。完整功能可以使用超级用户访问`<ip>:<8000>/admin/`
### 周期任务
 ![image](https://github.com/Xpitz/pingAdmin/blob/master/docs/img/周期任务.png)
 
### Crontab列表
 ![image](https://github.com/Xpitz/pingAdmin/blob/master/docs/img/Crontab列表.png)
 
### Interval列表
 ![image](https://github.com/Xpitz/pingAdmin/blob/master/docs/img/Interval列表.png)

### 任务结果
 ![image](https://github.com/Xpitz/pingAdmin/blob/master/docs/img/任务结果.png)
