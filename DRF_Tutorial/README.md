# Django REST Framework Tutorial

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

