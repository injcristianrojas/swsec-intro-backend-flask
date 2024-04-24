from flask import Flask
from flask_cors import CORS

from db import init_db
from v1.api import api as api_v1
from v2.api import api as api_v2

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])

app.register_blueprint(api_v1, url_prefix='/api/v1')
app.register_blueprint(api_v2, url_prefix='/api/v2')

if __name__ == "__main__":
    init_db()
    app.run(port=9000)
