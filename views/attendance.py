from flask import Blueprint, render_template, request, redirect, url_for
from datetime import date
from models.db import get_db
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance')


@attendance_bp.route('/today')
def today():
    raw_date = date.today()
    selected_date = raw_date.isoformat()
    formatted_date = raw_date.strftime('%Y年%m月%d日(%a)')

    conn = get_db()
    cur = conn.cursor()
    cur.execute(""""
        SELECT s.id AS student_id, s.name, s.classroom,
               a.reason, a.document_submitted"
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id AND a.date = ?
        ORDER BY s.classroom, s.name
        """, (selected_date,))
    records = cur.fetchall()

    return render_template(
        'today.html',
        selected_date=selected_date,
        formatted_date=formatted_date,
        records=records
    )


@attendance_bp.route('/other-date')
def other_date():
    raw_date = request.args.get('date')
    if not raw_date:
        raw_date = date.today().isoformat()

    parsed_date = date.fromisoformat(raw_date)
    formatted_date = parsed_date.strftime('%Y年%m月%d日(%a)')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.id AS student_id, s.name, s.classroom,
               a.reason, a.document_submitted"
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id AND a.date = ?
        ORDER BY s.classroom, s.name
    """, (raw_date,))
    records = cur.fetchall()

    return render_template(
        'other_date.html',
        selected_date=raw_date,
        formatted_date=formatted_date,
        records=records
    )


@attendance_bp.route('/toggle-submitted', methods=['POST'])
def toggle_submitted():
    student_id = request.form['student_id']
    date_val = request.form['date']
    submitted = 1 if 'submitted' in request.form else 0
    return_to = request.form.get('from', 'attendance.other_date')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO attendance (student_id, date, reason, document_submitted)
        VALUES (?, ?, '', ?)
        ON CONFLICT(student_id, date)
        DO UPDATE SET document_submitted = ?
    """, (student_id, date_val, submitted, submitted))
    conn.commit()

    return redirect(url_for(return_to, date=date_val))


@attendance_bp.route('/delete', methods=['POST'])
def delete():
    student_id = request.form['student_id']
    selected_date = request.form['date']

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    DELETE FROM attendance WHERE student_id = ? AND date = ?
    """, (student_id, selected_date))
    conn.commit()

    return redirect(url_for('attendance.other_date', date=selected_date))


@attendance_bp.route('/undelivered')
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
    """)
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

    return render_template('undeliverd.html', records=records)


@attendance_bp.route('/range', methods=['GET'])
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

    return render_template('range.html',
                           start_date=start_date,
                           end_date=end_date,
                           records=records)
