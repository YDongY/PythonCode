# __Time__ : 2020/10/7 上午12:56
# __Author__ : '__YDongY__'

from celery.schedules import crontab
from datetime import timedelta

broker_url = 'redis://127.0.0.1:6379/15'
result_backend = 'redis://127.0.0.1:6379/14'

imports = ('celery_tasks.email.tasks',)

timezone = 'Asia/Shanghai'
enable_utc = False
