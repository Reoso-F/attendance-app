from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date, datetime
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
DB = 'db.sqlite3'


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


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


@app.route('/', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        date_val = request.form['date']
        classroom = request.form['classroom']
        name = request.form['name']
        reason = request.form['reason']

        with get_db() as conn:
            cur = conn.cursor()
            # 生徒登録（仮：重複確認なし）
            cur.execute("INSERT INTO students (name, classroom) VALUES (?, ?)",
                        (name, classroom))
            student_id = cur.lastrowid

            # 欠席記録登録
            cur.execute("""
                INSERT INTO attendance (
                        student_id, date, reason, document_submitted)
                VALUES (?, ?, ?, 0)
            """, (student_id, date_val, reason))

        return redirect(url_for('other_date', date=date_val))

    return render_template('write.html')


@app.route('/today')
def today():
    raw_date = date.today()
    selected_date = raw_date.isoformat()
    # 「2025年03月27日（木）」形式
    formatted_date = raw_date.strftime('%Y年%m月%d日（%a）')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.id as student_id, s.name,
                s.classroom, a.reason, a.document_submitted
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


@app.route('/other-date')
def other_date():
    raw_date = request.args.get('date')
    if not raw_date:
        raw_date = date.today().isoformat()

    # 曜日つき日付の整形
    parsed_date = date.fromisoformat(raw_date)
    formatted_date = parsed_date.strftime('%Y年%m月%d日（%a）')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.id as student_id, s.name, s.classroom,
                a.reason, a.document_submitted
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


@app.route('/toggle-submitted', methods=['POST'])
def toggle_submitted():
    student_id = request.form['student_id']
    date_val = request.form['date']
    submitted = 1 if 'submitted' in request.form else 0
    return_to = request.form.get('from', 'other_date')

    logging.info(
        "[Toggle] student_id=%s,date=$s,submitted=%s",
        student_id, date_val, submitted
        )

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


@app.route('/undelivered')
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

    # Rowオブジェクトを辞書に変換してから加工
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

    return render_template('undelivered.html', records=records)


@app.route('/range', methods=['GET'])
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
        return redirect(url_for('other_date', date=selected_date))

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
