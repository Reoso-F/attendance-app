from flask import Blueprint, render_template, request, redirect, url_for
from models.db import get_db

write_bp = Blueprint("write", __name__)


@write_bp.route("/", methods=["GET", "POST"])
def write():
    if request.method == "POST":
        date_val = request.form["date"]
        classroom = request.form["classroom"]
        name = request.form["name"]
        reason = request.form["reason"]

        with get_db() as conn:
            cur = conn.cursor()
            # 生徒登録（仮：重複確認なし）
            cur.execute(
                "INSERT INTO students (name, classroom) VALUES (?, ?)",
                (name, classroom),
            )
            student_id = cur.lastrowid
            # 欠席記録登録
            cur.execute(
                """
                INSERT INTO attendance (
                        student_id, date, reason, document_submitted)
                VALUES (?, ?, ?, 0)
            """,
                (student_id, date_val, reason),
            )

        next_url = request.form.get("next")
        return redirect(next_url or url_for('write.write', date=date_val))

    return render_template("write.html")
