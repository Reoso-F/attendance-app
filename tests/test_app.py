from flask import Flask, url_for, request

app = Flask(__name__)


@app.route('/edit/<int:student_id>')
def edit(student_id):
    return f"Edit page for student {student_id} on {request.args.get('date')}"


@app.route('/test')
def test():
    return url_for('edit', student_id=1, date='2025-03-28')


if __name__ == '__main__':
    app.run()
