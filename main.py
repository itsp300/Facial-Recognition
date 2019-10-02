from flask import Flask, escape, request, jsonify, render_template, redirect, make_response, abort
import os
import base64
import requests

app = Flask(__name__)


@app.route('/attendances', methods=['GET', 'POST'])
def post():
    return str({"subjectAttendances": [{"code": "IT00311", "attendance": 3, "total": 4}, {"code": "ITDA211", "attendance": 1, "total": 5}]})


@app.route('/echo', methods=['POST'])
def echo():
    data = jsonify(request.get_json(force=True))
    return data


@app.route('/upload', methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        file = request.files["file"]
        file.save(os.path.join("faces", file.filename))
        return "Sucess"
    return render_template("index.html", message="Upload")


@app.route('/check', methods=['POST'])
def check():
    filecheck = request.get_json()
    filecheck = filecheck['process']

    if filecheck == 'run':
        # Get Request
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

    image_64_decode = base64.decodebytes(req_encode)
    image_result = open('temp.jpg', 'wb')
    image_result.write(image_64_decode)

    if request.method == "POST":
        import face_rec
    return filecheck


@app.route('/done', methods=['POST'])
def postre():
    print("In")
    data = request.get_json()
    print(data)
    return data
