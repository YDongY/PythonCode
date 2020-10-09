# __Time__ : 2020/10/9 下午4:21
# __Author__ : '__YDongY__'

import json
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

app.config["DEBGU"] = True

with open("data.json", 'r') as f:
    tasks = json.load(f)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": 'NOT FOUND'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"error": "Bad Request"}), 400)


@app.route("/api/v1/tasks/", methods=["GET"])
def get_tasks():
    return jsonify({"res": tasks})


@app.route("/api/v1/tasks/<int:tid>", methods=['GET'])
def get_task(tid):
    for task in tasks:
        if task["id"] == tid:
            return jsonify({"res": task})
    else:
        abort(404)


@app.route("/api/v1/tasks/", methods=["POST"])
def create_tasks():
    data = request.json
    if not data or not data.get("title") or not data.get("pub_date"):
        abort(400)

    task = {
        "id": id if data.get("id") else tasks[-1]["id"] + 1,
        "title": data["title"],
        "pub_date": data["pub_date"],
        "comment": 0,
        "image": None
    }

    tasks.append(task)
    with open("data.json", 'w') as f:
        json.dump(tasks, f, indent=4)

    return jsonify({"res": task}), 201


@app.route("/api/v1/tasks/<int:tid>", methods=['PUT'])
def update_task(tid):
    task_index = -1
    for index, t in enumerate(tasks):
        if t["id"] != int(tid):
            continue
        else:
            task_index = index
            break
    if task_index == -1:
        abort(400)

    data = request.json
    if not data:
        abort(400)

    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'pub_date' in request.json and type(request.json['pub_date']) != str:
        abort(400)
    if 'comment' in request.json and type(request.json['comment']) != int:
        abort(400)

    tasks[task_index]['title'] = request.json.get('title', tasks[task_index]['title'])
    tasks[task_index]['pub_date'] = request.json.get('pub_date', tasks[task_index]['pub_date'])
    tasks[task_index]['comment'] = request.json.get('comment', tasks[task_index]['comment'])
    tasks[task_index]['image'] = request.json.get('image', tasks[task_index]['image'])

    with open("data.json", 'w') as f:
        json.dump(tasks, f, indent=4)

    return jsonify({"res": tasks[task_index]})


@app.route("/api/v1/tasks/<int:tid>", methods=['DELETE'])
def delete_task(tid):
    task_index = -1
    for index, t in enumerate(tasks):
        if t["id"] != int(tid):
            continue
        else:
            task_index = index
            break
    if task_index == -1:
        abort(400)

    tasks.pop(task_index)
    with open("data.json", 'w') as f:
        json.dump(tasks, f, indent=4)

    return jsonify({"res": {}})


if __name__ == '__main__':
    app.run(debug=True)
