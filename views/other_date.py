from flask import Blueprint, render_template, request
from datetime import date
from models.db import get_db

other_date_bp = Blueprint("other_date", __name__)


@other_date_bp.route("/other-date")
def other_date():
    raw_date = request.args.get("date")
    if not raw_date:
        raw_date = date.today().isoformat()

    parsed_date = date.fromisoformat(raw_date)
    formatted_date = parsed_date.strftime("%Y年%m月%d日(%a)")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT s.id AS student_id, s.name, s.classroom,
               a.reason, a.document_submitted
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id AND a.date = ?
        ORDER BY s.classroom, s.name
    """,
        (raw_date,),
    )
    records = cur.fetchall()

    return render_template(
        "other_date.html",
        selected_date=raw_date,
        formatted_date=formatted_date,
        records=records,
    )
