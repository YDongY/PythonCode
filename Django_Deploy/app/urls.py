# __Time__ : 2020/10/8 下午10:37
# __Author__ : '__YDongY__'

from django.urls import path, include

from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index')
]
