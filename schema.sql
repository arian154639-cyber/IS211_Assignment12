DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS quizzes;
DROP TABLE IF EXISTS results; 

CREATE TABLE students (
student_id INTEGER PRIMARY KEY,
student_first_name TEXT,
student_last_name TEXT);

CREATE TABLE quizzes (
quiz_id INTEGER PRIMARY KEY,
quiz_subject TEXT,
quiz_question_count INTEGER,
quiz_date TEXT
);

CREATE TABLE results (
student_id INTEGER,
quiz_id INTEGER,
quiz_score INTEGER
);

