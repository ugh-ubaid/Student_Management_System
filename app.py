from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="student_management"
    )

# Home Page - Add & List Students
@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template("index.html", students=students)

# Add Student
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    roll_no = request.form['roll_no']
    course = request.form['course']
    email = request.form['email']
    phone = request.form['phone']

    if not name or not roll_no:
        return "Name and Roll No are required!"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, roll_no, course, email, phone) VALUES (%s, %s, %s, %s, %s)",
        (name, roll_no, course, email, phone)
    )
    conn.commit()
    conn.close()
    return redirect('/')

# Edit Student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']
        course = request.form['course']
        email = request.form['email']
        phone = request.form['phone']
        cursor.execute(
            "UPDATE students SET name=%s, roll_no=%s, course=%s, email=%s, phone=%s WHERE id=%s",
            (name, roll_no, course, email, phone, id)
        )
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
        student = cursor.fetchone()
        conn.close()
        return render_template("edit.html", student=student)

# Delete Student
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# View Student Details
@app.route('/view/<int:id>')
def view(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cursor.fetchone()
    conn.close()
    return render_template("view.html", student=student)

# All Students Table
@app.route('/students')
def students_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template("students.html", students=students)

# Dashboard - Stats
@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT course, COUNT(*) FROM students GROUP BY course")
    course_stats = cursor.fetchall()
    conn.close()
    return render_template("dashboard.html", total_students=total_students, course_stats=course_stats)

if __name__ == '__main__':
    app.run(debug=True)
