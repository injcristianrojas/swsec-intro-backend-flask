from flask import Blueprint, jsonify, request
from flask_restx import Api, Resource, fields
from db import connect_db

blueprint = Blueprint("api_v1", __name__)
api = Api(
    blueprint,
    version="1.0",
    title="My API v1",
    description="A simple Flask API",
    doc="/swaggerui",
)

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
    @api.doc(body=api.model("Message Data", {"message": fields.String}))
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
