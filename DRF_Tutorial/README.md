# Django REST Framework Tutorial

- [RESTful](#restful)
- [Django &amp; Django REST framework](#django--django-rest-framework)
- [环境安装与配置](#环境安装与配置)
- [Serializer 序列化器](#serializer-序列化器)
     - [Serializer](#serializer)
     - [ModelSerializer](#modelserializer)
     - [HyperlinkedModelSerializer](#hyperlinkedmodelserializer)
     - [ListSerializer](#listserializer)
- [视图](#视图)
     - [APIView](#apiview)
     - [GenericAPIView](#genericapiview)
     - [ListModelMixin](#listmodelmixin)
     - [CreateModelMixin](#createmodelmixin)
     - [RetrieveModelMixin](#retrievemodelmixin)
     - [UpdateModelMixin](#updatemodelmixin)
     - [DestroyModelMixin](#destroymodelmixin)
     - [Concrete View Classes](#concrete-view-classes)
     - [Customizing the generic views](#customizing-the-generic-views)
          * [Custom Mixin](#custom-mixin)
- [ViewSets](#viewsets)
- [Routers](#routers)
- [Parsers](#parsers)
     - [Setting the parsers](#setting-the-parsers)
     - [API Reference](#api-reference)
     - [Custom parsers](#custom-parsers)
- [Renderers](#renderers)
     - [Custom renderers](#custom-renderers)
- [Authentication](#authentication)
     - [API Reference](#api-reference-1)
     - [Custom authentication](#custom-authentication)
- [Permissions](#permissions)
     - [Custom permissions](#custom-permissions)
- [Throttling](#throttling)
     - [Custom throttles](#custom-throttles)
- [Filtering](#filtering)
     - [SearchFilter](#searchfilter)
     - [OrderingFilter](#orderingfilter)
     - [Custom generic filtering](#custom-generic-filtering)
- [Pagination](#pagination)
     - [PageNumberPagination](#pagenumberpagination)
     - [LimitOffsetPagination](#limitoffsetpagination)
     - [Custom pagination styles](#custom-pagination-styles)
- [Exceptions](#exceptions)
- [Settings](#settings)
- [相关参考](#相关参考)

Django REST Framework 是方便 Django 框架设计 REST API

## RESTful

传统的 API 设计：

- POST /add-post    新建文章
- POST /delete-post 删除文章
- POST /update-post 修改文章
- GET  /get-post    获取文章

REST API 设计

- 尽量将API部署在专用域名之下

```http request
https://api.example.com
https://example.org/api/
```

- 将 API 的版本号放入 URL

```http request
http://www.example.com/app/1.0/foo
http://www.example.com/app/1.1/foo
http://www.example.com/app/2.0/foo
```

- 另一种做法是，将版本号放在HTTP头信息中

```http request
Accept: vnd.example-com.foo+json; version=1.0

Accept: vnd.example-com.foo+json; version=1.1

Accept: vnd.example-com.foo+json; version=2.0
```

- 符合 RESTful 规范的 API 

```http
GET    /posts   ：获取所有文章（幂等）
POST   /posts   ：创建新文章（非幂等）
GET    /posts/1 ：获取 id 为 1 的文章（幂等）
PATCH  /posts/1 ：更新 id 为 1 的文章，局部更新（非幂等）
PUT    /posts/1 ：更新 id 为 1 的文章，全部更新（幂等）
DELELE /posts/1 ：删除 id 为 1 的文章（幂等）
```

- 返回结果

```http
GET      /collection              ：返回资源对象的列表（数组）
GET      /collection/resource     ：返回单个资源对象
POST     /collection              ：返回新生成的资源对象
PUT      /collection/resource     ：返回完整的资源对象
PATCH    /collection/resource     ：返回完整的资源对象
DELETE   /collection/resource     ：返回一个空文档
```

> RESTful 设计通过 HTTP 动词表示资源操作行为，使得 URL 中包含名词，而非动词

- 条件过滤

```http
?limit=10             ：指定返回记录的数量
?offset=10            ：指定返回记录的开始位置。
?page=2&per_page=100  ：指定第几页，以及每页的记录数。
?sortby=name&order=asc：指定返回结果按照哪个属性排序，以及排序顺序。
?post_type_id=1       ：指定筛选条件
```

- 状态码

```http
200 OK - [GET]                            ：服务器成功返回用户请求的数据
201 CREATED - [POST/PUT/PATCH]            ：用户新建或修改数据成功。
202 Accepted - [*]                        ：表示一个请求已经进入后台排队（异步任务）
204 NO CONTENT - [DELETE]                 ：用户删除数据成功。
400 INVALID REQUEST - [POST/PUT/PATCH]    ：用户发出的请求有错误，服务器没有进行新建或修改数据的操作
401 Unauthorized - [*]                    ：表示用户没有权限（令牌、用户名、密码错误）。
403 Forbidden - [*]                       ：表示用户得到授权（与401错误相对），但是访问是被禁止的。
404 NOT FOUND - [*]                       ：用户发出的请求针对的是不存在的记录，服务器没有进行操作，该操作是幂等的。
406 Not Acceptable - [GET]                ：用户请求的格式不可得（比如用户请求JSON格式，但是只有XML格式）。
410 Gone - [GET]                          ：用户请求的资源被永久删除，且不会再得到的。
422 Unprocesable entity - [POST/PUT/PATCH]：当创建一个对象时，发生一个验证错误。
500 INTERNAL SERVER ERROR - [*]           ：服务器发生错误，用户将无法判断发出的请求是否成功。
```

## Django & Django REST framework

在开发 REST API 的视图中，虽然每个视图具体操作的数据不同，但增、删、改、查的实现流程基本套路化，所以这部分代码也是可以复用简化编写的：

- 增：校验请求数据 -> 执行反序列化过程 -> 保存数据库 -> 将保存的对象序列化并返回
- 删：判断要删除的数据是否存在 -> 执行数据库删除
- 改：判断要修改的数据是否存在 -> 校验请求的数据 -> 执行反序列化过程 -> 保存数据库 -> 将保存的对象序列化并返回
- 查：查询数据库 -> 将数据序列化并返回

> 序列化：字典对象转 JSON
> 反序列化：JSON 转字典对象

在使用传统 Django 实现 REST API 视图过程中，我们需要自行实现序列化和反序列化操作，而 Django REST framework 提供了定义序列化器 Serializer 的方法，可以快速根据 Django ORM 或者其它库自动序列化和反序列化。

同时提供丰富的视图，Mixin 扩展类，简化视图的编写。同时包含多种身份认证和权限认证方式的支持、内置了限流系统、以及直观的 API web 调试界面

## 环境安装与配置

- 安装 DRF

```shell
pip install djangorestframework
```

- 添加 rest_framework 应用

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

## Serializer 序列化器

### [Serializer](https://www.django-rest-framework.org/api-guide/serializers/#serializers)

```python
from rest_framework import serializers

class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

- 序列化

```python
from . import CommentSerializer

serializer = CommentSerializer(comment)
serializer.data
# {'email': 'leila@example.com', 'content': 'foo bar', 'created': '2016-01-27T15:17:10.375877'}
```

- 反序列化

```python
serializer = CommentSerializer(data=data)
serializer.is_valid()
# True
serializer.validated_data
# {'content': 'foo bar', 'email': 'leila@example.com', 'created': datetime.datetime(2012, 08, 22, 16, 20, 09, 822243)}
```

- 保存

> 如果创建序列化器对象的时候，没有传递instance实例，则调用save()方法的时候，create()被调用，相反，如果传递了instance实例，则调用save()方法的时候，update()被调用。

```python
# .save() will create a new instance.
serializer = CommentSerializer(data=data)

# .save() will update the existing `comment` instance.
serializer = CommentSerializer(comment, data=data)

comment = serializer.save()
```

```python
class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance
```

### [ModelSerializer](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer)

```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'users', 'created']
        read_only_fields = ['account_name'] # 只读字段
        extra_kwargs = {'account_name': {'write_only': True}} # 额外参数
```

### [HyperlinkedModelSerializer](https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer)

> 默认情况下，序列化程序将包含一个 url 字段而不是主键字段。

```python
class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['account_url', 'account_name', 'users', 'created']
        extra_kwargs = {
            'url': {'view_name': 'accounts', 'lookup_field': 'account_name'},
            'users': {'lookup_field': 'username'}
        }
```

或

```python
class AccountSerializer(serializers.HyperlinkedModelSerializer):
    # view_name 和 urls.py 中的 name 参数相对应，表示使用哪个 url
    # lookup_field 表示用哪个字段来作为 url 的唯一识别标记
    url = serializers.HyperlinkedIdentityField(
        view_name='accounts',
        lookup_field='slug'
    )
    users = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        lookup_field='username',
        many=True,
        read_only=True
    )

    class Meta:
        model = Account
        fields = ['url', 'account_name', 'users', 'created']
```

### [ListSerializer](https://www.django-rest-framework.org/api-guide/serializers/#listserializer)

ListSerializer 类提供了序列化和一次验证多个对象的行为。通常不需要 ListSerializer 直接使用，而应该 many=True 在实例化序列化程序时指定

## 视图

### [APIView](https://www.django-rest-framework.org/api-guide/views/#class-based-views)

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
```

### [GenericAPIView](https://www.django-rest-framework.org/api-guide/generic-views/#genericapiview)

```python
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

class UserDetailView(GenericAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
```

### [ListModelMixin](https://www.django-rest-framework.org/api-guide/generic-views/#listmodelmixin)

列表视图扩展类，提供 list(request, *args, **kwargs) 方法快速实现列表视图，返回200状态码。

该 Mixin 的 list 方法会对数据进行过滤和分页。

源代码：
```python
class ListModelMixin(object):
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        # 过滤
        queryset = self.filter_queryset(self.get_queryset())
        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        # 序列化
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
```

### [CreateModelMixin](https://www.django-rest-framework.org/api-guide/generic-views/#createmodelmixin)

创建视图扩展类，提供create(request, *args, **kwargs)方法快速实现创建资源的视图，成功返回201状态码。

如果序列化器对前端发送的数据验证失败，返回400错误。

源代码：
```python
class CreateModelMixin(object):
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        # 获取序列化器
        serializer = self.get_serializer(data=request.data)
        # 验证
        serializer.is_valid(raise_exception=True)
        # 保存
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
```

### [RetrieveModelMixin](https://www.django-rest-framework.org/api-guide/generic-views/#retrievemodelmixin)
详情视图扩展类，提供retrieve(request, *args, **kwargs)方法，可以快速实现返回一个存在的数据对象。

如果存在，返回200， 否则返回404。

源代码：
```python
class RetrieveModelMixin(object):
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        # 获取对象，会检查对象的权限
        instance = self.get_object()
        # 序列化
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
```

### [UpdateModelMixin](https://www.django-rest-framework.org/api-guide/generic-views/#updatemodelmixin)
更新视图扩展类，提供update(request, *args, **kwargs)方法，可以快速实现更新一个存在的数据对象。

同时也提供partial_update(request, *args, **kwargs)方法，可以实现局部更新。

成功返回200，序列化器校验数据失败时，返回400错误。

源代码：
```python
class UpdateModelMixin(object):
    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
```

### [DestroyModelMixin](https://www.django-rest-framework.org/api-guide/generic-views/#destroymodelmixin)
删除视图扩展类，提供destroy(request, *args, **kwargs)方法，可以快速实现删除一个存在的数据对象。

成功返回204，不存在返回404。

源代码：
```python
class DestroyModelMixin(object):
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
```

### [Concrete View Classes](https://www.django-rest-framework.org/api-guide/generic-views/#concrete-view-classes)

| 类                           | 方法                    | 描述                                                         |
| ---------------------------- | ----------------------- | ------------------------------------------------------------ |
| CreateAPIView                | post                    | 继承自： GenericAPIView、CreateModelMixin                    |
| ListAPIView                  | get                     | 继承自：GenericAPIView、ListModelMixin                       |
| RetireveAPIView              | get                     | 继承自: GenericAPIView、RetrieveModelMixin                   |
| DestoryAPIView               | delete                  | 继承自：GenericAPIView、DestoryModelMixin                    |
| UpdateAPIView                | put、patch              | 继承自：GenericAPIView、UpdateModelMixin                     |
| RetrieveUpdateAPIView        | get、put、patch         | 继承自： GenericAPIView、RetrieveModelMixin、UpdateModelMixin |
| RetrieveUpdateDestoryAPIView | get、put、patch、delete | 继承自：GenericAPIView、RetrieveModelMixin、UpdateModelMixin、DestoryModelMixin |

### [Customizing the generic views](https://www.django-rest-framework.org/api-guide/generic-views/#customizing-the-generic-views)

#### 创建自定义 Mixin

例如，如果您需要根据 URL conf 中的多个字段查找对象，则可以创建一个 mixin 类。

```python
class MultipleFieldLookupMixin:
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]: # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj
```

随后可以在需要应用自定义行为的任​​何时候，将该 mixin 应用于视图或视图集。

```python
class RetrieveUserView(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_fields = ['account', 'username']
```

## [ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/#viewsets)

ViewSet 类只是一种基于类的 View，它不提供任何处理方法，如 .get() 或 .post()，而是提供诸如 .list() 和 .create() 之类的操作。

ViewSet 只在用 .as_view() 方法绑定到最终化视图时做一些相应操作。

通常，不是在 urlconf 中的视图集中明确注册视图，而是使用路由器类注册视图集，这会自动为您确定 urlconf。

定义一个简单的视图集，可以用来列出或检索系统中的所有用户。

```python
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from myapps.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.response import Response

class UserViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
```

如果需要，可以将这个视图集合成两个单独的视图，如下所示：

```python
user_list = UserViewSet.as_view({'get': 'list'})
user_detail = UserViewSet.as_view({'get': 'retrieve'})
```

通常情况下，我们不会这样做，而是用路由器注册视图集，并允许自动生成 urlconf。

```python
from myapp.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, base_name='user')
urlpatterns = router.urls
```

- [标记额外的路由行为](http://drf.jiuyou.info/#/drf/viewsets?id=%e6%a0%87%e8%ae%b0%e9%a2%9d%e5%a4%96%e7%9a%84%e8%b7%af%e7%94%b1%e8%a1%8c%e4%b8%ba)
- [action 跳转](http://drf.jiuyou.info/#/drf/viewsets?id=action-%e8%b7%b3%e8%bd%ac)


| 类                   | 描述                                                         |
| -------------------- | ------------------------------------------------------------ |
| ViewSet              | 继承自`APIView`，作用也与 APIView 基本类似，提供了身份认证、权限校验、流量管理等。在 ViewSet 中，没有提供任何动作 action 方法，需要我们自己实现 action 方法。 |
| GenericViewSet       | 继承自`GenericAPIView`，作用也与 GenericAPIVIew 类似，提供了 get_object、get_queryset 等方法便于列表视图与详情信息视图的开发。 |
| ModelViewSet         | 继承自`GenericAPIVIew`，同时包括了ListModelMixin、RetrieveModelMixin、CreateModelMixin、UpdateModelMixin、DestoryModelMixin。 |
| ReadOnlyModelViewSet | 继承自`GenericAPIVIew`，同时包括了ListModelMixin、RetrieveModelMixin。 |

## [Routers](https://www.django-rest-framework.org/api-guide/routers/#routers)

```python
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)
urlpatterns = router.urls
```

register() 方法有两个必须参数：

- prefix - 设置这组路由的前缀。
- viewset - 设置对应的视图集类

上面的例子会生成以下 URL 模式：

- URL pattern: ^users/$         Name: 'user-list'
- URL pattern: ^users/{pk}/$    Name: 'user-detail'
- URL pattern: ^accounts/$      Name: 'account-list'
- URL pattern: ^accounts/{pk}/$ Name: 'account-detail'

## [Parsers](https://www.django-rest-framework.org/api-guide/parsers/#parsers)

当访问 request.data 时，REST framework 将检查传入请求的 Content-Type ，并确定使用哪个解析器来解析请求内容。

### [Setting the parsers](https://www.django-rest-framework.org/api-guide/parsers/#setting-the-parsers)

```python
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
}
```

还可以在基于类（API​​View ）的视图上设置单个视图或视图集的解析器。

```python
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
    """
    A view that can accept POST requests with JSON content.
    """
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        return Response({'received data': request.data})
```

或者和 @api_view 装饰器一起使用。

```python
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

@api_view(['POST'])
@parser_classes((JSONParser,))
def example_view(request, format=None):
    """
    A view that can accept POST requests with JSON content.
    """
    return Response({'received data': request.data})
```

### [API Reference](https://www.django-rest-framework.org/api-guide/parsers/#api-reference)

| 解析类           | 说明                                                         | 类型                              |
| ---------------- | ------------------------------------------------------------ | --------------------------------- |
| JSONParser       | 解析 JSON 请求内容。                                         | application/json                  |
| FormParser       | 解析 HTML 表单内容。`request.data` 是一个 `QueryDict` 字典，包含所有表单参数。通常需要同时使用 `FormParser` 和 `MultiPartParser`，以完全支持 HTML 表单数据。 | application/x-www-form-urlencoded |
| MultiPartParser  | 解析文件上传的 multipart HTML 表单内容                       | application/form-data             |
| FileUploadParser | 解析文件上传内容。 `request.data` 是一个 `QueryDict` （只包含一个存有文件的 `'file'` key）。 | */*                               |

基本用法示例：

```python
# views.py
class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        # ...
        # do some stuff with uploaded file
        # ...
        return Response(status=204)

# urls.py
urlpatterns = [
    # ...
    url(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view())
]
```

### [Custom parsers](https://www.django-rest-framework.org/api-guide/parsers/#custom-parsers)

要实现自定义解析器，应该继承 BaseParser，设置 .media_type 属性并实现 .parse(self,stream,media_type,parser_context) 方法。

该方法应该返回将用于填充 request.data 属性的数据。

传递给 .parse() 的参数是：

- stream：表示请求正文的流式对象。
- media_type：可选。如果提供，则这是传入请求内容的 media type。
- parser_context：可选。如果提供，则该参数将是一个包含解析请求内容可能需要的任何其他上下文的字典。默认情况下，这将包括以下 key：view，request，args，kwargs。


```python
class PlainTextParser(BaseParser):
    """
    Plain text parser.
    """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        return stream.read()
```

## [Renderers](https://www.django-rest-framework.org/api-guide/renderers/#renderers)

使用 DEFAULT_RENDERER_CLASSES 设置全局的默认渲染器集。例如，以下设置将使用JSON作为主要 media type，并且还包含自描述 API。

```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}
```

还可以使用基于 API​​View 的视图类来设置单个视图或视图集的渲染器。

```python
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

class UserCountView(APIView):
    """
    A view that returns the count of active users in JSON.
    """
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        user_count = User.objects.filter(active=True).count()
        content = {'user_count': user_count}
        return Response(content)
```

或者是在基于 @api_view 装饰器的函数视图上设置。

```python
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def user_count_view(request, format=None):
    """
    A view that returns the count of active users in JSON.
    """
    user_count = User.objects.filter(active=True).count()
    content = {'user_count': user_count}
    return Response(content)
```

- JSONRenderer
- TemplateHTMLRenderer
- StaticHTMLRenderer
- BrowsableAPIRenderer
- AdminRenderer
- HTMLFormRenderer
- MultiPartRenderer

### [Custom renderers](https://www.django-rest-framework.org/api-guide/renderers/#custom-renderers)

要实现自定义渲染器，您应该继承 BaseRenderer ，设置 .media_type 和 .format 属性，并实现 .render(self, data, media_type=None, renderer_context=None) 方法。

```python
from django.utils.encoding import smart_text
from rest_framework import renderers


class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'
    charset = 'iso-8859-1'

    def render(self, data, media_type=None, renderer_context=None):
        return smart_text(data, encoding=self.charset)
```

## [Authentication](https://www.django-rest-framework.org/api-guide/authentication/#authentications)

认证方案总是被定义为一个类的列表。 REST framework 将尝试使用列表中的每个类进行认证，并将使用成功认证的第一个类的返回值来设置 request.user 和 request.auth 。

如果没有类进行身份验证，则将 request.user 设置为 django.contrib.auth.models.AnonymousUser 的实例，并将 request.auth 设置为 None.

可以使用 UNAUTHENTICATED_USER 和 UNAUTHENTICATED_TOKEN 设置修改未经身份验证的请求的 request.user 和 request.auth 的值。

在配置文件中配置全局默认的认证方案

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',   # 基本认证
        'rest_framework.authentication.SessionAuthentication',  # session认证
    )
}
```

也可以在每个视图中通过设置authentication_classes属性来设置

```python
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView

class ExampleView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    ...
```

或者，如果您将 @api_view 装饰器与基于函数的视图一起使用。

```python
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def example_view(request, format=None):
    content = {
        'user': unicode(request.user),  # `django.contrib.auth.User` instance.
        'auth': unicode(request.auth),  # None
    }
    return Response(content)
```

认证失败会有两种可能的返回值：

- 401 Unauthorized 未认证
- 403 Permission Denied 权限被禁止

### [API Reference](https://www.django-rest-framework.org/api-guide/authentication/#api-reference)

- BasicAuthentication
- TokenAuthentication：此认证方案使用简单的基于令牌的 HTTP 认证方案

要使用 TokenAuthentication 方案，您需要将认证类配置为包含 TokenAuthentication ，并在 INSTALLED_APPS 设置中另外包含 rest_framework.authtoken ：

```python
INSTALLED_APPS = (
    ...
    'rest_framework.authtoken'
)
```
- SessionAuthentication：此认证方案使用 Django 的默认 session 后端进行认证
- RemoteUserAuthentication：这种身份验证方案允许您将身份验证委托给您的 Web 服务器

### [Custom authentication](https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication)

要实现自定义身份验证方案，请继承 BaseAuthentication 并重写 .authenticate(self, request) 方法。如果认证成功，该方法应返回 (user, auth) 的二元组，否则返回 None。

```python
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('X_USERNAME')
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return user, None
```

## [Permissions](https://www.django-rest-framework.org/api-guide/permissions/#permissions)

权限控制可以限制用户对于视图的访问和对于具体数据对象的访问。

- 在执行视图的dispatch()方法前，会先进行视图访问权限的判断
- 在通过get_object()获取具体对象时，会进行对象访问权限的判断

在配置文件中设置默认的权限管理类，如

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}
```

如果未指明，则采用如下默认配置

```python
'DEFAULT_PERMISSION_CLASSES': (
   'rest_framework.permissions.AllowAny',
)
```

也可以在具体的视图中通过permission_classes属性来设置，如

```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class ExampleView(APIView):
    permission_classes = (IsAuthenticated,)
    ...
```

或者在基于 @api_view 装饰器的函数视图上设置。

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def example_view(request, format=None):
    content = {
        'status': 'request was permitted'
    }
    return Response(content)
```

- AllowAny 允许所有用户
- IsAuthenticated 仅通过认证的用户
- IsAdminUser 仅管理员用户
- IsAuthenticatedOrReadOnly 认证的用户可以完全操作，否则只能get读取


### [Custom permissions](https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions)

要实现自定义权限，请继承 BasePermission 并实现以下方法中的一个或两个：

- .has_permission(self, request, view)
- .has_object_permission(self, request, view, obj)

如果请求被授予访问权限，则方法应该返回 True，否则返回 False。

```python
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
```

## [Throttling](https://www.django-rest-framework.org/api-guide/throttling/#throttling)

可以使用 DEFAULT_THROTTLE_CLASSES 和 DEFAULT_THROTTLE_RATES setting 全局设置默认限流策略。例如：

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}
```

DEFAULT_THROTTLE_RATES 中使用的频率描述可能包括 second，minute ，hour 或 day 作为限流期。

你还可以使用基于 APIView 类的视图，在每个视图或每个视图集的基础上设置限流策略。

```python
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

class ExampleView(APIView):
    throttle_classes = (UserRateThrottle,)

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)
```

或者在基于 @api_view 装饰器的函数视图上设置。

```python
@api_view(['GET'])
@throttle_classes([UserRateThrottle])
def example_view(request, format=None):
    content = {
        'status': 'request was permitted'
    }
    return Response(content)
```

- AnonRateThrottle

限制所有匿名未认证用户，使用IP区分用户。

使用DEFAULT_THROTTLE_RATES['anon'] 来设置频次

- UserRateThrottle

限制认证用户，使用User id 来区分。

使用DEFAULT_THROTTLE_RATES['user'] 来设置频次

- ScopedRateThrottle

限制用户对于每个视图的访问频次，使用ip或user id。

例如：

```python
class ContactListView(APIView):
    throttle_scope = 'contacts'
    ...

class ContactDetailView(APIView):
    throttle_scope = 'contacts'
    ...

class UploadView(APIView):
    throttle_scope = 'uploads'
    ...
```
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'contacts': '1000/day',
        'uploads': '20/day'
    }
}
```
用户对 ContactListView 或 ContactDetailView 的请求将被限制为每天 1000 次。用户对 UploadView 的请求将被限制为每天 20 次。

### [Custom throttles](https://www.django-rest-framework.org/api-guide/throttling/#custom-throttles)

要自定义限流，请继承 BaseThrottle 类并实现 .allow_request(self, request, view) 方法。如果请求被允许，该方法应该返回 True，否则返回 False。

或者，你也可以重写 .wait() 方法。如果实现，.wait() 应该返回建议的秒数，在尝试下一次请求之前等待，或者返回 None。如果 .allow_request() 先前已经返回 False，则只会调用 .wait() 方法。

如果 .wait() 方法被实现并且请求受到限制，那么 Retry-After header 将包含在响应中。

以下是限流的一个示例，随机地控制每 10 次请求中的 1 次。

```python
import random

class RandomRateThrottle(throttling.BaseThrottle):
    def allow_request(self, request, view):
        return random.randint(1, 10) != 1
```

## [Filtering](https://www.django-rest-framework.org/api-guide/filtering/#filtering)

django-filter 库包含一个 DjangoFilterBackend 类，它支持 REST framework 对字段过滤进行高度定制。

要使用 DjangoFilterBackend，首先安装 django-filter。然后将 django_filters 添加到 Django 的 INSTALLED_APPS 中


```shell script
pip install django-filter
```

将过滤器后端添加到设置中：

```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}
```

或者将过滤器后端添加到单个视图或视图集。

```python
from django_filters.rest_framework import DjangoFilterBackend

class UserListView(generics.ListAPIView):
    ...
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('category', 'in_stock')
```

这将自动为给定字段创建一个 FilterSet 类，并允许你发出如下请求：

```http request
http://example.com/api/products?category=clothing&in_stock=True
```

### [SearchFilter](https://www.django-rest-framework.org/api-guide/filtering/#searchfilter)

SearchFilter 类将仅在视图具有 search_fields 属性集的情况下应用。search_fields 属性应该是模型上文本类型字段的名称列表，例如 CharField 或 TextField。

```python
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', 'email')
```

这将允许客户端通过查询来过滤列表中的项目，例如：

```http request
http://example.com/api/users?search=russell
```

你还可以使用查找 API 双下划线表示法对 ForeignKey 或 ManyToManyField 执行相关查找：

```python
search_fields = ('username', 'email', 'profile__profession')
```

搜索行为可以通过将各种字符预先添加到 search_fields 来限制。

- '^' 匹配起始部分。
- '=' 完全匹配。
- '@' 全文搜索。（目前只支持 Django 的 MySQL 后端。）
- '$' 正则匹配。
例如：
```http request
search_fields = ('=username', '=email')
```

默认情况下，搜索参数被命名为 'search' ，但这可能会被 **SEARCH_PARAM** setting 覆盖。


### [OrderingFilter](https://www.django-rest-framework.org/api-guide/filtering/#orderingfilter)

OrderingFilter 类支持简单查询参数控制结果的排序。

默认情况下，查询参数被命名为 'ordering'，但这可能会被 ORDERING_PARAM setting 覆盖。

例如，要通过 username 对用户排序：

```http request
http://example.com/api/users?ordering=username
```

客户端也可以通过在字段名称前加 ' - ' 来指定反向排序，如下所示：

```http request
http://example.com/api/users?ordering=-username 
```

也可以指定多个排序：

```http request
http://example.com/api/users?ordering=account,username
```

通过在视图上设置一个 ordering_fields 属性来完成此操作，如下所示：

```python
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('username', 'email')
```

### [Custom generic filtering](https://www.django-rest-framework.org/api-guide/filtering/#custom-generic-filtering)

继承 BaseFilterBackend，并覆盖 .filter_queryset(self, request, queryset, view) 方法。该方法应该返回一个新的，过滤的查询集。

```python
class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)
```

## [Pagination](https://www.django-rest-framework.org/api-guide/pagination/#pagination)

分页样式可以使用 DEFAULT_PAGINATION_CLASS 和 PAGE_SIZE setting key 全局设置。例如，要使用内置的 limit/offset 分页，你可以这样做：

```python
REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_PAGINATION_CLASS':  'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100  # 每页数目
}
```

也可通过自定义Pagination类，来为视图添加不同分页行为。在视图中通过pagination_clas属性来指明。

```python
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000
```

### PageNumberPagination

前端访问网址形式：

```http request
GET  http://api.example.org/books/?page=4
```
- page_size 每页数目
- page_query_param 前端发送的页数关键字名，默认为"page"
- page_size_query_param 前端发送的每页数目关键字名，默认为None
- max_page_size 前端最多能设置的每页数量

### LimitOffsetPagination

前端访问网址形式：

```http request
GET http://api.example.org/books/?limit=100&offset=400
```

- default_limit 默认限制，默认值与PAGE_SIZE设置一直
- limit_query_param limit参数名，默认'limit'
- offset_query_param offset参数名，默认'offset'
- max_limit 最大limit限制，默认None


### [Custom pagination styles](https://www.django-rest-framework.org/api-guide/pagination/#custom-pagination-styles)

继承 pagination.BasePagination 并覆盖 paginate_queryset(self, queryset, request, view=None) 和 get_paginated_response(self, data) 方法：

- paginate_queryset 方法被传递给初始查询集，并且应该返回一个只包含请求页面中的数据的可迭代对象。
- get_paginated_response 方法传递序列化的页面数据，并返回一个 Response 实例。

假设我们想用一个修改后的格式替换默认的分页输出样式，该样式包含嵌套的 “links” key（包含上一页，下一页链接）。我们可以像这样指定一个自定义分页类：

```python
class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })
```

然后我们需要在配置中设置自定义类：

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'my_project.apps.core.pagination.CustomPagination',
    'PAGE_SIZE': 100
}
```

## [Exceptions](https://www.django-rest-framework.org/api-guide/exceptions/#exceptions)

REST framework提供了异常处理，我们可以自定义异常处理函数。

```python
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # 先调用REST framework默认的异常处理方法获得标准错误响应对象
    response = exception_handler(exc, context)

    # 在此处补充自定义的异常处理
    if response is not None:
        response.data['status_code'] = response.status_code

    return response
```

在配置文件中声明自定义的异常处理

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'my_project.my_app.utils.custom_exception_handler'
}
```

如果未声明，会采用默认的方式，如下

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler'
}
```

例如：处理关于数据库的异常

```python
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status
from django.db import DatabaseError

def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is None:
        view = context['view']
        if isinstance(exc, DatabaseError):
            print('[%s]: %s' % (view, exc))
            response = Response({'detail': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response
```

## [Settings](https://www.django-rest-framework.org/api-guide/settings/#settings)


## 相关参考

- https://www.django-rest-framework.org/
- http://drf.jiuyou.info/#/

