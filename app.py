from flask import Flask, jsonify
from flask_cors import CORS

from flask_restx import Api

from db import init_db
from v1.api import blueprint as api_v1
from v2.api import blueprint as api_v2

import subprocess

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

@app.route('/healthcheck', defaults={'file': 'healthcheck'})
@app.route('/healthcheck/<string:file>')
def healthcheck(file):
    data = subprocess.check_output('cat %s' % file, shell=True, text=True)
    return jsonify([{"status": data}])

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=9000)
