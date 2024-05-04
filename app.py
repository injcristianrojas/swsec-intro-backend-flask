from flask import Flask, jsonify, request
from flask_cors import CORS

from flask_restx import Api, Resource, fields

from db import init_db, connect_db
from v1.api import api as api_v1
from v2.api import api as api_v2

app = Flask(__name__)
CORS(app, origins=["*"])

api = Api(
    app,
    version="1.0",
    title="My API",
    description="A simple Flask API",
    doc="/swaggerui",
)

app.register_blueprint(api_v1, url_prefix="/api/v1")
app.register_blueprint(api_v2, url_prefix="/api/v2")


@api.route("/messages")
class Messages(Resource):
    def get(self):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM messages")
        results = cur.fetchall()
        conn.close()

        json_results = []
        for row in results:
            json_results.append({"id": row[0], "message": row[1]})

        return jsonify(json_results)


@api.route("/messages/add")
class AddMessage(Resource):
    def post(self):
        message = request.get_json().get("message")
        print(message)
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO messages(message) VALUES ('" + message + "')")
        conn.commit()
        conn.close()

        return jsonify([{"status": "OK"}])


@api.route("/users/type/<id>")
class UsersByType(Resource):
    def get(self, id):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_type = " + id)
        results = cur.fetchall()
        conn.close()

        json_results = []
        for row in results:
            json_results.append({"id": row[0], "username": row[1], "password": row[2]})

        return jsonify(json_results)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=9000)
