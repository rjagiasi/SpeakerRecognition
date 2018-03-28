import os
from flask import Flask, render_template, request, url_for, Response
import time
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from app.utils import get_all_speakers, preprocess_audio
from app.CNN import trainCNN

app = Flask(__name__)
CORS(app)
app.config.from_pyfile('config.py')


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/enrollSpeaker')
def enrollSpeaker():
	speakers = get_all_speakers()
	return render_template('enroll_speaker.html', speakers=speakers)


@app.route('/trainModel')
def trainModel():
	trainCNN()
	return render_template('index.html')
	# https://www.youtube.com/watch?v=f6Bf3gl4hWY
	# https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html


# app.config['progress_val'] = 0
# @app.route('/progress')
# def progress():
#     def generate():
#         val = app.config['progress_val']
#         while val <= 100:
#             yield "data:" + str(val) + "\n\n"
#     return Response(generate(), mimetype= 'text/event-stream')


@app.route('/recognizeSpeaker')
def recognizeSpeaker():
	return render_template('recognize_speaker.html')


@app.route('/upload', methods = ['POST'])
@cross_origin()
def upload():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(app.config['RAW_AUDIO_FOLDER'], file.filename))
        preprocess_audio(file.filename)
        
    return 'ok'


@app.route('/register')
def register():
	pass


if __name__ == '__main__':
	app.run()