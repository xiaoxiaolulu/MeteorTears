from flask import abort, jsonify, Flask, request, Response, make_response
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)


tasks = {
    "data": {
        "loginName": "admin",
        "roles": 1,
        "permissions": 1,
        "active": 1
    },
    "stateCode": {
        "code": 0,
        "desc": "成功"
    },
    "statusText": "成功",
    "timestamp": "1500531770453",
    "success": 1
}


@app.route("/task", methods=['GET'])
def get_all_task():
    return jsonify(tasks)


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8989,
        debug=True
    )
