# coding:utf-8

from celery import Celery
from info.utils.sms import CCP

# 定义celery对象
app = Celery("info", broker='redis://127.0.0.1:6379/3')


# TODO:启动worker：celery -A info.tasks.tasks_sms worker -l INFO

@app.task
def send_sms(to, datas, temp_id):
    """发送短信异步任务"""
    ccp = CCP()
    ccp.send_template_sms(to, datas, temp_id)
