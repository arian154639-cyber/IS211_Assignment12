"""
Note to Professor: I refactored the code after reconsidering the offer to resubmit. As per the
instructions, the username is admin and the password is password. You need to run hw12db.py first
to create the database. I sent two emails about assignments 10 and 12.

I aimed to keep the code readable for this assignment, using two of the tutorials from the readings.
I only implemented sessions into the dashboard because all other features are only accessed from there.
The input validation is minimal, it only checks for empty fields. This was due to time constraints. I
did not use the triple quote style from hw12db.py for brevity. There's still few things I didn't handle
such as type conversion due to time constraints.
"""

from flask import Flask, render_template, redirect, session, request, g
import sqlite3

app = Flask(__name__)

app.secret_key = '7a1aac9b364a1eb17261ac27e2ff1470d245dfd506131ee7efba1b7a7cce0f3d' 

DATABASE = 'hw12.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def main_controller():
    return redirect('/login')

def valid_login(username, password):
    return username == 'admin' and password == 'password'

@app.route('/login', methods=['GET', 'POST'])
def login_controller():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if valid_login(username, password):
            session['username'] = username
            return redirect('/dashboard')
        else:
            error = 'Invalid username/password.'

    return render_template('login_form.html', error=error)

@app.route('/dashboard')
def dashboard_controller():
    if 'username' not in session:
        return redirect('/login')

    db = get_db()

    students = db.execute('SELECT * FROM students').fetchall()
    quizzes = db.execute('SELECT * FROM quizzes').fetchall()

    return render_template('dashboard_page.html', students=students, quizzes=quizzes)

@app.route('/student/add', methods=['GET', 'POST'])
def add_student_controller():
    if request.method == 'POST':
        student_first_name = request.form['student_first_name']
        student_last_name = request.form['student_last_name']
        error = None

        if not student_first_name or not student_last_name:
            error = 'Required field is empty.'

        if error:
            return render_template('add_student_page.html', error=error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO students (student_first_name, student_last_name) VALUES (?, ?)',
                (student_first_name, student_last_name)
            )

            db.commit()

            return redirect('/dashboard')

    return render_template('add_student_page.html')

@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz_controller():
    if request.method == 'POST':
        quiz_subject = request.form['quiz_subject']
        quiz_question_count = request.form['quiz_question_count']
        quiz_date = request.form['quiz_date']
        error = None

        if not quiz_subject or not quiz_question_count or not quiz_date:
            error = 'Required field is empty.'

        if error:
            return render_template('add_quiz_page.html', error=error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO quizzes (quiz_subject, quiz_question_count, quiz_date) VALUES (?, ?, ?)',
                (quiz_subject, quiz_question_count, quiz_date)
            )

            db.commit()

            return redirect('/dashboard')

    return render_template('add_quiz_page.html')

@app.route('/student/<int:student_id>')
def view_results_controller(student_id):
    db = get_db()

    student = db.execute('SELECT * FROM students WHERE student_id = ?', (student_id,)).fetchone()
    
    results = db.execute('SELECT * FROM results WHERE student_id = ?', (student_id,)).fetchall()

    if not results:
        message = 'No results.'
    else:
        message = None

    return render_template('student_results_page.html', student=student, results=results, message=message)

@app.route('/results/add', methods=['GET', 'POST'])
def add_results_controller():
    db = get_db()
    error = None

    if request.method == 'POST':
        student_id = request.form['student_id']
        quiz_id = request.form['quiz_id']
        quiz_score = request.form['quiz_score']

        if not student_id or not quiz_id or not quiz_score:
            error = 'Required field is empty.'
        else:
            db.execute(
                'INSERT INTO results (student_id, quiz_id, quiz_score) VALUES (?, ?, ?)', 
                (student_id, quiz_id, quiz_score)
            )
            
            db.commit()

            return redirect('/dashboard')

    students = db.execute('SELECT * FROM students').fetchall()
    quizzes = db.execute('SELECT * FROM quizzes').fetchall()

    return render_template('add_results_page.html', students=students, quizzes=quizzes, error=error)

if __name__ == '__main__':
    app.run()