import json
from threading import Thread

from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, reverse, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired

from validate_email import validate_email

from celery_tasks.email.tasks import send_register_active_email, send_rest_password_email


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({"username_error": "用户名只包含字母和数字"}, status=400)
        user = User.objects.filter(username=username)
        if user:
            return JsonResponse({"username_error": "用户名已存在"}, status=409)
        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email=email):
            return JsonResponse({"email_error": "邮箱格式错误"}, status=400)
        user = User.objects.filter(email=email)
        if user:
            return JsonResponse({"email_error": "邮箱已存在"}, status=409)
        return JsonResponse({'email_valid': True})


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'auth/register.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.filter(Q(username=username) | Q(email=email))

        if user:
            return render(request, 'auth/register.html')

        if len(password) < 6:
            messages.error(request, "密码长度太短")
            return render(request, 'auth/register.html')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()

        # 激活链接中需要包含用户的身份信息,并且把信息加密

        # 加密用户身份信息，生成激活的token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'uid': user.id}
        token = serializer.dumps(info)  # bytes
        token = token.decode('utf8')  # 默认utf8

        domain = get_current_site(request).domain

        # 发送激活邮件，包含激活链接：http://127.0.0.1:8000/auth/active
        active_url = f"http://{domain}" + reverse("auth:active", kwargs={
            "token": token})

        send_register_active_email.delay(email, username, active_url)

        # domain = get_current_site(request).domain
        #
        # # 发送激活邮件，包含激活链接：http://127.0.0.1:8000/auth/active
        #
        # active_url = f"http://{domain}" + reverse("auth:active", kwargs={
        #     "token": token})
        # subject = '资产明细后台'
        # message = ''
        # sender = settings.EMAIL_FROM
        # receiver = [email]
        # html_message = f"""
        # <h1>{username},欢迎您注册资产明细后台</h1>点击以下链接激活您的账户<br/><a href="{active_url}">{active_url}</a>
        # """
        # send_mail(subject, message, sender, receiver, html_message=html_message)

        messages.success(request, '注册成功，请前去邮箱进行激活')
        return render(request, 'auth/register.html')


class ActiveView(View):
    """
    用户激活
    """

    def get(self, request, token):
        # 进行解密，获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取待激活用户id
            user_id = info['uid']
            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            # 跳转登录页面
            return redirect(reverse('auth:login'))
        except SignatureExpired as e:
            # 激活链接过期
            return HttpResponse('激活链接已过期')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'auth/login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not all([username, password]):
            messages.error(request, "信息不完整")
            return render(request, 'auth/login.html')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)

                # 获取登录后所要跳转的地址,request.GET.get()就是获取url参数。
                # 默认跳转到next_url
                next_url = request.GET.get('next', reverse('cost:index'))

                # 跳转到首页,返回应答
                messages.success(request, f"欢迎，{user.username}登录成功")
                return redirect(next_url)
            else:
                messages.info(request, "账号未激活")
                return render(request, 'auth/login.html')
        else:
            messages.error(request, "用户名或密码错误")
            return render(request, 'auth/login.html')


class LogoutView(View):
    def post(self, request):
        # 清除用户session信息
        logout(request)
        messages.success(request, "退出成功")
        # 跳转到首页
        return redirect(reverse('auth:login'))


class ResetPassword(View):
    def get(self, request):
        return render(request, "auth/reset-password.html")

    def post(self, request):
        email = request.POST.get("email")

        context = {
            'values': request.POST
        }

        if not validate_email(email):
            messages.error(request, "邮箱格式错误")
            return render(request, 'auth/reset-password.html', context)

        user = User.objects.filter(email=email).first()

        if not user:
            messages.error(request, "邮箱不存在")
            return render(request, 'auth/reset-password.html', context)

        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'uid': user.id}
        token = serializer.dumps(info)  # bytes
        token = token.decode('utf8')  # 默认utf8

        domain = get_current_site(request).domain

        # 发送激活邮件，包含激活链接：http://127.0.0.1:8000/auth/active

        active_url = f"http://{domain}" + reverse("auth:set-newpassword", kwargs={
            "token": token})

        send_rest_password_email.delay(email, user.email, active_url)
        messages.success(request, '重置邮件已发送')
        return redirect(reverse('auth:login'))


class SetNewPassword(View):
    def get(self, request, token):
        context = {
            "token": token
        }
        # 进行解密，获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取待激活用户id
            user_id = info['uid']
            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            if not user:
                messages.error(request, '重置连接失效')
                return render(request, 'auth/reset-password.html', context)
            return render(request, 'auth/set-newpassword.html', context)
        except SignatureExpired as e:
            messages.error(request, '重置连接失效')
            return render(request, 'auth/reset-password.html', context)

    def post(self, request, token):
        context = {
            "token": token
        }
        # 进行解密，获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取待激活用户id
            user_id = info['uid']
            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            if not user:
                messages.error(request, '重置连接失效')
                return render(request, 'auth/reset-password.html', context)
        except SignatureExpired as e:
            messages.error(request, '重置连接失效')
            return render(request, 'auth/set-newpassword.html', context)

        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, '两次密码不一致')
            return render(request, 'auth/set-newpassword.html', context)

        if len(password1) < 6:
            messages.error(request, "密码长度太短")
            return render(request, 'auth/set-newpassword.html', context)

        user.set_password(password1)
        user.save()
        messages.success(request, "重置密码成功")
        return render(request, 'auth/login.html')
