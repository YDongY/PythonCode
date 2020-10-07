# coding:utf-8

import os

# 图片验证码的redis有效期:秒
IMAGE_CODE_REDIS_EXPIRE = 180

# 短信验证码
SMS_CODE_REDIS_EXPIRE = 300

# 发送短信验证码的间隔
SEND_SMS_CODE_INTERVAL = 60

# 登录错误尝试次数
LOGIN_ERROR_MAX_TIMES = 5

# 登录错误限制事件
LOGIN_ERROR_FORBID_TIME = 600

# 新闻点击量前十
CLICK_RANK_MAX_NEWS = 10

# 用户收藏每页最多显示1条
USER_COLLECTION_MAX_NEWS = 1

# 用户关注每页最多显示一条
USER_COLLECTION_MAX_FOLLOW = 1

# 用户发布新闻列表每页最多显示一条
USER_NEWS_MAX = 1

# 管理员用户列表每页显示一条
ADMIN_USER_INFO_MAX = 1

# 管理员新闻版式每页显示10条
ADMIN_NEWS_INFO_MAX = 10

# 七牛域名
QINIU_URL_DOMAIN = "http://qhtow8dsp.hd-bkt.clouddn.com/"

# 容联云通讯
# 说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
# 说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
ACCOUNT_TOKEN = os.environ.get("ACCOUNT_TOKEN")
# 请使用管理控制台首页的APPID或自己创建应用的APPID
APP_ID = os.environ.get("APP_ID")

# 七牛云存储
# 需要填写你的 Access Key 和 Secret Key
QINIU_ACCESS_KEY = os.environ.get("QINIU_ACCESS_KEY")
QINIU_SECRET_KEY = os.environ.get("QINIU_SECRET_KEY")
