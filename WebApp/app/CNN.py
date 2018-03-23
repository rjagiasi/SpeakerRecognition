import os
import numpy as numpy
import scipy.io.wavfile as wav
from python_speech_features import mfcc, delta, logfbank
# from app.feature_extraction import get_feature_vectors

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, Reshape
from keras.layers import Convolution1D, MaxPooling1D
from keras.optimizers import SGD
from keras.utils import np_utils

from matplotlib import pyplot as plt


from flask import current_app as app


no_of_features = 13
no_of_fbank_features = 13
no_of_columns = (3 * no_of_features) + no_of_fbank_features


def get_feature_vector(file, directory, no_of_frames, start_frame):

    (rate,sig) = wav.read(os.path.join(directory, file))
    fbank_feat = logfbank(sig,rate,nfft=2048)
    mfcc_feat = mfcc(sig,rate,winlen=0.032,winstep=0.016,numcep=13,nfft=2048)

    d_mfcc_feat = delta(mfcc_feat, 2)
    dd_mfcc_feat = delta(d_mfcc_feat, 2)
    
    mfcc_vectors = mfcc_feat[start_frame:start_frame+no_of_frames,:no_of_features]
    dmfcc_vectors = d_mfcc_feat[start_frame:start_frame+no_of_frames,:no_of_features]
    ddmfcc_vectors = dd_mfcc_feat[start_frame:start_frame+no_of_frames,:no_of_features]
    fbank_vectors = fbank_feat[start_frame:start_frame+no_of_frames,:no_of_fbank_features]
    
    feature_vectors = numpy.hstack((mfcc_vectors, dmfcc_vectors, ddmfcc_vectors, fbank_vectors))
    # print(feature_vectors)
    
    # get speaker index from filename
    speaker_index = int(file.split("_")[0])

    #append speaker index to feature vectors
    np_speaker_index = numpy.array([speaker_index])
    # print(np_speaker_index)
    temp = numpy.tile(np_speaker_index[numpy.newaxis,:], (feature_vectors.shape[0],1))
    # print(temp)
    concatenated_feature_vector = numpy.concatenate((feature_vectors,temp), axis=1)
    # print(concatenated_feature_vector)
    return concatenated_feature_vector



def trainCNN():

    directory = os.path.join(os.getcwd(), '../voices_processed')
    no_of_frames = 800
    start_frame = 10
    classes = len(os.listdir(directory))
    print(classes)
    dataset = numpy.empty([0, no_of_columns + 1])
    
    for file in os.listdir(directory):
        dataset = numpy.concatenate((dataset, get_feature_vector(file, directory, no_of_frames, start_frame)), axis=0)

    my_data = dataset
    numpy.random.shuffle(my_data)

    print(my_data.shape)
    Y = numpy.copy(my_data[:, no_of_columns:])
    print(Y.shape)
    
    X = numpy.copy(my_data[:, :no_of_columns])
    print(X.shape)
    
    mean = X.mean(0, keepdims=True)
    print(mean.shape)
    
    std_deviation = numpy.std(X, axis=0, keepdims=True)
    print(std_deviation.shape)
    
    normalized_X = (X - mean) / std_deviation
    print(normalized_X.shape)
    
    one_hot_labels = np_utils.to_categorical(Y, num_classes=classes+1)
    print(one_hot_labels)
    
    cnn_model = cnn_train(normalized_X, one_hot_labels, classes)
    test_cnn(cnn_model, mean, std_deviation)


def cnn_train(normalized_X, one_hot_labels, classes):
    
    temp = normalized_X.reshape(normalized_X.shape[0], no_of_columns, 1)
    
    model = Sequential()
    # 13 7 1 1 0.25 60 0.25 10 - 70%
    
    model.add(Convolution1D(52, 13, activation='tanh', input_shape=(no_of_columns,1)))
    print(model.output_shape)
    model.add(Convolution1D(52, 7, activation='tanh'))
    print(model.output_shape)
    model.add(Convolution1D(13, 3, activation='tanh'))
    print(model.output_shape)
    
    # stride = 2 - 70
    # 20, 10, 17 op - 64
    
    model.add(MaxPooling1D(pool_size=(1)))
#     model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(1000, activation='tanh'))
    model.add(Dropout(0.25))
    
    # 0.4 70
    model.add(Dense(classes+1, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.fit(temp, one_hot_labels, epochs=10, batch_size=100)
    return model


def test_cnn(model, mean, std_deviation):

    directory = os.path.join(os.getcwd(), '../temp/test')
    no_of_frames = 50
    test_frames = 50
    start_frame = 1
    classes = 3
    test_model = numpy.empty([0, no_of_columns + 1])
    
    for file in os.listdir(directory):
        test_model = numpy.concatenate((test_model, get_feature_vector(file, directory, no_of_frames, start_frame)), axis=0)
    
#     print(test_model.shape)

    test_X = numpy.copy(test_model[:, :no_of_columns])
#     print(test_X.shape)

    normalized_test_X = (test_X - mean) / std_deviation
#     print(normalized_test_X.shape)

    test_Y = numpy.copy(test_model[:, no_of_columns:])
#     print(test_Y.shape)
    test_labels = np_utils.to_categorical(test_Y, num_classes=classes+1)
    
    test_X = test_X.reshape(test_X.shape[0], no_of_columns, 1)
    normalized_test_X = normalized_test_X.reshape(normalized_test_X.shape[0], no_of_columns, 1)
    
    print(model.test_on_batch(normalized_test_X, test_labels, sample_weight=None))
    print(model.metrics_names)
    predictions = model.predict(normalized_test_X)

    b = [sum(predictions[current: current+test_frames]) for current in range(0, len(predictions), test_frames)]
    predicted_Y = []
    for row in b:
        predicted_Y.append(row.argmax(axis=0))

    # print(predicted_Y)
    # print(test_Y[::40].T)
    
    indices = numpy.argmax(predictions, axis=1)
    majority = []
    
    for i in range(0, len(indices), test_frames):
        majority.append(find_majority(indices[i:i + test_frames]))
        
#     majority = 
    for t, p, m in zip(test_Y[::test_frames].T[0], predicted_Y, majority):
        print(int(t), p, m[0])
    
#     for t, p in zip(test_Y.T[0], indices):
#         print(int(t), p)
    
    
    diff = predicted_Y - test_Y[::test_frames].T[0]
    maj_diff = numpy.array(majority)[:, 0] - test_Y[::test_frames].T[0]

    numerator = sum(x == 0 for x in diff)
    denominator = len(predicted_Y)
    
    numerator2 = sum(x == 0 for x in maj_diff)
    denominator2 = len(maj_diff)
    

    print("Accuracy prob_diff: {} of {} - {}".format(numerator, denominator, numerator/denominator))
    
    print("Accuracy maj_diff: {} of {} - {}".format(numerator2, denominator2, numerator2/denominator2))


def find_majority(k):
    myMap = {}
    maximum = ( '', 0 ) # (occurring element, occurrences)
    for n in k:
        if n in myMap: myMap[n] += 1
        else: myMap[n] = 1

        # Keep track of maximum on the go
        if myMap[n] > maximum[1]: maximum = (n,myMap[n])

    return maximum