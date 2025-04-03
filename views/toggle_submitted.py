from flask import Blueprint, request, redirect, url_for
from models.db import get_db

toggle_bp = Blueprint("toggle", __name__)


@toggle_bp.route("/toggle-submitted", methods=["POST"])
def toggle_submitted():
    student_id = request.form["student_id"]
    selected_date = request.form["date"]
    submitted = 1 if "submitted" in request.form else 0
    return_to = request.form.get('from')

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO attendance (student_id, date, reason, document_submitted)
        VALUES (?, ?, '', ?)
        ON CONFLICT(student_id, date)
        DO UPDATE SET document_submitted = ?
    """,
        (student_id, selected_date, submitted, submitted),
    )
    conn.commit()

    endpoint_map = {
        'today.today': url_for(
            'today.today',
            date=selected_date,
        ),
        'other_date.other_date': url_for('other_date.other_date', date=selected_date),
        'undelivered.undelivered': url_for('undelivered.undelivered'),
    }

    return redirect(
        endpoint_map.get(
            return_to, url_for('other_date.other_date', date=selected_date)
        )
    )
