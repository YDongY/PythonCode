# -*- coding: utf-8 -*-

"""
https://developer.qiniu.com/kodo/sdk/1242/python
"""
import os

from qiniu import Auth, put_data, etag
from info import constants


def storage(file_data):
    # 构建鉴权对象
    q = Auth(constants.QINIU_ACCESS_KEY, constants.QINIU_SECRET_KEY)
    # 要上传的空间
    bucket_name = 'flask-news111'

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, None, 3600)

    ret, info = put_data(token, None, file_data)

    if info.status_code == 200:
        # 上传成功
        return ret.get("key")
    else:
        raise Exception("上传失败")


if __name__ == '__main__':
    with open("./1.jpg", "rb") as f:
        file_data = f.read()
        storage(file_data)
