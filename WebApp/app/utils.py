from flask import current_app as app

import os
import scipy.io.wavfile as wav


def preprocess_audio(file):
    source = app.config['RAW_AUDIO_FOLDER']
    source = os.path.join(source, file)
    dest = app.config['PROCESSED_AUDIO_FOLDER']
    dest = os.path.join(dest, file)
    (rate,sig) = wav.read(source)

    if int(rate) > 8000:
        cmd = "sox {} {} silence 1 0.3 -45d -1 0.1 1% lowpass 7000".format(source, dest)
        os.system(cmd);
    else:
        cmd = "sox {} {} silence 1 0.3 -55d -1 0.1 1% lowpass 3500".format(source, dest)
        os.system(cmd);

def get_all_speakers():
    speakers = []
    directory = os.listdir(app.config['PROCESSED_AUDIO_FOLDER'])
    for file in directory:
    	speakers.append(file)
    return speakers


def find_majority(k):
    myMap = {}
    maximum = ( '', 0 ) # (occurring element, occurrences)
    for n in k:
        if n in myMap: myMap[n] += 1
        else: myMap[n] = 1

        # Keep track of maximum on the go
        if myMap[n] > maximum[1]: maximum = (n,myMap[n])

    return maximum