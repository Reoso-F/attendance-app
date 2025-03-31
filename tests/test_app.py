from flask import Flask, url_for


def test_url_for_edit():
    app = Flask(__name__)
    app.config["SERVER_NAME"] = "localhost"

    @app.route("/edit/<int:student_id>")
    def edit(student_id):
        return f"Edit {student_id}"

    with app.test_request_context():
        result = url_for("edit", student_id=1, date="2025-03-28", _external=False)
        assert result == "/edit/1?date=2025-03-28"
