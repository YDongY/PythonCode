# Flask-Restful-API

RESTful web services 概念的核心就是“资源”。 资源可以用 URI 来表示。 客户端使用 HTTP协议定义的方法来发送请求到这些 URIs， 当然可能会导致这些被访问的”资源“状态的改变。

HTTP 标准的方法有如下:

| Description  | Action Name | HTTP Mapping | HTTP URL                              | HTTP Request Body | HTTP Response Body |
| :----------- | :---------- | :----------- | ------------------------------------- | :---------------- | :----------------- |
| 查询所有     | list        | GET          | http://example.com/api/resources      | N/A               | Resource* list     |
| 获取单个资源 | query       | GET          | http://example.com/api/resources/{id} | N/A               | Resource*          |
| 创建单个资源 | create      | POST         | http://example.com/api/resources      | Resource          | Resource*          |
| 更新单个资源 | update      | PUT          | http://example.com/api/resources/{id} | Resource          | Resource*          |
| 删除单个资源 | delete      | DELETE       | http://example.com/api/resources/{id} | N/A               | Empty              |

REST 设计不需要特定的数据格式。 在请求中数据可以以 JSON 形式, 或者有时候作为 url 中查询参数项

## 使用 Flask 设计 RESTful API

- 查询所有

```python
@app.route("/api/v1/tasks/", methods=["GET"])
def get_tasks():
    return jsonify({"res": tasks})
```

- 获取单个资源

```python
@app.route("/api/v1/tasks/<int:tid>", methods=['GET'])
def get_task(tid):
    ...
    return jsonify({"res": task})
```

- 创建单个资源

```python
@app.route("/api/v1/tasks/", methods=["POST"])
def create_tasks():
    ...
    return jsonify({"res": task}), 201
```

- 更新单个资源

```python
@app.route("/api/v1/tasks/<int:tid>", methods=['PUT'])
def update_task(tid):
    ...
    return jsonify({"res": task})
```

- 删除单个资源

```python
@app.route("/api/v1/tasks/<int:tid>", methods=['DELETE'])
def delete_task(tid):
    ...
    return jsonify({"res": {}})
```

## 使用 Flask-RESTful 设计 RESTful API

```python
from flask import Flask
from flask_restful import Api, Resource, reqparse, inputs

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app) # 封装 app ，以后使用 api
```

- 添加路由

```python
api.add_resource(TaskAPI, "/api/v2/tasks/<int:tid>", endpoint='task')
api.add_resource(TasksAPI, "/api/v2/tasks", endpoint='tasks')
```

- GET(单一)/PUT/DELETE

```python
class TaskAPI(Resource):

    def get(self, tid):
        for task in self.tasks:
            if task["id"] == tid:
                return {"res": task}
        else:
            return {"error": "NOT FOUND"}, 404

    def put(self, tid):
        # ......
        
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, help="标题", require=True)
        parser.add_argument('pub_date', type=inputs.date, help="日期", require=True)
        parser.add_argument('comment', type=int, help="评论", required=False, default=0)
        parser.add_argument('image', type=str, help="图片路径", required=False, default=None)
        args = self.reqparse.parse_args()
        
        # ......

    def delete(self, tid):
        pass
```

- POST/GET(列表)

```python
class TasksAPI(Resource):

    def get(self):
        pass

    def post(self):
        pass
```

