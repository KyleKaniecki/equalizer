import numpy as np
import struct


class AudioProcessor():

    def __init__(self,max_freq=10000,min_freq=20,channel_length=20):
        self.max = max_freq
        self.min = min_freq

        self.channel_length = channel_length

        self.mean = np.array([11.0 for _ in range(20)], dtype='float32')
        self.std = np.array([1.2,1.2,1.2,1.2,1.2,1.2,1.2,2.4,2.4,2.4,2.4,2.4,2.4,2.4,2.4,3.2,3.2,3.2,3.2,3.2],dtype='float32')

        self.frequency_limits = self.calculate_channel_frequency(min_freq,max_freq)


    def get_visualizer_array(self,data,chunk,rate):

        matrix = self.calculate_levels(data,chunk,rate)
        brightness = matrix - self.mean + (self.std * 0.5)
        brightness = brightness / (self.std * 1.25)
        brightness = np.clip(brightness, 0.0, 1.0)
        brightness = np.round(brightness, decimals=3)
        return brightness

    def calculate_levels(self,data, chunk, rate):
        piff = list()

        if len(piff) < 1:
            f1 = np.array(self.frequency_limits)
            piff = ((f1 * chunk) / rate).astype(int)

            for a in range(len(piff)):
                if piff[a][0] == piff[a][1]:
                    piff[a][1] += 1

        data = struct.unpack("%dh"%(len(data)/2),data)

        data = np.array(data, dtype="h")

        fourier = np.fft.rfft(data)
        fourier.resize(len(fourier)-1)
        power = np.abs(fourier) ** 2

        matrix = np.empty(20, dtype = "float32")

        for pin in range(20):
            matrix[pin] = sum(power[piff[pin][0]:piff[pin][1]])
        
        power = np.log10(matrix)
        
        return power

    def calculate_channel_frequency(self,min_freq, max_freq):
        channel_length = 20
        octaves = (np.log(self.max/self.min))/np.log(2)
        octaves_per_channel = octaves / self.channel_length
        frequency_limits = []
        frequency_store = []

        frequency_limits.append(min_freq)

        for i in range(1,self.channel_length+1):
            frequency_limits.append(frequency_limits[-1]*10**(3/(10 * (1/octaves_per_channel))))

        for i in range(0, channel_length):
            frequency_store.append((frequency_limits[i],frequency_limits[i+1]))
            
        return frequency_store