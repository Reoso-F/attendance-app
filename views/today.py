from flask import Blueprint, render_template
from datetime import date
from models.db import get_db

today_bp = Blueprint("today", __name__)


@today_bp.route("/today")
def today():
    raw_date = date.today()
    selected_date = raw_date.isoformat()
    formatted_date = raw_date.strftime("%Y年%m月%d日(%a)")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.id AS student_id, s.name, s.classroom,
               a.reason, a.document_submitted
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id AND a.date = ?
        ORDER BY s.classroom, s.name
        """, (selected_date,)
    )
    records = cur.fetchall()

    return render_template(
        "today.html",
        selected_date=selected_date,
        formatted_date=formatted_date,
        records=records,
    )
