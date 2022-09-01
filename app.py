import redis
from rq import Queue, Connection
from flask import render_template, Blueprint, jsonify, request, current_app

from task import create_task
import os

from flask import Flask
from flask_bootstrap import Bootstrap4

app = Flask(__name__)

# set config
app_settings = os.getenv("APP_SETTINGS")
app.config.from_object(app_settings)

# set up extensions
Bootstrap4(app)


@app.route("/", methods=["GET"])
def home():
    return render_template("main/home.html")


@app.route("/tasks", methods=["POST"])
def run_task():
    task_type = request.form["type"]
    with Connection(redis.from_url("redis://127.0.0.1:6379/0")):
        q = Queue()
        task = q.enqueue(create_task, task_type) #添加任务
    response_object = {
        "status": "success",
        "data": {
            "task_id": task.get_id()
        }
    }
    return jsonify(response_object), 202


#查询任务的状态
@app.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    with Connection(redis.from_url("redis://127.0.0.1:6379/0")):
        q = Queue()
        task = q.fetch_job(task_id)
    if task:
        response_object = {
            "status": "success",
            "data": {
                "task_id": task.get_id(),
                "task_status": task.get_status(),
                "task_result": task.result,
            },
        }
    else:
        response_object = {"status": "error"}
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
