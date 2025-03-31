import sqlite3
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DB"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app, schema_path="schema.sql"):
    with app.app_context():
        db = get_db()
        with open(schema_path, "r", encoding="utf-8") as f:
            db.executescript(f.read())
