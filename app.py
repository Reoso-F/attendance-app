from flask import Flask, render_template, request, redirect
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
        SELECT s.name, s.classroom, a.reason, a.document_submitted
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id AND a.date = ?
        ORDER BY s.classroom, s.name
    """, (selected_date,))
    records = cur.fetchall()
    return render_template('index.html', records=records, selected_date=selected_date)

if __name__ == '__main__':
    app.run(debug=True)