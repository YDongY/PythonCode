# __Time__ : 2020/10/8 下午5:14
# __Author__ : '__YDongY__'

import time
from django.conf import settings

from jose import jwt


def my_obtain_jwt_token(username, expire_time=10):
    """通过用户名生成 payload"""
    # 手动生成 token
    secret = settings.SECRET_KEY
    expire_time = int(time.time() + expire_time)  # 过期时间

    payload = {
        "username": username,
        'exp': expire_time
    }

    token = jwt.encode(payload, secret, algorithm='HS256')

    return token
