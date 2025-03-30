from flask import Blueprint, render_template, request
from models.db import get_db

range_bp = Blueprint('range', __name__)

@range_bp.route('/range', methods=['GET'])
def range_view():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    records = []

    if start_date and end_date:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.name, s.classroom, a.reason, a.date, a.document_submitted
            FROM students s
            JOIN attendance a ON s.id = a.student_id
            WHERE a.date BETWEEN ? AND ?
            ORDER BY s.classroom, a.date, s.name
        """, (start_date, end_date))
        records = cur.fetchall()

    return render_template(
        'range.html',
        start_date=start_date,
        end_date=end_date,
        records=records
    )
