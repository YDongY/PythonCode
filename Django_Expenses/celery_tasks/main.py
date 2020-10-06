# __Time__ : 2020/10/7 上午12:55
# __Author__ : '__YDongY__'

# 主程序
import os
import django
from celery import Celery

# 创建celery实例对象
app = Celery("expenses")

# 把celery和django进行组合，识别和加载django的配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expenses.settings')
django.setup()

# 通过app对象加载配置
app.config_from_object("celery_tasks.config")

# 加载任务
# 参数必须必须是一个列表，里面的每一个任务都是任务的路径名称
# app.autodiscover_tasks(["任务1","任务2"])
app.autodiscover_tasks(["celery_tasks.email"])

# TODO: celery -A celery_tasks.main worker --loglevel=INFO
