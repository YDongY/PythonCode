# __Time__ : 2020/10/7 上午12:56
# __Author__ : '__YDongY__'

from celery.schedules import crontab
from datetime import timedelta
from django.conf import settings

broker_url = settings.CELERY_BROKER
result_backend = settings.CELERY_BACKEND

imports = ('celery_tasks.email.tasks',)

timezone = 'Asia/Shanghai'
enable_utc = False
