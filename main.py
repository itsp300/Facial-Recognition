import communication
import threading
import time
import ssl
import base64
import face_recon
import sqlite3
from sqlite3 import Error
from typing import Dict


debug = True
ws = None
report_num = ""
database = "faceStudent.db"

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
    print(rows)
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

    print(student_number)

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

def debug_log(message):
    if debug:
        print("[Main]" + str(message))


def start_queue_handler():
    while True:
        time.sleep(0.3) # artificial wait to prevent spamming cpu time checking, change as desired
        if not communication.request_queue.empty():
            message = communication.request_queue.get()
            if len(message) < 2048: # gets rid of 
                debug_log("Dispatching queued jwt request: " + str(message))
            else:
                debug_log("Dispatching queued jwt request [Truncated, too long for console (" + str(len(message)) + ")]")
            try:
                ws.send(message)
            except Exception as e:
                debug_log("Queue: " + str(e))
 

def use_communication_queue_thread():
    queue_thread = threading.Thread(target=start_queue_handler)
    queue_thread.start()
    
    
def use_communication_and_run():
    global ws
    while True:
        try:
            ws = communication.start_websocket()
            ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})  # REMOVE CERT_NONE WHEN IN PRODUCTION ENVIRONMENT
        except KeyboardInterrupt:
            break


# handler method, you write a bunch of these to handle different messages sent by server
def handle_auth_timeout(payload):
    print("Auth Timeout: " + str(payload))


def face_rec_image(payload: Dict):
    global report_num
    report_num = payload['record_id']
    print("Obtaining Facial Image Data")
    req_encode = payload['image']
    # Decode the image into temp image file
    image_64_decode = base64.decodebytes(req_encode)
    image_result = open('testDrive.jpg', 'wb')
    image_result.write(image_64_decode)

    communication.request_send_jwt(
        {
            "type": "face_rec",
            "students": "people",
            "record_id": payload['record_id']
        }
    )


def face_rec_identify(payload: Dict):
    print("Identifying People")
    people = face_recon.classify_face('testDrive.jpg', report_num)
    print('Students Identified:')
    print(people)


def face_rec_detail(payload: Dict):
    print("Detailed Info")

    id = payload["id"]
    
    communication.request_send_jwt(
        {
            "type": "face_rec_details",
            "identified": [
                {
                    "person_id": "RJMMLYX21",
                    "certainty": "56"
                },
                {
                    "person_id": "PR3C56TY",
                    "certainty": "56"
                }
            ]
        }
    )


def main():
  print("Server Started!")
  # define what message types we want to handle
  communication.register_message_type("auth_timeout", handle_auth_timeout)
  communication.register_message_type("face_rec", face_rec_image)
  communication.register_message_type("face_rec_identifier", face_rec_identify)
  communication.register_message_type("face_rec_details", face_rec_detail)

    # good place to start the facial recognition thread(s), or you could spawn them in the message handlers just above this line
  # start queue thread
  use_communication_queue_thread()
  # start websocket - code will never run past here since .run_forever blocks infinitely
  use_communication_and_run()


if __name__ == '__main__':
    main()

