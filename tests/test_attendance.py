import pytest
from flask import Flask
from views.attendance import attendance_bp
from models.db import init_db
import sqlite3
import tempfile
import os


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["DB"] = db_path

    app.register_blueprint(attendance_bp)

    def get_test_db():
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    import models.db

    models.db.get_db = get_test_db

    with app.app_context():
        init_db(app, schema_path="schema.sql")

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


def test_today_page(client):
    response = client.get("/today")
    assert response.status_code == 200
    assert "今日" in response.get_data(as_text=True)


def test_other_date_page(client):
    response = client.get("/other-date?date=2025-03-28")
    assert response.status_code == 200
    assert "2025年3月28日" in response.data
