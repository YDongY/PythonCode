# Online News

# 前言

- 一款新闻展示的 Web 项目，主要为用户提供最新的金融资讯数据
- 以抓取其他网站数据和用户发布作为新闻的主要来源
- 基于 Flask 框架，以**前后端不分离**的形式实现具体业务逻辑

## 预览截图

![](https://github.com/YDongY/code_snippets/blob/master/Flask_News/assets/post-index.png)
![](https://github.com/YDongY/code_snippets/blob/master/Flask_News/assets/post-detail.png)
![](https://github.com/YDongY/code_snippets/blob/master/Flask_News/assets/user-register.png)
![](https://github.com/YDongY/code_snippets/blob/master/Flask_News/assets/user-base-info.png)
![](https://github.com/YDongY/code_snippets/blob/master/Flask_News/assets/new-admin.png)

## 技术实现

- 基于 Python 3.7 + Flask 框架实现
- 数据存储使用 Redis + MySQL 实现
- 第三方扩展：
  - 七牛云：文件存储平台
  - 云通信：短信验证码平台
- 布署：

## 功能模块

- 新闻模块
  - 首页新闻列表
  - 新闻详情
- 用户模块
  - 登录注册/个人信息修改
  - 新闻收藏/发布
- 后台管理

## 项目运行

- 环境搭建

```shell script
pip install -r requirements.txt -i https://pypi.doubanio.com/simple

或者

pipenv install
```

- 数据库迁移

```shell script
python manager.py db init
python manager.py db migrate
python manager.py db upgrade
```

- 创建数据库

```shell script
mysql -uroot -p
create database News;
```

- 导入数据：进入到 sql 目录，登录数据库

```sql
use News;
source infomation_info_category.sql
source infomation_info_news.sql
```

- 整库导入

```shell script
mysql -uroot -p < all.sql
```

- 编辑配置 .env

```.env
export SECRET_KEY=ydyakdkanv
export DB_NAME=News
export DB_HOST=127.0.0.1
export DB_USER=root
export DB_PASSWORD=root
export DB_PORT=3306
export REDIS_DB_HOST=127.0.0.1
export REDIS_DB_PORT=6379
export REDIS_DB_NUM=3
export ACCOUNT_SID=
export ACCOUNT_TOKEN=
export APP_ID=
export QINIU_ACCESS_KEY=
export QINIU_SECRET_KEY=
```

- 导入环境变量
```shell script
source .env
```

- 启动 Celery

```shell script
celery -A info.tasks.tasks_sms worker -l INFO
```

- 启动项目

```shell script
python manager.py runserver
```
