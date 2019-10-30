import sqlite3
from sqlite3 import Error


def convert_tuple(tup):
    str = ''.join(tup)
    return str


# Database Connection
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """

    print("Creating a connection to the database")
    conn = None
    try:
        print("Connection Created!")
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


# Creates tables in the database
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


# Create a Attendance Record
def create_attend(conn, face_attend):
    """
        Create a new record  into the students table
        :param conn:
        :param face_attend:
        :return: table id
        """
    sql = ''' INSERT INTO attendance(attendance_id,report_id,student_number,confidence, date_attended)
                  VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, face_attend)
    return cur.lastrowid


# Create a Report Record
def create_report(conn, face_report):
    """
        Create a new record  into the students table
        :param conn:
        :param face_report:
        :return: table id
        """
    sql = ''' INSERT INTO report(report_id,identified,date_attended)
                  VALUES(?,?,?) '''
    print("Report " + sql)
    cur = conn.cursor()
    cur.execute(sql, face_report)
    return cur.lastrowid


# Create a Student Record
def create_student(conn, student_data):
    """
        Create a new record  into the students table
        :param conn:
        :param student_data:
        :return: table id
        """
    try:
        sql = ''' INSERT INTO students(student_number, first_name, surname, file_name)
                      VALUES(?,?,?,?) '''

        cur = conn.cursor()
        cur.execute(sql, student_data)
    except Error as e:
        print(e)
    return cur.lastrowid


# Select all Students in the Database
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


# Select all records from Table Attendances
def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM attendance")

    rows = cur.fetchall()
    for row in rows:
        print(row)


# Select All Records from Table Reports
def select_all_report(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM report")

    rows = cur.fetchall()

    for row in rows:
        print(row)


# Creates the Json Statement to return to main Server
def create_the_statement(conn, report_num):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :param report_num: the identifier
    :return:
    """
    student_number = []
    att_confidence = []
    identified = []
    cur = conn.cursor()
    cur.execute("SELECT student_number FROM attendance WHERE report_id =" + report_num)
    students = cur.fetchall()

    for student in students:
        stud = convert_tuple(student)
        student_number.append(stud)

    print(student_number)

    cur.execute("SELECT confidence FROM attendance WHERE report_id =" + report_num)
    confidence = cur.fetchall()

    for con in confidence:
        conf = convert_tuple(con)
        att_confidence.append(conf)

    print(att_confidence)

    counter = 0
    for person in student_number:
        the_records = {
            "person_id": person,
            "certainty": att_confidence[counter]
        }
        identified.append(the_records)
        counter = counter +1

    report_config = {
        "type": "face_rec_details",
        "identified": identified
    }

    return report_config


