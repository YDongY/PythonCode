# JWT - JSON Web Token

> [https://jwt.io/introduction/](https://jwt.io/introduction/)

## 什么是 JSON Web Token

JSON Web Token（JWT）是一个开放标准（[RFC 7519](https://tools.ietf.org/html/rfc7519)） ，它定义了一种紧凑且自包含的方式，用于在各方之间安全地传输信息作为 JSON 对象。由于此信息是经过数字签名的，因此可以被验证和信任。可以使用秘密（使用 HMAC 算法）或使用 RSA 或 ECDSA 的公用/专用密钥对对 JWT 进行签名。

JSON Web Token 应用场景：

授权：用户登录颁发 JWT ，之后每个请求将包括 JWT，从而通过校验 JWT 判断用户是否可以访问受限的路由，服务和资源。在单点登录中广泛使用 JWT ，因为它的开销很小并且可以在不同的域中轻松使用。

## JWT 认证流程



上图所示的过程进行认证，即：用户登录成功之后，服务端给用户浏览器返回一个**带盐的 JWT**，以后用户浏览器要携带 JWT 再去向服务端发送请求，服务端校验 JWT 的合法性，合法则给用户返回数据，否则，返回一些错误信息。

## JSON Web Token 结构

JSON Web Token 以紧凑的形式由三部分组成，这些部分由点（`.`）分隔，分别是：

- Header
- Payload
- Signature

因此，JWT 通常如下所示。

```python
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InJvb3QiLCJleHAiOjE2MDIxNDk4MzN9.8Xbyh3VA-gmgiD-k768-KPlPsim0Tq-c5KSA2aPBtq4
```

### Header

通常由两部分组成：令牌的类型（即JWT）和所使用的签名算法，例如 HMAC SHA256 或 RSA。

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

然后，此 JSON 被 **Base64Url** 编码以形成 JWT 的第一部分。

### Payload

令牌的第二部分是 Payload，其中包含一些数据，例如用户名、用户 ID，但最好不要存放密码，还可以存放其他数据，比如过期时间 exp

```json
{
  "exp": "1602160238",
  "name": "John Doe",
  "admin": true
}
```

然后，对有效负载进行　**Base64Url**　编码，以形成　JSON Web Token 的第二部分。

### Signature

把前两段的 base64url 密文通过`.`拼接起来，然后对其进行`HS256`加密，再然后对 `HS256` 密文进行 base64url 加密，最终得到 JSON Web Token 的第三段。

其中这一步需要加盐（secret），例如 Django 框架中的 SECRET_KEY

```
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret)
```

最后将三段字符串通过 `.`拼接起来就生成了 JSON Web Token。

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InJvb3QiLCJleHAiOjE2MDIxNDk4MzN9.8Xbyh3VA-gmgiD-k768-KPlPsim0Tq-c5KSA2aPBtq4
```

## Python 实现 JWT

- Python生成 JWT 的库  

```shell
pip install pyjwt
pip install python-jose
pip install jwcrypto
pip install authlib
```

### pyjwt

```python
import jwt
import time
secret = b"hdkahkhaj21njpogpapj1pgjpoajgoa" # 盐值
expire_time = int(time.time() + 3600) #过期时间
info={'id': 1,'name':'ydy','exp': expire_time} #保存的信息，以及过期时间
algorithm='HS256' #加密算法
encoded = jwt.encode(, secret, algorithm='HS256')
encoded_str = str(encoded, encoding='ascii') #针对于二进制的secret
# 结果：
'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwibmFtZSI6InlkeSIsImV4cCI6MTU4NzI4NzQzMn0.lzLLGWsg_clw6zMJdOMhpmmn83fva9oVBqxLYJ0Svrc'

# 解密
info = jwt.decode(encoded_str, secret, algorithm='HS256')
# 结果
{'exp': 1587287432, 'id': 1, 'name': 'ydy'}
```

### python-jose

```python
# 与Demo1相同，但是secret为str类型
from jose import jwt
secret = "hdkahkhaj21njpogpapj1pgjpoajgoa" # 盐值
token = jwt.encode({'key': 'value'}, 'secret', algorithm='HS256')
u'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJ2YWx1ZSJ9.FG-8UppwHaFp1LgRYQQeS6EDQF7_6-bMFegNucHjmWg'

jwt.decode(token, 'secret', algorithms=['HS256'])
{u'key': u'value'}
```

### [jwcrypto]( https://jwcrypto.readthedocs.io/en/latest/jwt.html   )

### authlib

```python
from authlib.jose import jwt
header = {'alg': 'HS256'}
payload = {'iss': 'Authlib', 'sub': '123', 'name': 'ydy'}
secret = '123abc.'
token = jwt.encode(header, payload, secret)
#token
b'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJBdXRobGliIiwic3ViIjoiMTIzIiwibmFtZSI6InlkeWQifQ.XwnXrosudR1fZ5kDUMadkxj8nGW6OpMoSfOkDlbOYa8'
```

## Django 集成 JWT

在用户登录成功之后，生成 JWT 并返回，用户再次来访问时需携带 JWT 。

```python
class LoginAPIView(APIView):

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "用户名或密码错误"}, status=status.HTTP_400_BAD_REQUEST)

        token = my_obtain_jwt_token(username, 20) # 生成 JWT

        return Response({"token": token}, status=status.HTTP_200_OK)
```

```python
def my_obtain_jwt_token(username, expire_time=10):
    """通过用户名生成 payload"""
    # 手动生成 token
    secret = settings.SECRET_KEY
    expire_time = int(time.time() + expire_time)  # 过期时间

    payload = {
        "username": username,
        'exp': expire_time
    }

    token = jwt.encode(payload, secret, algorithm='HS256')

    return token
```

自定义 JWT 规则

```python
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
```

集成到 DRF，访问需要授权的用户信息

```python
class UserInfoAPIView(APIView):
    authentication_classes = [MyJSONWebTokenAuthentication] # JWT 认证
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
```

