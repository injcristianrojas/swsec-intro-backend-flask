import sqlite3
from flask import Blueprint, jsonify
from db import connect_db

api_v1 = Blueprint('simple_page', __name__)

@api_v1.route("/api/v2/messages")
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