import json
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

def connect_db():
    return sqlite3.connect("db.sqlite")

def init_db():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS messages");
    cur.execute("DROP TABLE IF EXISTS users");

    cur.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY NOT NULL, message TEXT NOT NULL)");
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY NOT NULL, username VARCHAR(10) NOT NULL, password VARCHAR(30) NOT NULL, user_type INTEGER NOT NULL)");

    cur.execute("INSERT INTO messages(message) VALUES ('Bienvenidos al foro de Fans de las Aves Chilenas. Soy el Administrador.')");
    cur.execute("INSERT INTO messages(message) VALUES ('Se informa que la API se encuentra deshabilitada hasta nuevo aviso.')");

    cur.execute("INSERT INTO users(username,password,user_type) VALUES ('admin', '123', 1)");
    cur.execute("INSERT INTO users(username,password,user_type) VALUES ('zorzal', 'fio', 2)");
    cur.execute("INSERT INTO users(username,password,user_type) VALUES ('chincol', 'fiofio', 2)");

    conn.commit()
    conn.close()

@app.route("/api/v2/messages")
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

if __name__ == "__main__":
    init_db()
    app.run(port=9000)
