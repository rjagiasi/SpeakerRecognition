from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/registerSpeaker')
def registerSpeaker():
	return render_template('register_speaker.html')


@app.route('/register')
def register():
	pass


if __name__ == '__main__':
	app.run()