from flask import Blueprint, render_template
from models.db import get_db
from datetime import datetime

undelivered_bp = Blueprint("undelivered", __name__)


@undelivered_bp.route("/undelivered")
def undelivered():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.id AS student_id, s.name, s.classroom,
               a.reason, a.document_submitted, a.date
        FROM students s
        JOIN attendance a ON s.id = a.student_id
        WHERE a.document_submitted = 0
              AND a.reason IS NOT NULL AND TRIM(a.reason) != ''
              AND DATE(a.date) < DATE('now')
        ORDER BY s.classroom, a.date
    """
    )
    rows = cur.fetchall()

    records = []
    for r in rows:
        record = dict(r)
        date_val = record["date"]
        if isinstance(date_val, str):
            dt = datetime.strptime(date_val, "%Y-%m-%d").date()
        else:
            dt = date_val
        record["formatted_date"] = dt.strftime("%Y年%m月%d日")
        records.append(record)

    return render_template("undelivered.html", records=records)
