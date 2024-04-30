from flask import Blueprint, jsonify, request
from db import connect_db

api = Blueprint('APIv1', __name__)

@api.route("/messages")
def messages():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages")
    results = cur.fetchall()
    conn.close()

    json_results = []
    for row in results:
        json_results.append({'id': row[0], 'message': row[1]})
    
    return jsonify(json_results)

@api.route("/messages/add", methods = ['POST'])
def post_message():
    message = request.get_json().get('message')
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO messages(message) VALUES ('" + message + "')");
    conn.commit()
    conn.close()

    return jsonify([{'status': 'OK'}])

@api.route("/users/type/<id>")
def get_users_by_type(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_type = " + id)
    results = cur.fetchall()
    conn.close()

    json_results = []
    for row in results:
        json_results.append({'id': row[0], 'username': row[1], 'password': row[2]})
    
    return jsonify(json_results)