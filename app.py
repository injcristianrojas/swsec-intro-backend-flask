from flask import Flask

from db import init_db
from v2.api import api_v2

app = Flask(__name__)
app.register_blueprint(api_v2, url_prefix='/api/v2')

if __name__ == "__main__":
    init_db()
    app.run(port=9000)
