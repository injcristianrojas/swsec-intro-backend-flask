import datetime
import jwt
from flask import Blueprint, jsonify, request
from db import connect_db
from functools import wraps

api = Blueprint("APIv2", __name__)

SECRET_KEY = "123"
ALGORITHM = "HS256"

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            current_user = data["username"]
        except:
            return jsonify({"message": "Token is invalid"}), 401
        return f(current_user, *args, **kwargs)
    return decorated_function


def get_user_data(username, password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username = '"
        + username
        + "' AND password = '"
        + password
        + "'"
    )
    results = cur.fetchall()
    conn.close()
    if len(results) == 0:
        return None
    return {"username": results[0][1], "type": results[0][3]}


@api.route("/login", methods=["POST"])
def authenticate():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    user_data = get_user_data(username, password)
    if user_data is None:
        return jsonify({"message": "Invalid credentials"}), 401
    payload = {
        "username": user_data["username"],
        "type": user_data["type"],
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=6),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return jsonify({"token": token})


@api.route("/messages")
@token_required
def messages(_):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages")
    results = cur.fetchall()
    conn.close()

    json_results = []
    for row in results:
        json_results.append({"id": row[0], "message": row[1]})

    return jsonify(json_results)


@api.route("/users/type/<id>")
def get_users_by_type(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_type = " + id)
    results = cur.fetchall()
    conn.close()

    json_results = []
    for row in results:
        json_results.append({"id": row[0], "username": row[1]})

    return jsonify(json_results)
