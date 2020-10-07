# coding:utf-8

from werkzeug.routing import BaseConverter
from flask import session, jsonify, g, current_app
from info.utils.response_code import RET
import functools


class ReConverter(BaseConverter):
    def __init__(self, url_map, regex):
        # 调用父类初始化方法
        super(ReConverter, self).__init__(url_map)
        # 将正则表达式保存在对象的属性中，flask会去使用这个属性来进行路由的正则匹配
        self.regex = regex


# 定义的验证登录装饰器
def login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        # 判断用户的登录状态
        user_id = session.get("user_id")
        is_admin = session.get("is_admin")
        # 查询用户的对象
        user = None
        if user_id:
            try:
                from info.models import User
                user = User.query.get(user_id)
            except Exception as e:
                current_app.logger.error(e)
        # 使用g对象保存
        g.user = user
        return view_func(*args, **kwargs)

    return wrapper
