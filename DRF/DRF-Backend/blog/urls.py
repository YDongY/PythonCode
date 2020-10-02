# __Time__ : 2020/10/2 下午12:30
# __Author__ : '__YDongY__'

from django.urls import path

from django.views.generic import TemplateView

app_name = 'blog'

urlpatterns = [
    path('', TemplateView.as_view(template_name='blog/index.html'))
]
