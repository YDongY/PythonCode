# __Time__ : 2020/10/7 下午10:19
# __Author__ : '__YDongY__'


from django.urls import path

from . import views

app_name = "app"

urlpatterns = [
    path('books/', views.BooksAPIVIew.as_view()),
    path('books/<pk>/', views.BookAPIView.as_view()),
    path('drf-books/', views.DRFBooksAPIView.as_view()),
    path('drf-books/<pk>/', views.DRFBookAPIView.as_view()),
    path('drf-heros/', views.DRFHerosAPIView.as_view()),
]
