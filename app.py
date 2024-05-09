from flask import Flask
from flask_cors import CORS

from flask_restx import Api

from db import init_db
from v1.api import blueprint as api_v1
from v2.api import blueprint as api_v2

app = Flask(__name__)
CORS(app, origins=["*"])

api = Api(
    app,
    version="1.0",
    title="My API",
    description="A simple Flask API"
)

app.register_blueprint(api_v1, url_prefix="/api/v1")
app.register_blueprint(api_v2, url_prefix="/api/v2")


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=9000)
