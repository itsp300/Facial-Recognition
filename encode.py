import face_recognition as fr
import os
import pickle
import base64

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
    print("Faces Encoded")
    return encoded

def main():
    encode = get_encoded_faces()
    print("Before")
    print(encode)
    with open("pickles/face.pickle", 'wb') as f:
        pickle.dump(encode, f)


if __name__ == '__main__':
    main()