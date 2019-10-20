import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
import requests
import sqlite3
from datetime import datetime
from sqlite3 import Error

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

def create_record(conn, faceRecord):
    """
        Create a new record  into the students table
        :param conn:
        :param faceRecord:
        :return: project id
        """
    sql = ''' INSERT INTO students(report_id,student_number,confidence, date_attended)
                  VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, faceRecord)
    return cur.lastrowid

def get_encoded_faces():
    """
    looks through the faces folder and encodes all
    the faces

    :return: dict of (name, image encoded)
    """
    encoded = {}

    for dirpath, dnames, fnames in os.walk("./faces"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("faces/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding

    return encoded


def unknown_image_encoded(img):
    """
    encode a face given the file name
    """
    face = fr.load_image_file("faces/" + img)
    encoding = fr.face_encodings(face)[0]

    return encoding


def classify_face(im, record_id):
    dateAttended = datetime.now()
    database = "faceStudent.db"
    """
    will find all of the faces in a given image and label
    them if it knows what they are

    :param im: str of file path
    :return: list of face names
    """
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    img = cv2.imread(im, 1)
    # img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    # img = img[:,:,::-1]

    face_locations = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(img, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"

        # use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Draw a box around the face
            cv2.rectangle(img, (left-20, top-20), (right+20, bottom+20), (255, 0, 0), 2)

            # Draw a label with a name below the face
            cv2.rectangle(img, (left-20, bottom -15), (right+20, bottom+20), (255, 0, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, name, (left -20, bottom + 15), font, 1.0, (255, 255, 255), 2)


    # Post data to server
    url = 'https://8080.imja.red/imageRet'
    myobj = {'student': face_names[0]}
    x = requests.post(url, json=myobj)

    if x.status_code == 200:
        # print the response text (the content of the requested file):
        print('test' + x.text)
    elif x.status_code == 502:
        print("502 Error: Can't send data to server.")

    # create a database connection
    conn = create_connection(database)
    with conn:
        face_name = face_names[0];
        face_record = (record_id, face_name, "16.0", dateAttended)
        the_id = create_record(conn, face_record)


    return face_names
"""""
    # Display the resulting image
    while True:

        cv2.imshow('Video', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return face_names
"""""
def face():
    print(" hi")
    # Get Request
    """""
    response = requests.get('https://8080.imja.red/image')
    if response.status_code == 200:
        print("Succesful Connection")
        req_encode = bytes(response.text, 'utf-8')
    elif response.status_code == 502:
        print("502 Error: Server is offline")
        print("Loading backup image instead")

        # Encode the image
        image = open('temp.jpg', 'rb')
        image_read = image.read()
        req_encode = base64.encodebytes(image_read)
    """

    print(classify_face('test.jpg'))
