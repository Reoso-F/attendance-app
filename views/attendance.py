from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3
from datetime import date
from models.db import get_db
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance')


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
