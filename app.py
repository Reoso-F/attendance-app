from flask import Flask
from models.db import get_db
from views.write import write_bp
from views.attendance import attendance_bp

def create_app():
    app = Flask(__name__)
    app.config['DB'] = 'db.sqlite3'

    app.register_blueprint(write_bp)
    app.register_blueprint(attendance_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
