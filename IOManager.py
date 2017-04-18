import pyaudio
import alsaaudio as aa
from Queue import Queue
import subprocess
import os
from threading import Thread



class IOManager():
    
    def __init__(self,chunk=2048,rate=44100,aux_input=False,aux_output=True):
        
        #self.p = pyaudio.PyAudio()

        self.chunk = chunk

        self.rate = rate
    
        self.stream = aa.PCM(aa.PCM_PLAYBACK,aa.PCM_NORMAL,card="hw:1")
        self.mixer = aa.Mixer(control="PCM")
        self.stream.setchannels(2)
        self.stream.setformat(aa.PCM_FORMAT_S16_LE)
        self.stream.setperiodsize(self.chunk)
        self.stream.setrate(self.rate)
        self.mixer.setvolume(100)


        self.streaming = None

    def start_stream(self,cmd="shairport-sync -o stdout"):

        self.streaming = subprocess.Popen(cmd,
                                          stdin=subprocess.PIPE,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE,
                                          shell=True)


    def read(self):
        try:
            if self.streaming:
                return self.streaming.stdout.read(self.chunk)
            elif self.stream.input:
                return self.stream.read()
            else:
                print "IOManager not set to accept input!"
        except OSError as err:
            if err.errno == errno.EAGAIN or err.errno == errno.EWOULDBLOCK:
                print err
                print err.errno
                exit(0)

    def write(self,data):
        try:
            self.stream.write(data)
        except Exception as e:
            print "couldnt write"
            print e


