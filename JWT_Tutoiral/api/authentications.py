# __Time__ : 2020/10/8 下午4:50
# __Author__ : '__YDongY__'

"""

1.继承BaseAuthentication
2.重写authenticate方法，自定义认证规则
3.认证规则基于条件:
　　没有认证信息返回None
　　有认证信息认证失败抛异常
　　有认证信息认证成功，返回用户与认证信息
4. 完成视图类全局(settings)或局部配置(视图类属性)

"""

from jose import jwt, exceptions

from rest_framework.authentication import BaseAuthentication
from rest_framework import HTTP_HEADER_ENCODING, exceptions

from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model


def get_authorization_header(request):
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, str):
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class MyJSONWebTokenAuthentication(BaseAuthentication):
    """
        Authorization: AUTH eyJhbGciOiAiSFMyNTYiLCAidHlwIj
    """

    def get_jwt_value(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'auth':
            return None

        if len(auth) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

    def authenticate(self, request):
        """
                Returns a two-tuple of `User` and token if a valid signature has been
                supplied using JWT-based authentication.  Otherwise returns `None`.
                """
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None

        try:
            payload = jwt.decode(jwt_value.decode(HTTP_HEADER_ENCODING), settings.SECRET_KEY, algorithms=['HS256'])
        except exceptions.ExpiredSignatureError:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except exceptions.JWTError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except exceptions.ValidationError:
            raise exceptions.AuthenticationFailed()

        user = self.authenticate_credentials(payload)

        return user, jwt_value

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user username.
        """
        User = get_user_model()
        username = payload.get('username')

        if not username:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            msg = _('Invalid signature.')
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.AuthenticationFailed(msg)

        return user
