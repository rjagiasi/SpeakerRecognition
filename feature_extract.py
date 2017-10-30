#!/usr/bin/env python
# Gives a list of mfcc vectors for every file

import os

from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank
import scipy.io.wavfile as wav

directory = os.path.join(os.getcwd(), 'python_speech_features/sound_files')
# print (directory)
for file in os.listdir(directory):
	# print(file)
	(rate,sig) = wav.read(os.path.join(directory, file))
	mfcc_feat = mfcc(sig,rate)
	# d_mfcc_feat = delta(mfcc_feat, 2)
	# fbank_feat = logfbank(sig,rate)
	myList = mfcc_feat[1:41,:]
	for cur_list in myList:
		# if "F001" in file:
		myString = ','.join([str(i) for i in cur_list])
		myString += ','+file
		print(myString)
	# print(d_mfcc_feat[1:3,:])
