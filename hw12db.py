import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

with open('schema.sql', 'r') as schema_file:
    cursor.executescript(schema_file.read())

    cursor.execute("""
    INSERT INTO students (student_id, student_first_name, student_last_name)
    VALUES (1, 'John', 'Smith')
    """);

    cursor.execute("""
    INSERT INTO quizzes (quiz_id, quiz_subject, quiz_question_count, quiz_date)
    VALUES (1, 'Python Basics', '5', 'February, 5th, 2015')
    """);

    cursor.execute("""
    INSERT INTO results (student_id, quiz_id, quiz_score)
    VALUES (1, 1, 85)
    """);

conn.commit()
conn.close()