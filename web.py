import os
import Database
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
            conn = Database.create_connection(database)
            the_file_name = student_number + ".jpg"

            with conn:
                student_data = (student_number, name, surname, the_file_name)
                Database.create_student(conn, student_data)
                Database.select_all_students(conn)

            conn.close()

            filename = secure_filename(the_file_name)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file', filename=filename))
    return render_template("index.html")
