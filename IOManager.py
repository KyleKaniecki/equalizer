<<<<<<< HEAD
import pyaudio
import alsaaudio as aa
from Queue import Queue
import subprocess
import os
from threading import Thread



class IOManager():
    
    def __init__(self,chunk=2048,rate=44100,aux_input=False,aux_output=True,fifo="/tmp/shairportpipe"):
        
        #self.p = pyaudio.PyAudio()

        self.chunk = chunk

        self.rate = rate
        """
        self.stream = self.p.open(format=self.p.get_format_from_width(2),
                channels=2,
                rate=self.rate,
                input=aux_input,
                output=aux_output,
                frames_per_buffer=self.chunk
                )
        """
        #print aa.pcms()
        self.stream = aa.PCM(aa.PCM_PLAYBACK,aa.PCM_NORMAL,card="hw:1")
        self.mixer = aa.Mixer(control="PCM")
        self.stream.setchannels(2)
        self.stream.setformat(aa.PCM_FORMAT_S16_LE)
        self.stream.setperiodsize(self.chunk)
        self.stream.setrate(self.rate)
        self.mixer.setvolume(100)

        self.output_queue = Queue()

        self.streaming = None

        self.fifo = fifo

    def start_stream(self,cmd="shairport-sync -o stdout"):

        self.streaming = subprocess.Popen(cmd,
                                          stdin=subprocess.PIPE,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE,
                                          shell=True)
        self.outthr = Thread(target=self.enqueue_output, args=(self.streaming.stderr,self.output_queue))
        self.outthr.daemon = True
        self.outthr.start()


    def read(self):
        if self.streaming:
            return self.streaming.stdout.read(self.chunk)
        elif self.stream.input:
            return self.stream.read()
        else:
            print "IOManager not set to accept input!"

    def write(self,data):
        self.stream.write(data)

    def enqueue_output(self, out, queue):
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()

