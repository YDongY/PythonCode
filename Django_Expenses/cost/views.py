import json
import datetime
import csv
import xlwt
import tempfile

from weasyprint import HTML

from django.db.models import Sum
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse

from utils.mixin import LoginRequiredMixin

from .models import Category, Expenses
from userpreferences.models import UserPreference


@login_required
def index(request):
    categories = Category.objects.all()
    expenses = Expenses.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 4)
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


@login_required
def expense_category_summary(request):
    today_date = datetime.date.today()
    six_months_ago = today_date - datetime.timedelta(days=30 * 6)
    expenses = Expenses.objects.filter(owner=request.user, date__gt=six_months_ago, date__lt=today_date)
    resp = {}
    for exp in expenses:
        if exp.category in resp:
            resp[exp.category] += exp.amount
        else:
            resp[exp.category] = exp.amount

    return JsonResponse({"expense_category_data": resp}, safe=False)


@login_required
def stats_view(request):
    return render(request, 'cost/stats.html')


@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=Expenses' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['总计', '描述', '类型', '日期'])
    expenses = Expenses.objects.filter(owner=request.user)

    for exp in expenses:
        writer.writerow([exp.amount, exp.description, exp.category, exp.date])

    return response


@login_required
def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Expenses' + str(datetime.datetime.now()) + '.xls'

    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['总计', '描述', '类型', '日期']

    for col_num in range(len(columns)):
        # 行，列，值
        worksheet.write(row_num, col_num, columns[col_num], font_style)

    rows = Expenses.objects.filter(owner=request.user).values_list('amount', 'description', 'category', 'date')

    for row in rows:
        row_num += 1
        for col_num, col_data in enumerate(row):
            worksheet.write(row_num, col_num, str(col_data), font_style)
    workbook.save(response)

    return response


@login_required
def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline;attachment;filename=Expenses' + str(datetime.datetime.now()) + '.pdf'

    expenses = Expenses.objects.filter(owner=request.user)
    total = expenses.aggregate(Sum('amount'))

    html_string = render_to_string('cost/pdf-output.html', {"expenses": expenses, 'total': total["amount__sum"]})
    html = HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output = open(output.name, 'rb')
        response.write(output.read())

    return response
