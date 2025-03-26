from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)
DB = 'db.sqlite3'


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    selected_date = request.args.get('date', date.today().isoformat())
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    SELECT s.id AS student_id, s.name, s.classroom,
                a.reason, a.document_submitted
    FROM students s
    LEFT JOIN attendance a ON s.id = a.student_id AND a.date = ?
    ORDER BY s.classroom, s.name
""", (selected_date,))
    # records = cur.fetchall()
    # ダミーデータ（DBがまだ空でも表示できるように）
    records = [
        {'name': '田中 太郎', 'classroom': 'A',
         'reason': '', 'document_submitted': 0},
        {'name': '山田 花子', 'classroom': 'B',
         'reason': '体調不良', 'document_submitted': 1},
    ]
    return render_template('index.html',
                           records=records,
                           selected_date=selected_date)


@app.route('/delete', methods=['POST'])
def delete():
    student_id = request.form['student_id']
    selected_date = request.form['date']

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM attendance WHERE student_id = ? AND date = ?
    """, (student_id, selected_date))
    conn.commit()

    return redirect(url_for('other_date', date=selected_date))


@app.route('/write')
def write():
    return render_template('write.html')


@app.route('/today')
def today():
    return render_template('today.html')


@app.route('/other-date', methods=['GET'])
def other_date():
    selected_date = request.args.get('date', date.today().isoformat())
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
       SELECT s.id AS student_id, s.name, s.classroom,
                a.reason, a.document_submitted
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id AND a.date = ?
        ORDER BY s.classroom, s.name
    """, (selected_date,))
    records = cur.fetchall()
    return render_template('other_date.html',
                           records=records, selected_date=selected_date)


@app.route('/toggle-submitted', methods=['POST'])
def toggle_submitted():
    student_id = request.form['student_id']
    date_val = request.form['date']
    submitted = 1 if 'submitted' in request.form else 0

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO attendance (student_id, date, reason, document_submitted)
        VALUES (?, ?, '', ?)
        ON CONFLICT(student_id, date)
        DO UPDATE SET document_submitted = ?
    """, (student_id, date_val, submitted, submitted))
    conn.commit()

    return redirect(url_for('other_date', date=date_val))


@app.route('/undelivered')
def undelivered():
    return render_template('undelivered.html')


@app.route('/range')
def range_view():
    return render_template('range.html')


@app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit(student_id):
    selected_date = request.args.get('date')
    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        reason = request.form['reason']
        submitted = 1 if 'submitted' in request.form else 0

        cur.execute("""
            INSERT INTO attendance (student_id, date, reason,
                    document_submitted)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(student_id, date)
            DO UPDATE SET reason=excluded.reason,
                    document_submitted=excluded.document_submitted
        """, (student_id, selected_date, reason, submitted))

        conn.commit()
        return redirect(url_for('index', date=selected_date))

    # GETメソッドの場合：現在の値を取得してフォームに表示
    cur.execute("""
        SELECT s.name, s.classroom, a.reason, a.document_submitted
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id AND a.date = ?
        WHERE s.id = ?
    """, (selected_date, student_id))
    record = cur.fetchone()
    return render_template(
        'edit.html',
        record=record,
        student_id=student_id,
        selected_date=selected_date,
        return_to=request.args.get('from', 'index'))


if __name__ == '__main__':
    app.run(debug=True)
