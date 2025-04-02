from flask import Blueprint, render_template, request, redirect, url_for
from models.db import get_db

edit_bp = Blueprint("edit", __name__)


@edit_bp.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    selected_date = request.args.get("date")
    if not selected_date:
        return "日付が指定されていません", 400

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        reason = request.form["reason"]
        submitted = 1 if "submitted" in request.form else 0

        cur.execute(
            """
            INSERT INTO attendance (student_id, date, reason, document_submitted)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(student_id, date)
            DO UPDATE SET reason=excluded.reason,
                          document_submitted=excluded.document_submitted
        """,
            (student_id, selected_date, reason, submitted),
        )
        conn.commit()

        return_to = request.args.get("from_page", "other_date.other_date")
        return redirect(url_for(f"attendance.{return_to}", date=selected_date))

    cur.execute(
        """
        SELECT s.name, s.classroom, a.reason, a.document_submitted
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id AND a.date = ?
        WHERE s.id = ?
    """,
        (selected_date, student_id),
    )
    record = cur.fetchone()

    if not record:
        return "対象の生徒が見つかりません", 404

    return render_template(
        "edit.html",
        record=record,
        student_id=student_id,
        selected_date=selected_date,
        return_to=request.args.get("from", "other_date.other_date"),
    )
