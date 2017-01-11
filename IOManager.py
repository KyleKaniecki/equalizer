import pyaudio
import decoder


class IOManager():

    def __init__(self):
        
        self.p = pyaudio.PyAudio()

        self.chunk = 8192

        self.rate = 44100

        self.stream = self.p.open(format=pyaudio.paInt16,
                channels=1,
                rate=self.rate,
                input=True,
                output=True,
                frames_per_buffer=8192,
                output_device_index=2,
                input_device_index=2
                )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def play(self):

        data = self.read()
        self.write(data)
        return data

    def read(self,chunk=8192):
        return self.stream.read(chunk)

    def write(self,data,chunk=8192):
        self.stream.write(data,chunk)
