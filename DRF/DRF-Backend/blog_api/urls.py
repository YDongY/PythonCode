# __Time__ : 2020/10/2 下午12:30
# __Author__ : '__YDongY__'

from django.urls import path

from .views import PostList, PostDetail

app_name = 'blog_api'

urlpatterns = [
    path('<int:pk>/', PostDetail.as_view(), name='detailcreate'),
    path('', PostList.as_view(), name='listcreate')
]

