import os
import scipy.io.wavfile as wav


def preprocess_audio(file):
    source = os.path.join(os.getcwd(), '../voices_raw')
    source = os.path.join(source, file)
    dest = os.path.join(os.getcwd(), '../voices_processed')
    dest = os.path.join(dest, file)
    (rate,sig) = wav.read(source)

    if int(rate) >= 8000:
        cmd = "sox {} {} silence 1 0.3 -55d -1 0.1 1% lowpass 7000".format(source, dest)
        os.system(cmd);
        print('hmm')
    else:
        cmd = "sox {} {} silence 1 0.3 -55d -1 0.1 1% lowpass 3500".format(source, dest)
        os.system(cmd);
        print('hm')


def main():
    directory = os.listdir(os.path.join(os.getcwd(), '../voices_raw'))
    for file in directory:
        preprocess_audio(file)
    

if __name__ == '__main__':
	main()