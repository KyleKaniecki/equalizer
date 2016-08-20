"""
FFT files that gets the values for the LED syncing to music

Created by: Kyle Kaniecki

Based off of program such as:

http://blog.yjl.im/2012/11/frequency-spectrum-of-sound-using.html

"""
import struct
import wave
import numpy as np
import pyaudio
#import decoder

_nFFT = 512
_BUF_SIZE = 4 * _nFFT
_FORMAT = pyaudio.paInt16
_CHANNELS = 2
_RATE = 44100
_SAMPLE_SIZE = 2
_MAX_Y = 2.0 ** (_SAMPLE_SIZE * 8 - 1)

def get_fft_data(file_name):

    p = pyaudio.PyAudio()
    stream = p.open(format=_FORMAT,
                    channels=_CHANNELS,
                    rate=_RATE,
                    input=True,
                    frames_per_buffer=_BUF_SIZE)
    

    N = max(stream.get_read_available() / _nFFT, 1) * _nFFT
    data = stream.read(N)

    y = np.array(struct.unpack("%dh" % (N*_CHANNELS) , data)) / _MAX_Y
    y_L = y[::2]
    y_R = y[1::2]

    Y_L = np.fft.fft(y_L, _nFFT)
    Y_R = np.fft.fft(y_R, _nFFT)

    return Y_L,Y_R

def main():

    file_name = "/home/pi/Music/"
