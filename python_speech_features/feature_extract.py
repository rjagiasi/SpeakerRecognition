#!/usr/bin/env python
import os

from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank
import scipy.io.wavfile as wav

directory = os.path.join(os.getcwd(), 'sound_files')
# print (directory)
for file in os.listdir(directory):
	# print(file)
	(rate,sig) = wav.read(os.path.join(directory, file))
	mfcc_feat = mfcc(sig,rate)
	d_mfcc_feat = delta(mfcc_feat, 2)
	fbank_feat = logfbank(sig,rate)
	myList = mfcc_feat[2:3,:][0]
	myString = ','.join([str(i) for i in myList])
	myString += ','+file.split('_')[0]
	print(myString)
	# print(d_mfcc_feat[1:3,:])
