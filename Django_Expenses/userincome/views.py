import json

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse

from utils.mixin import LoginRequiredMixin

from .models import UserIncome, Source
from userpreferences.models import UserPreference


@login_required
def index(request):
    sources = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency,
        'sources': sources
    }
    return render(request, 'income/index.html', context)


class AddIncome(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        sources = Source.objects.all()
        context = {
            "sources": sources
        }
        return render(request, 'income/add-income.html', context)

    def post(self, request, *args, **kwargs):
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        source = request.POST.get("source")
        date = request.POST.get("income_date")

        if not all([amount, description, source, date]):
            messages.error(request, "请填写完成信息")
            return render(request, 'income/add-income.html')

        UserIncome.objects.create(amount=amount, description=description,
                                  date=date, source=source, owner=request.user)

        messages.success(request, '添加成功')
        return redirect(reverse("income:income"))


class EditIncome(LoginRequiredMixin, View):
    def get(self, request, cid):
        income = UserIncome.objects.filter(id=cid).first()
        if not income:
            return render(request, '404.html')
        sources = Source.objects.all()
        context = {
            "income": income,
            "sources": sources
        }
        return render(request, 'income/edit-income.html', context)

    def post(self, request, cid):
        income = UserIncome.objects.filter(id=cid).first()
        if not income:
            return render(request, '404.html')
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        source = request.POST.get("source")
        date = request.POST.get("income_date")

        if not all([amount, description, source, date]):
            messages.error(request, "请填写完成信息")
            return render(request, 'income/edit-income.html')
        income.amount = amount
        income.description = description
        income.source = source
        income.date = date
        income.save()
        messages.success(request, '修改成功')
        return redirect(reverse("income:income"))


class DeleteIncome(LoginRequiredMixin, View):
    def get(self, request, cid):
        income = UserIncome.objects.filter(id=cid).first()
        if not income:
            return render(request, '404.html')
        income.delete()
        messages.success(request, '删除成功')
        return redirect(reverse("income:income"))


class SearchIncome(LoginRequiredMixin, View):
    def post(self, request):
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)
