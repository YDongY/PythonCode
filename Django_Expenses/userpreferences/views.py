import os
import json

from django.shortcuts import render
from django.conf import settings
from django.views import View
from django.contrib import messages

from utils.mixin import LoginRequiredMixin
from .models import UserPreference


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        user_preference = UserPreference.objects.filter(user=request.user).first()
        currency_data = []
        file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

        with open(file_path, 'r') as f:
            data = json.load(f)
            for key, value in data.items():
                currency_data.append({"name": key, "value": value})
        context = {
            "currencies": currency_data,
        }
        if user_preference:
            context["user_preference"] = user_preference
        return render(request, 'preferences/index.html', context)

    def post(self, request):
        currency = request.POST.get("currency")
        user_preference = UserPreference.objects.filter(user=request.user).first()
        if user_preference:
            user_preference.currency = currency
            user_preference.save()
        else:
            UserPreference.objects.create(user=request.user, currency=currency)
        messages.success(request, "保存成功")

        currency_data = []
        file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
        with open(file_path, 'r') as f:
            data = json.load(f)
            for key, value in data.items():
                currency_data.append({"name": key, "value": value})
        context = {
            "currencies": currency_data,
            "user_preference": user_preference
        }
        return render(request, 'preferences/index.html', context)
