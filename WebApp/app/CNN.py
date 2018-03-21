# import os
# import numpy as numpy
# # from app.feature_extraction import get_feature_vectors

# from keras.models import Sequential
# from keras.layers import Dense, Dropout, Activation, Flatten, Reshape
# from keras.layers import Convolution1D, MaxPooling1D
# from keras.utils import np_utils

# from matplotlib import pyplot as plt


# def get_feature_vector(file_path):
#     no_of_features = 13
#     no_of_fbank_features = 13
#     no_of_columns = (3 * no_of_features) + no_of_fbank_features
#     no_of_frames = 800
#     start_frame = 10

#     (rate,sig) = wav.read(file_path)
#     fbank_feat = logfbank(sig,rate,nfft=2048)
#     mfcc_feat = mfcc(sig,rate,winlen=0.032,winstep=0.016,numcep=13,nfft=2048)

#     d_mfcc_feat = delta(mfcc_feat, 2)
#     dd_mfcc_feat = delta(d_mfcc_feat, 2)
    
#     mfcc_vectors = mfcc_feat[start_frame:start_frame+no_of_frames,:no_of_features]
#     dmfcc_vectors = d_mfcc_feat[start_frame:start_frame+no_of_frames,:no_of_features]
#     ddmfcc_vectors = dd_mfcc_feat[start_frame:start_frame+no_of_frames,:no_of_features]
#     fbank_vectors = fbank_feat[start_frame:start_frame+no_of_frames,:no_of_fbank_features]
    
#     feature_vectors = numpy.hstack((mfcc_vectors, dmfcc_vectors, ddmfcc_vectors, fbank_vectors))
    
#     # get speaker index from filename
#     speaker_index = file.split("_")[0]

#     #append speaker index to feature vectors
#     np_speaker_index = numpy.array([speaker_index])
#     temp = numpy.tile(np_speaker_index[numpy.newaxis,:], (feature_vectors.shape[0],1))
#     concatenated_feature_vector = numpy.concatenate((feature_vectors,temp), axis=1)
#     return concatenated_feature_vector



# def trainCNN():

#     directory = os.listdir(os.path.join(os.getcwd(), '../voices_processed'))
#     classes = len(directory)
#     dataset = numpy.empty([0, no_of_columns + 1])
    
#     for file in directory:
#         file_path = os.path.join(directory, file)
#         dataset = numpy.concatenate((dataset, get_feature_vector(file_path)), axis=0)

#         app.logger.error('logged in successfully')

#     my_data = dataset
#     numpy.random.shuffle(my_data)

