import json

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse

from utils.mixin import LoginRequiredMixin

from .models import Category, Expenses
from userpreferences.models import UserPreference


@login_required
def index(request):
    categories = Category.objects.all()
    expenses = Expenses.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page', 1)
    page_obj = Paginator.page(paginator, page_number)
    user_preference = UserPreference.objects.filter(user=request.user).first()
    context = {
        "categories": categories,
        "expenses": expenses,
        "page_obj": page_obj,
        "currency": user_preference.currency if user_preference else None
    }
    return render(request, 'cost/index.html', context)


class AddCost(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            "categories": categories
        }
        return render(request, 'cost/add-cost.html', context)

    def post(self, request, *args, **kwargs):
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        category = request.POST.get("category")
        date = request.POST.get("expense_date")

        if not all([amount, description, category, date]):
            messages.error(request, "请填写完成信息")
            return render(request, 'cost/add-cost.html')

        Expenses.objects.create(amount=amount, description=description,
                                date=date, category=category, owner=request.user)

        messages.success(request, '添加成功')
        return redirect(reverse("cost:index"))


class EditCost(LoginRequiredMixin, View):
    def get(self, request, cid):
        expense = Expenses.objects.filter(id=cid).first()
        if not expense:
            return render(request, '404.html')
        categories = Category.objects.all()
        context = {
            "expense": expense,
            "categories": categories
        }
        return render(request, 'cost/edit-cost.html', context)

    def post(self, request, cid):
        expense = Expenses.objects.filter(id=cid).first()
        if not expense:
            return render(request, '404.html')
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        category = request.POST.get("category")
        date = request.POST.get("expense_date")

        if not all([amount, description, category, date]):
            messages.error(request, "请填写完成信息")
            return render(request, 'cost/edit-cost.html')
        expense.amount = amount
        expense.description = description
        expense.category = category
        expense.date = date
        expense.save()
        messages.success(request, '修改成功')
        return redirect(reverse("cost:index"))


class DeleteCost(LoginRequiredMixin, View):
    def get(self, request, cid):
        expense = Expenses.objects.filter(id=cid).first()
        if not expense:
            return render(request, '404.html')
        expense.delete()
        messages.success(request, '删除成功')
        return redirect(reverse("cost:index"))


class SearchCost(LoginRequiredMixin, View):
    def post(self, request):
        search = json.loads(request.body).get("searchText")
        expenses = Expenses.objects.filter(
            amount__istartswith=search, owner=request.user) | Expenses.objects.filter(
            date__istartswith=search, owner=request.user) | Expenses.objects.filter(
            description__icontains=search, owner=request.user) | Expenses.objects.filter(
            category__icontains=search, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)
