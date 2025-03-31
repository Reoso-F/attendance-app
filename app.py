from flask import Flask
from views import register_blueprints


def create_app():
    app = Flask(__name__)
    app.config["DB"] = "db.sqlite3"

    register_blueprints(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
