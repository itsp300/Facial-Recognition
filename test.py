import face_recon
import sqlite3
from sqlite3 import Error
import pickle

report_num = ""
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


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

def select_all_students(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def face_rec_detail():
    database = "faceStudent.db"
    global report_num
    report_num = "60"
    face = face_recon.classify_face('testDrive.jpg', report_num)
    print(face)

    # create a database connection
    conn = create_connection(database)
    dbCursor = conn.cursor()
    dbCursor.execute("SELECT * FROM attendance where report_id = 3")
    row = dbCursor.fetchone()
    rowDict = dict(zip([c[0] for c in dbCursor.description], row))

    print(rowDict)

    with conn:
        print("Selecting all Attendance Data")
        select_all_tasks(conn)
        print("-----------------------------------")
        print("Selecting all Reports")
        select_all_report(conn)
        print("----------------------------------")
        print("Selecting all Students")
        select_all_students(conn)


def checkconfig():
    print("Do Something")
    database = "faceStudent.db"
    conn = create_connection(database)
    dbCur = conn.cursor()
    dbCur.execute("SELECT identified FROM report WHERE report_id=?", (report_num,))
    fileget = dbCur.fetchone()

    image_result = open('check.pickle', 'wb')
    image_result.write(fileget[0])

    with open('check.pickle', 'rb') as handle:
        unserialized_data = pickle.load(handle)

    print(unserialized_data)

def thecheck():
    print(report_num)

def main():
    print("Face Rec Detailed:")
    face_rec_detail()
    checkconfig()



if __name__ == '__main__':
    main()
