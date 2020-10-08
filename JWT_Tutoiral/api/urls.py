# __Time__ : 2020/10/8 下午3:35
# __Author__ : '__YDongY__'


from django.conf.urls import re_path

from . import views

from rest_framework_jwt.views import ObtainJSONWebToken, obtain_jwt_token

urlpatterns = [

    re_path(r'^login/$', views.LoginView.as_view()),
    re_path(r'^user-info/$', views.UserInfoView.as_view()),

    re_path(r'^v1/login/$', views.LoginAPIView.as_view()),
    re_path(r'^v1/user-info/$', views.UserInfoAPIView.as_view()),
]
