import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import status

from django.conf import settings
from django.contrib.auth import authenticate

from jose import jwt, exceptions

from . import serializers
from .models import UserInfo
from .utils import my_obtain_jwt_token
from .authentications import MyJSONWebTokenAuthentication


# {
#     "username": "root",
#     "password": "root"
# }


class LoginView(APIView):
    """原生签名 jwt token 登录"""

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "用户名或密码错误"}, status=status.HTTP_400_BAD_REQUEST)

        # 手动生成 token
        secret = settings.SECRET_KEY
        expire_time = int(time.time() + 200)  # 过期时间

        token = jwt.encode({'uid': user.id, 'exp': expire_time}, secret, algorithm='HS256')

        return Response({"token": token}, status=status.HTTP_200_OK)


class UserInfoView(APIView):
    """原生 jwt token 校验"""

    def get(self, request):
        """
            Return request's 'Authorization:' header, as a bytestring.

            Hide some test client ickyness where the header can be unicode.
        """
        token = request.META.get('HTTP_AUTHORIZATION', b'')

        if not token:
            return Response({"error": "认证失败"}, status=status.HTTP_401_UNAUTHORIZED)
        secret = settings.SECRET_KEY

        try:
            info = jwt.decode(token, secret, algorithms=['HS256'])
        except exceptions.JWTError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            uid = info['uid']
            user = UserInfo.objects.filter(id=uid).first()
            if not user:
                return Response({"error": "认证失败"}, status=status.HTTP_401_UNAUTHORIZED)

            data = {
                "username": user.get_username(),
                "email": user.email
            }

            return Response(data=data, status=status.HTTP_200_OK)


# -------------------------------------------------------------------------------------------------

# 1.禁用认证与权限
# 2.拿到前台登录信息
# 3.校验登录用户
# 4.签发token返回

class LoginAPIView(APIView):

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "用户名或密码错误"}, status=status.HTTP_400_BAD_REQUEST)

        token = my_obtain_jwt_token(username, 20)

        return Response({"token": token}, status=status.HTTP_200_OK)


class UserInfoAPIView(APIView):
    authentication_classes = [MyJSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user:
            return Response({"error": "认证失败"}, status=status.HTTP_401_UNAUTHORIZED)

        data = {
            "username": user.get_username(),
            "email": user.email
        }

        return Response(data=data, status=status.HTTP_200_OK)

# -------------------------------------------------------------------------------------------------
