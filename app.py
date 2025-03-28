from flask import Flask
from models.db import get_db
from views.write import write_bp
from views.attendance import attendance_bp

app = Flask(__name__)

app.register_blueprint(write_bp)
app.register_blueprint(attendance_bp)

if __name__ == '__main__':
    app.run(debug=True)
