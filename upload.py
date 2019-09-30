from flask import Flask, render_template, request
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)

photes = UploadSet('photes', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'faces'
configure_uploads(app, photes)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photes.save(request.files['photo'])
        return filename
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)

