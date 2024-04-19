import datetime
from flask import Blueprint, jsonify, request
from db import connect_db
import jwt

api = Blueprint("APIv2", __name__)

SECRET_KEY = "12345"
ALGORITHM = "HS256"

@api.route("/messages")
def messages():
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


@api.route("/auth", methods = ['POST'])
def authenticate():
    data = request.form
    username = data.get("username")
    password = data.get("password")
    if True:
        payload = {
            "username": username,
            "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return jsonify({"token": token})
    return jsonify({"message": "Invalid credentials"}), 401
