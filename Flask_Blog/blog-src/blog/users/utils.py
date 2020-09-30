# __Time__ : 2020/9/30 下午9:37
# __Author__ : '__YDongY__'

import secrets
import os
from PIL import Image

from blog import mail
from flask_mail import Message
from flask import url_for, current_app


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # 调整图片大小，无法调整 gif 图
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()  # 获取 token 默认有效期 1800s
    msg = Message("重置密码", recipients=[user.email])
    msg.body = f"""重置密码，请访问链接：
    {url_for('reset_token', token=token, _external=True)}
    如果您没有提出此请求，只需要忽略此电子邮件，不做任何更改请求。"""  # 为 True 是为了获得绝对 URL
    mail.send(msg)
