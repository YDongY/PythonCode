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
    path('expense-category-summary', views.expense_category_summary, name="expense-category-summary"),
    path('stats', views.stats_view, name="stats"),
    path('export-csv', views.export_csv, name="export-csv"),
    path('export-excel', views.export_excel, name="export-excel"),
    path('export-pdf', views.export_pdf, name="export-pdf"),
]
