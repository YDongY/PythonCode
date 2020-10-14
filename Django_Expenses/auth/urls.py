# __Time__ : 2020/10/6 下午1:38
# __Author__ : '__YDongY__'

from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = "auth"

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('validate-username', csrf_exempt(views.UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email', csrf_exempt(views.EmailValidationView.as_view()), name='validate-email'),
    re_path(r'^active/(?P<token>.*)$', views.ActiveView.as_view(), name='active'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('request-rest', views.ResetPassword.as_view(), name='request-rest'),
    re_path(r'^set-newpassword/(?P<token>.*)$', views.SetNewPassword.as_view(), name='set-newpassword'),
]
