from flask import Blueprint, request, redirect, url_for
from models.db import get_db

delete_bp = Blueprint("delete", __name__)


@delete_bp.route("/delete", methods=["POST"])
def delete():
    student_id = request.form["student_id"]
    selected_date = request.form["date"]

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
    DELETE FROM attendance WHERE student_id = ? AND date = ?
    """,
        (student_id, selected_date),
    )
    conn.commit()

    return redirect(url_for("attendance.other_date", date=selected_date))
