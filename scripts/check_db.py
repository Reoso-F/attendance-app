import sqlite3

conn = sqlite3.connect("db.sqlite3")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

print("=== Students ")
for row in cur.execute("SELECT * FROM students"):
    print(dict(row))

print("\n=== Attendance ===")
for row in cur.execute("SELECT * FROM attendance"):
    print(dict(row))

conn.close()
