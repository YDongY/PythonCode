# __Time__ : 2020/10/9 下午5:54
# __Author__ : '__YDongY__'

from flask import Flask, abort
from flask_restful import Api, Resource, reqparse, inputs

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)


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


class TasksAPI(Resource):

    def get(self):
        pass

    def post(self):
        pass


api.add_resource(TaskAPI, "/api/v2/tasks/<int:tid>", endpoint='task')
api.add_resource(TasksAPI, "/api/v2/tasks", endpoint='tasks')

if __name__ == '__main__':
    app.run()
