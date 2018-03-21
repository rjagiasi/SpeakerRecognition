import os
import numpy as numpy
from python_speech_features import mfcc, delta, logfbank


no_of_features = 13
no_of_fbank_features = 13
no_of_columns = (3 * no_of_features) + no_of_fbank_features
test_frames = 50
classes = 10


def get_feature_vector(dataset_type):
    #set parameters for training and testing
    if (dataset_type == "train"):
        directory = os.path.join(os.getcwd(), '../voices_processed')
        no_of_frames = 800
        start_frame = 10
    elif (dataset_type == "test"):    
        directory = os.path.join(os.getcwd(), '../voices_processed')
        no_of_frames = test_frames
        start_frame = 1
        
    dataset = numpy.empty([0, no_of_columns + 1])
    
    for file in os.listdir(directory):
        
        # filter speakers
        n = int(classes/2)
#         print(n)
        names = []
        
        for i in range (1, n+1):
            names.append('F1' + '%02d'%(i))
            names.append('M1' + '%02d'%(i))

        if any(name in file for name in names):
            
            # extract mfcc vectors
#             print(file)
            (rate,sig) = wav.read(os.path.join(directory, file))
            fbank_feat = logfbank(sig,rate,nfft=2048)
            mfcc_feat = mfcc(sig,rate,winlen=0.032,winstep=0.016,numcep=13,nfft=2048)
            
#             print("SR :" + str(rate) + " " + file)
#             y, sr = librosa.load(os.path.join(directory, file))
#             mfcc_feat = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, n_fft=2048).T
            d_mfcc_feat = delta(mfcc_feat, 2)
            dd_mfcc_feat = delta(d_mfcc_feat, 2)
            
#             fbank_feat = logfbank(sig,rate)
            mfcc_vectors = mfcc_feat[start_frame:start_frame+no_of_frames,:no_of_features]
            dmfcc_vectors = d_mfcc_feat[start_frame:start_frame+no_of_frames,:no_of_features]
            ddmfcc_vectors = dd_mfcc_feat[start_frame:start_frame+no_of_frames,:no_of_features]
            fbank_vectors = fbank_feat[start_frame:start_frame+no_of_frames,:no_of_fbank_features]
            
            feature_vectors = numpy.hstack((mfcc_vectors, dmfcc_vectors, ddmfcc_vectors, fbank_vectors))
#             print(feature_vectors.shape)
            
            # get speaker index from filename
            speaker_index = file.split("_")[0]
            if speaker_index[0] == 'M':
                speaker_index = n + int(speaker_index[3:])
            else:
                speaker_index = int(speaker_index[3:])

            #append speaker index to feature vectors
            np_speaker_index = numpy.array([speaker_index])
            temp = numpy.tile(np_speaker_index[numpy.newaxis,:], (feature_vectors.shape[0],1))
            concatenated_feature_vector = numpy.concatenate((feature_vectors,temp), axis=1)
            
#             print(concatenated_feature_vector.shape)
#             print(fbank_vectors.shape)
            
            # append file's data to dataset
            dataset = numpy.concatenate((dataset, concatenated_feature_vector), axis=0)
            
    
    return dataset