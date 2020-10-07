# Django-Expense

------

## 说明

该项目的原作者为 [CryceTruly](https://github.com/CryceTruly)，非常感谢作者提供的教程。

原代码地址：https://github.com/CryceTruly/trulyexpensesyoutube

作者 YouTube 频道：https://www.youtube.com/channel/UCQM4dR3UREnGIHz93zRw_0Q

项目是用 Django 构建了一个支出/收入跟踪网站，原本作者给的示例还是挺好看的，实际做出来的效果比较简陋🤣。整个项目非常的基础，适合新手快速熟悉 Django 搭建网站（如果对页面效果没有要求的话）。

## 预览截图


## 技术实现

- 基于 Python 3.7 + Django 框架实现
- 数据存储： SQLite
- 其他工具： Celery
- 部署：

## 功能模块

- 认证模块
    - 登录
    - 注册
    - 找回密码
- 支出模块
    - 添加支出明细
    - 编辑支出明细
    - 删除支出明细
    - 搜索
    - 支出明细导出(PDF/CSV/EXCEL)
- 收入模块
    - 添加收入明细
    - 编辑收入明细
    - 删除收入明细
    - 搜索

## 运行

- 安装依赖

```shell script
pip install -r requirements.txt -i https://pypi.doubanio.com/simple

或者

pipenv install
```

- 修改配置文件

```config
# 邮件
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
# 发送邮件的邮箱
EMAIL_HOST_USER = '😄'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = '😄'
# 收件人看到的发件人
EMAIL_FROM = '😄'
```

- 项目启动

```shell script
python manage.py runserver 
```

- Celery启动

```shell script
celery -A celery_tasks.main worker --loglevel=INFO
```
