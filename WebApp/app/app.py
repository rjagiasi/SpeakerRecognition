import os
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename


app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/enrollSpeaker')
def enrollSpeaker():
	return render_template('enroll_speaker.html')


@app.route('/recognizeSpeaker')
def recognizeSpeaker():
	return render_template('recognize_speaker.html')


UPLOAD_FOLDER = '/audio/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods = ['POST'])
@cross_origin()
def upload():
    if request.method == 'POST':
        file = request.files['file']
        app.logger.error('%s logged in successfully', file.filename)
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return 'ok'


@app.route('/register')
def register():
	pass


if __name__ == '__main__':
	app.run()