import subprocess
import soundcard


class IOManager():

    def __init__(self, chunk=2048, rate=44100):
        self.chunk = chunk
        self.rate = rate
        self.speaker = soundcard.default_speaker()
        self.mic = soundcard.default_microphone()
        self.shairport = None

    def start_shairport_sync(self):
        self.shairport = subprocess.Popen("shairport-sync -o stdout",
                                          stdin=subprocess.PIPE,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE,
                                          shell=True)

    def is_input_alive(self):
        if self.shairport:
            return self.shairport.poll() != None
        return True

    def read(self):
        if self.shairport:
            return self.shairport.stdout.read(self.chunk)

        return self.mic.record(self.chunk, self.rate)

    def write(self, data):
        try:
            self.speaker.play(data, self.rate)
        except Exception:
            pass