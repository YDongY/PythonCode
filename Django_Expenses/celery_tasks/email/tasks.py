# __Time__ : 2020/10/6 下午3:23
# __Author__ : '__YDongY__'


from django.core.mail import send_mail
from django.conf import settings

from celery_tasks.main import app


@app.task
def send_register_active_email(to_email, username, active_url):
    """
    发送激活邮件
    :param to_email:
    :param username:
    :param token:
    :return:
    """
    subject = '资产明细后台'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = f"""
    <h1>{username},欢迎您注册资产明细后台</h1>点击以下链接激活您的账户<br/><a href="{active_url}">{active_url}</a>
    """
    send_mail(subject, message, sender, receiver, html_message=html_message)


@app.task
def send_rest_password_email(to_email, email, active_url):
    subject = '资产明细后台'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = f"""
                        <h1>{email},资产明细后台-重置密码</h1>点击以下链接重置您的账户<br/><a href="{active_url}">{active_url}</a>
                        """
    send_mail(subject, message, sender, receiver, html_message=html_message)
