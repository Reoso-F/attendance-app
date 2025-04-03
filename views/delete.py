from flask import Blueprint, request, redirect, url_for
from models.db import get_db

delete_bp = Blueprint("delete", __name__)


@delete_bp.route("/delete", methods=["POST"])
def delete():
    student_id = request.form["student_id"]
    selected_date = request.form["date"]
    return_to = request.form.get('from')

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        DELETE FROM attendance WHERE student_id = ? AND date = ?
    """,
        (student_id, selected_date),
    )
    conn.commit()

    endpoint_map = {
        'today.today': url_for(
            'today.today',
            date=selected_date,
        ),
        'other_date.other_date': url_for('other_date.other_date', date=selected_date),
    }

    return redirect(
        endpoint_map.get(
            return_to, url_for('other_date.other_date', date=selected_date)
        )
    )
