import os
import sqlite3
import tempfile
import pytest
from flask import Flask
from models.db import init_db, get_db
from views.write import write_bp


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["DB"] = db_path

    app.register_blueprint(write_bp)

    # Replace the DB path used by get_db() with a temporary file
    def get_test_db():
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # Replace like a monkey patch
    import models.db

    models.db.get_db = get_test_db

    with app.app_context():
        init_db(app, schema_path="schema.sql")

    yield app

    os.close(db_fd)
    os.unlink(db_path)  # Delete after testing


@pytest.fixture
def client(app):
    return app.test_client()


def test_write_post(client):
    # Send student and attendance information via POST
    response = client.post(
        "/",
        data={
            "date": "2025-03-28",
            "classroom": "第1教室",
            "name": "テスト太郎",
            "reason": "体調不良",
        },
    )

    # Verify that the redirect was successful
    assert response.status_code == 302
    assert "/other-date?date=2025-03-28" in response.headers["Location"]

    # DBの中身をチェック
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE name = ?", ("テスト太郎",))
        student = cur.fetchone()
        assert student is not None

        cur.execute("SELECT * FROM attendance WHERE student_id = ?", (student["id"],))
        attendance = cur.fetchone()
        assert attendance is not None
        assert attendance["reason"] == "体調不良"
