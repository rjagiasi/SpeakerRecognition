#!/usr/bin/env python
# Gives a list of mfcc vectors for every file

import os

from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank
import scipy.io.wavfile as wav

directory = os.path.join(os.getcwd(), 'data_thuyg20_sre/test')
# directory = os.path.join(os.getcwd(), 'data_thuyg20_sre/enroll')
# print (directory)
for file in os.listdir(directory):
	# print(file)
	names = ['F101', 'F102', 'F103', 'F104', 'F105']
	if any(name in file for name in names):
		(rate,sig) = wav.read(os.path.join(directory, file))
		mfcc_feat = mfcc(sig,rate)
		# d_mfcc_feat = delta(mfcc_feat, 2)
		# fbank_feat = logfbank(sig,rate)
		myList = mfcc_feat[11:51,:]

		filename = file.split("_")[0]
		if filename[0] == 'M':
			filename = 10 + int(filename[3:])
		else:
			filename = int(filename[3:])

		# print(filename)
		for cur_list in myList:
			# if "F001" in file:
				myString = ','.join([str(i) for i in cur_list])
				myString += ','+str(filename)
				print(myString)
		# print(d_mfcc_feat[1:3,:])
