from flask import Flask, escape, request, jsonify, render_template, redirect, make_response
import os
import base64

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
    '''''''''
    
    req_encode = bytes(filecheck, 'utf-8')
    image_64_decode = base64.decodebytes(req_encode)
    image_result = open('temp.jpg', 'wb')
    image_result.write(image_64_decode)
    print(filecheck)
    '''
    filecheck = request.get_json()
    filecheck = filecheck['student']

    if request.method == "POST":
        import face_rec
    return filecheck


@app.route('/done', methods=['POST'])
def postre():
    print("In")
    data = request.get_json()
    print(data)
    return data

