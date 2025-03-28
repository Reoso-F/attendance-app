import tempfile
import os
import pytest
import sqlite3
from flask import Flask, url_for
from models.db import get_db, init_db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = Flask(__name__)
    app.config['DB'] = db_path
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema.sql')
    init_db(app, schema_path=schema_path)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


def test_get_db(app):
    with app.app_context():
        db = get_db()
        assert isinstance(db, sqlite3.Connection)


def test_url_for_edit():
    app = Flask(__name__)
    app.config['SERVER_NAME'] = 'localhost'

    @app.route('/edit/<int:student_id>')
    def edit(student_id):
        return f"Edit {student_id}"

    with app.test_request_context():
        result = url_for('edit',
                         student_id=1,
                         date='2025-03-28',
                         _external=False)
        assert result == '/edit/1?date=2025-03-28'
