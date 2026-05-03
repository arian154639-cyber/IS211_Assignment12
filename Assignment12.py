"""
I aimed to keep the code readable for this assignment, using last week's assignment as a reference.
I implemented sessions into the script as per the instructions, but I chose not to use "g". I used 
try/except for error handling. I would have done some more polishing such as adding "placeholder" 
to the html forms if there had been more time. I did not use my triple quote style from hw12db.py 
here for brevity. There's also a few errors that I'm aware of that i would have liked to fix if 
there had been more time.
"""

from flask import Flask, render_template, redirect, session, request
import sqlite3

app = Flask(__name__)

app.secret_key = "secret_key" 

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return redirect("/login")

def valid_login(username, password):
    return username == "admin" and password == "password"

@app.route("/login", methods = ["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if valid_login(username, password):
            session["username"] = username
            return redirect("/dashboard")
        else:
            error = "Invalid username/password."

    return render_template("login_form.html", error = error)

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/login")

    conn = get_db()

    students = conn.execute("SELECT * FROM students").fetchall()
    quizzes = conn.execute("SELECT * FROM quizzes").fetchall()

    conn.close()

    return render_template("dashboard_page.html", students = students, quizzes = quizzes)

@app.route("/student/add", methods = ["GET", "POST"])
def add_student():
    if "username" not in session:
        return redirect("/login")

    if request.method == "POST":
        try:
            first_name = request.form["student_first_name"]
            last_name = request.form["student_last_name"]

            conn = get_db()
            conn.execute(
                "INSERT INTO students (student_first_name, student_last_name) VALUES (?, ?)",
                (first_name, last_name)
            )

            conn.commit()
            conn.close()

            return redirect("/dashboard")

        except Exception:
            return render_template("add_student_page.html", error = "Error. Please try again.")

    return render_template("add_student_page.html")

@app.route("/quiz/add", methods = ["GET", "POST"])
def add_quiz():
    if "username" not in session:
        return redirect("/login")

    if request.method == "POST":
        try:
            subject = request.form["quiz_subject"]
            question_count = request.form["quiz_question_count"]
            date = request.form["quiz_date"]

            conn = get_db()
            conn.execute(
                "INSERT INTO quizzes (quiz_subject, quiz_question_count, quiz_date) VALUES (?, ?, ?)",
                (subject, question_count, date)
            )

            conn.commit()
            conn.close()

            return redirect("/dashboard")

        except Exception:
            return render_template("add_quiz_page.html", error = "Error. Please try again.")

    return render_template("add_quiz_page.html")

@app.route("/student/<id>")
def view_results(id):
    if "username" not in session:
        return redirect("/login")

    conn = get_db()

    results = conn.execute("SELECT * FROM results WHERE student_id = ?", (id,)).fetchall()

    student = conn.execute("SELECT * FROM students WHERE student_id = ?", (id,)).fetchone()

    conn.close()

    if not results:
        message = "No results."
    else:
        message = None

    return render_template("student_results_page.html", results = results, student = student, message = message)

@app.route("/results/add", methods = ["GET", "POST"])
def add_results():
    if "username" not in session:
        return redirect("/login")

    try:
        conn = get_db()

        if request.method == "POST":
            student_id = request.form["student_id"]
            quiz_id = request.form["quiz_id"]
            score = request.form["quiz_score"]

            conn.execute(
                "INSERT INTO results (student_id, quiz_id, quiz_score) VALUES (?, ?, ?)",
                (student_id, quiz_id, score)
            )

            conn.commit()
            conn.close()

            return redirect("/dashboard")

        students = conn.execute("SELECT * FROM students").fetchall()
        quizzes = conn.execute("SELECT * FROM quizzes").fetchall()

        conn.close()

        return render_template("add_results_page.html", students = students, quizzes = quizzes)

    except Exception:
        return render_template("add_results_page.html", students = [], quizzes = [], error = "Error. Please try again.")

if __name__ == "__main__":
    app.run()