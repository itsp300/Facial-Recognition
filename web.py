import os
import sqlite3
from sqlite3 import Error
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'faces'
ALLOWED_EXTENSIONS = set(['jpg', 'png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
database = "faceStudent.db"


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Database Connection
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


# Create a Student Record
def create_student(conn, faceStudent):
    """
        Create a new record  into the students table
        :param conn:
        :param faceStudent:
        :return: table id
        """
    sql = ''' INSERT INTO students(student_number, first_name, surname, file_name)
                  VALUES(?,?,?,?) '''

    cur = conn.cursor()
    cur.execute(sql, faceStudent)
    return cur.lastrowid


def select_all_students(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")

    rows = cur.fetchall()
    print("Students in Database")
    for row in rows:
        print(row)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has a file part
        name = request.form.get('firstName')
        surname = request.form.get('surname')
        student_number = request.form.get('number')

        if 'file' not in request.files:
            flash('No file Part')
            return render_template("index.html")
        file = request.files['file']
        # if user does not select a file, browser also
        # submit an empty part without a filename
        if file.filename == '':
            flash('No file Selected')
            return render_template("index.html", message="No file Selected")
        if file and allowed_file(file.filename):
            # create a database connection
            conn = create_connection(database)
            the_file_name = student_number + ".jpg"

            with conn:
                student_data = (student_number, name, surname, the_file_name)
                create_student(conn, student_data)
                select_all_students(conn)

            conn.close()

            filename = secure_filename(the_file_name)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file', filename=filename))
    return render_template("index.html")
