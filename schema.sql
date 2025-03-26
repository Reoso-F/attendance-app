CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    classroom TEXT NOT NULL
);

CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    date TEXT,
    reason TEXT,
    document_submitted INTEGER DEFAULT 0,
    UNIQUE(student_id, date),
    FOREIGN KEY (student_id) REFERENCES students(id)
);