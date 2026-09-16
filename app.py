from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# Create database
def init_db():
    conn = sqlite3.connect("students.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Home page - Read students
@app.route("/")
def index():

    conn = sqlite3.connect("students.db")

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        students=students
    )


# Add student - Create
@app.route("/add", methods=["POST"])
def add_student():

    name = request.form["name"]
    email = request.form["email"]
    course = request.form["course"]
    age = request.form["age"]

    conn = sqlite3.connect("students.db")

    conn.execute("""
        INSERT INTO students
        (name, email, course, age)
        VALUES (?, ?, ?, ?)
    """, (name, email, course, age))

    conn.commit()
    conn.close()

    return redirect("/")


# Delete student - Delete
@app.route("/delete/<int:id>")
def delete_student(id):

    conn = sqlite3.connect("students.db")

    conn.execute(
        "DELETE FROM students WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# Edit student page
@app.route("/edit/<int:id>")
def edit_student(id):

    conn = sqlite3.connect("students.db")

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        "index.html",
        edit_student=student,
        students=[]
    )


# Update student - Update
@app.route("/update/<int:id>", methods=["POST"])
def update_student(id):

    name = request.form["name"]
    email = request.form["email"]
    course = request.form["course"]
    age = request.form["age"]

    conn = sqlite3.connect("students.db")

    conn.execute("""
        UPDATE students
        SET name = ?, email = ?, course = ?, age = ?
        WHERE id = ?
    """, (name, email, course, age, id))

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":

    init_db()

    app.run(debug=True)