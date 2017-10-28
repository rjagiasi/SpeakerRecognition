#!/usr/bin/env python

from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank
import scipy.io.wavfile as wav

(rate,sig) = wav.read("english.wav")
mfcc_feat = mfcc(sig,rate)
d_mfcc_feat = delta(mfcc_feat, 2)
fbank_feat = logfbank(sig,rate)

myList = mfcc_feat[1:40,:]
for cur_list in myList:
	myString = ','.join([str(i) for i in cur_list])
	myString += ",english.wav"
	print(myString)

# a e f g l m 