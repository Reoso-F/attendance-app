from flask import Blueprint

from .write import write_bp
from .attendance import attendance_bp
from .today import today_bp
from .other_date import other_date_bp
from .edit import edit_bp
from .range_view import range_bp
from .undelivered import undelivered_bp


def register_blueprints(app):
    app.register_blueprint(write_bp)
    app.register_blueprint(today_bp)
    app.register_blueprint(other_date_bp)
    app.register_blueprint(edit_bp)
    app.register_blueprint(range_bp)
    app.register_blueprint(undelivered_bp)
