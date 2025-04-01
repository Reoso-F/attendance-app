from flask import Blueprint, request, redirect, url_for
from models.db import get_db

toggle_bp = Blueprint("toggle", __name__)


@toggle_bp.route("/toggle-submitted", methods=["POST"])
def toggle_submitted():
    student_id = request.form["student_id"]
    date_val = request.form["date"]
    submitted = 1 if "submitted" in request.form else 0
    next_url = request.form.get('next')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO attendance (student_id, date, reason, document_submitted)
        VALUES (?, ?, '', ?)
        ON CONFLICT(student_id, date)
        DO UPDATE SET document_submitted = ?
    """, (student_id, date_val, submitted, submitted)
    )
    conn.commit()

    return redirect(next_url or
                    url_for('other_date.other_date', date=date_val))
