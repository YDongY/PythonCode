# __Time__ : 2020/10/6 下午10:00
# __Author__ : '__YDongY__'

from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = "user"

urlpatterns = [
    path('preferences', views.IndexView.as_view(), name='preferences'),
]
