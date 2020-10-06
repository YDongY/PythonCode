# __Time__ : 2020/10/6 上午11:54
# __Author__ : '__YDongY__'


from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = "cost"

urlpatterns = [
    path('', views.index, name="index"),
    path('add-cost', views.AddCost.as_view(), name="add-cost"),
    path('edit-cost/<int:cid>', views.EditCost.as_view(), name="edit-cost"),
    path('delete-cost/<int:cid>', views.DeleteCost.as_view(), name="delete-cost"),
    path('search-cost', csrf_exempt(views.SearchCost.as_view()), name="search-cost"),
]
