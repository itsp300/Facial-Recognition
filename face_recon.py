import face_recognition as fr
import cv2
import face_recognition
import numpy as np
import Database
import pickle
from datetime import datetime


def convert_to_binary_data(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def unknown_image_encoded(img):
    print("this is a check of one")
    """
    encode a face given the file name
    """
    face = fr.load_image_file("faces/" + img)
    encoding = fr.face_encodings(face)[0]

    return encoding


def classify_face(im, record_id):
    date_attended = datetime.now()
    database = "faceStudent.db"
    """
    will find all of the faces in a given image and label
    them if it knows what they are

    :param im: str of file path
    :return: list of face names
    """

    # Reads trained data from pickle file
    with open("pickles/face.pickle", 'rb') as f:
        faces = pickle.load(f)

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
        print(matches)

        # use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        print(best_match_index)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            print(name)

        face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Draw a box around the face
            cv2.rectangle(img, (left-20, top-20), (right+20, bottom+20), (255, 0, 0), 2)

            # Draw a label with a name below the face
            cv2.rectangle(img, (left-20, bottom -15), (right+20, bottom+20), (255, 0, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, name, (left -20, bottom + 15), font, 1.0, (255, 255, 255), 2)

    confidence = ["1", "2", "3", "4"]

    # create a database connection
    conn = Database.create_connection(database)
    with conn:
        counter=0
        for i in face_names:
            attend_id = i + record_id
            attend_record = (attend_id, record_id, i, confidence[counter], date_attended)
            print(attend_record)
            counter = counter+1
            Database.create_attend(conn, attend_record)

    return face_names
"""""
    # Display the resulting image
    while True:

        cv2.imshow('Video', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return face_names
"""""


def face():
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
