# __Time__ : 2020/10/6 下午10:52
# __Author__ : '__YDongY__'

from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = "income"

urlpatterns = [
    path('', views.index, name="income"),
    path('add-income', views.AddIncome.as_view(), name="add-income"),
    path('edit-income/<int:cid>', views.EditIncome.as_view(), name="edit-income"),
    path('delete-income/<int:cid>', views.DeleteIncome.as_view(), name="delete-income"),
    path('search-income', csrf_exempt(views.SearchIncome.as_view()), name="search-income"),
]
