import face_recon
import sqlite3
from sqlite3 import Error


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
    cur.execute("SELECT * FROM students")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def main():
    database = "faceStudent.db"
    face = face_recon.classify_face('testDrive.jpg', "9")
    print(face)

    # create a database connection
    conn = create_connection(database)
    dbCursor = conn.cursor()
    dbCursor.execute("SELECT * FROM students where report_id = '8'")
    row = dbCursor.fetchone()
    rowDict = dict(zip([c[0] for c in dbCursor.description], row))

    print(rowDict)
    with conn:
        print("Selecting all Student Data")
        select_all_tasks(conn)


if __name__ == '__main__':
    main()
