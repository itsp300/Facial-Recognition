import face_recon
import sqlite3
from sqlite3 import Error
import ast
import base64
from typing import Dict
report_num = ""

def convertTuple(tup):
    str = ''.join(tup)
    return str

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
    cur.execute("SELECT student_number FROM attendance")

    rows = cur.fetchall()
    for row in rows:
        print(row)

def create_the_statement(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    student_number =[]
    att_confidence =[]
    identified=[]
    cur = conn.cursor()
    cur.execute("SELECT student_number FROM attendance WHERE report_id =" +report_num)
    students = cur.fetchall()

    for student in students:
        stud = convertTuple(student)
        student_number.append(stud)


    cur.execute("SELECT confidence FROM attendance WHERE report_id =" + report_num)
    confidence = cur.fetchall()

    for con in confidence:
        conf = convertTuple(con)
        att_confidence.append(conf)

    print(att_confidence)

    counter = 0
    for person in student_number:
        therecords = {
            "person_id": person,
            "certainty": att_confidence[counter]
        }
        identified.append(therecords)
        counter = counter+1

    report_config = {
        "type": "face_rec_details",
        "identified": identified
    }

    return report_config

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
    print(rows)
    for row in rows:
        print(row)


def face_rec_detail():
    database = "faceStudent.db"
    global report_num
    report_num = "8"
    face = face_recon.classify_face('testDrive.jpg', report_num)
    print(face)

    # create a database connection
    conn = create_connection(database)
    dbCursor = conn.cursor()
    dbCursor.execute("SELECT * FROM attendance")
    row = dbCursor.fetchall()
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
        print("Certain Students: ")
        check = create_the_statement(conn)
        print(check)


def checkconfig():
    d={
        "name": "love"
    }

    print(d)
    for k, v in d.items():
        if v[0] == '{' and v[-1] == '}':
            d[k] = ast.literal_eval(v)

    print(d)


def face_rec(payload:Dict):
    print("Obtaining Facial Image Data")
    global report_num
    print(payload)
    report_num = payload['record_id']
    req_encode = payload['image']
    # Decode the image into temp image file
    image_64_decode = base64.decodebytes(req_encode)
    image_result = open('testDrive.jpg', 'wb')
    image_result.write(image_64_decode)

    communication = {
            "type": "face_rec",
            "students": "people",
            "record_id": payload['record_id']
        }

    return communication



def main():
    # Encode the image
    image = open('testDrive.jpg', 'rb')
    image_read = image.read()
    image_64_encode = base64.encodebytes(image_read)
    com = {
        "record_id": "1",
        "image": image_64_encode
    }


    # print(com)
    print("Face Rec Detailed:")
    face_rec_detail()


if __name__ == '__main__':
    main()
