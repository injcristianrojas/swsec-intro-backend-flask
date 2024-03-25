from flask import Flask

from db import init_db
from v1.api import api_v1

app = Flask(__name__)
app.register_blueprint(api_v1)

if __name__ == "__main__":
    init_db()
    app.run(port=9000)
