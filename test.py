import face_recon
import base64
from typing import Dict
import Database
report_num = ""


def face_rec_detail():
    database = "faceStudent.db"
    global report_num
    report_num = "2"
    face = face_recon.classify_face('testDrive.jpg', report_num)
    print(face)

    # create a database connection
    conn = Database.create_connection(database)
    dbCursor = conn.cursor()
    dbCursor.execute("SELECT * FROM attendance")
    row = dbCursor.fetchall()
    rowDict = dict(zip([c[0] for c in dbCursor.description], row))

    print(rowDict)

    with conn:
        print("Selecting all Attendance Data")
        Database.select_all_tasks(conn)
        print("-----------------------------------")
        print("Selecting all Students")
        Database.select_all_students(conn)
        print("Certain Students: ")
        check = Database.create_the_statement(conn, report_num)
        print(check)


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
    print("Face Rec Detailed:")
    face_rec_detail()


if __name__ == '__main__':
    main()
