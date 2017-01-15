#!/usr/bin/env python
from IOManager import IOManager
from LEDs.LEDManager import LEDManager

import numpy as np
import struct
import sys
import select
import errno
import time
import math
from Queue import Empty

"""
def play(song):

    io = IOManager()
    leds = LEDManager()

    mean = np.array([12.0 for _ in range(8)], dtype='float32')
    std = np.array([3.2 for _ in range(8)], dtype='float32')

    frequency_limits = calculate_channel_frequency(20,15000)

    print("Playing...")
"""
def calculate_levels(data, chunk, rate, limits):
    piff = list()

    if len(piff) < 1:
        f1 = np.array(limits)
        piff = ((f1 * chunk) / rate).astype(int)

        for a in range(len(piff)):
            if piff[a][0] == piff[a][1]:
                piff[a][1] += 1

    data = struct.unpack("%dh"%(len(data)/2),data)

    data = np.array(data, dtype="h")

    fourier = np.fft.rfft(data)
    fourier.resize(len(fourier)-1)
    power = np.abs(fourier) ** 2

    matrix = np.empty(8, dtype = "float32")

    for pin in range(8):
        matrix[pin] = sum(power[piff[pin][0]:piff[pin][1]])
    
    power = np.log10(matrix)
    
    return power

def calculate_channel_frequency(min_freq, max_freq):
    channel_length = 8
    octaves = (np.log(max_freq/min_freq))/np.log(2)
    octaves_per_channel = octaves / channel_length
    frequency_limits = []
    frequency_store = []

    frequency_limits.append(min_freq)

    for i in range(1,channel_length+1):
        frequency_limits.append(frequency_limits[-1]*10**(3/(10 * (1/octaves_per_channel))))

    for i in range(0, channel_length):
        frequency_store.append((frequency_limits[i],frequency_limits[i+1]))
        
    return frequency_store


def wire():

    io = IOManager()
    leds = LEDManager()

    mean = np.array([11.0 for _ in range(8)], dtype='float32')
    std = np.array([3.2 for _ in range(8)], dtype='float32')
    frequency_limits = calculate_channel_frequency(20,15000)

    io.start_stream()

    update = 0

    while True:
        try:
            streamout = io.output_queue.get_nowait().strip('\n\r')
        except Empty:
            pass
        else:
            print streamout

        try:
            data = io.read()
        except OSError as err:
            if err.errno == errno.EAGAIN or err.errno == errno.EWOULDBLOCK:
                print err
                print err.errno
                exit(0)
                continue
        try:
            io.write(data)
        except Exception as e:
            print "couldnt write"
            print e
            time.sleep(1)
            continue

        
        if len(data):
            matrix = calculate_levels(data,io.chunk,io.rate,frequency_limits)
            brightness = matrix - mean + (std * 0.5)
            brightness = brightness / (std * 1.25)
            brightness = np.clip(brightness, 0.0, 1.0)
            brightness = np.round(brightness, decimals=3)

            if update >= 3:
                for i in range(0,8):
                    leds.fill(color=(0,0,255),start=i*20,end=int((i*20+(brightness[i]*20))))
                    leds.fill(color=(0,0,0),start=int(((i*20+(brightness[i]*20)))),end=-1)
                update = 0
            else:
                update += 1


            
    """
    try:
        while True:
            data = io.read()
            io.write(data)
            
            if len(data):
                matrix = calculate_levels(data,io.chunk,io.rate,frequency_limits)
                brightness = matrix - mean + (std * 0.5)
                brightness = brightness / (std * 1.25)
                brightness = np.clip(brightness, 0.0, 1.0)
                brightness = np.round(brightness, decimals=3)

                for i in range(0,8):
                    leds.fill(start=i*20,end=int((i*20+(brightness[i]*20))))
                    leds.fill(color=(0,0,0),start=int(((i*20+(brightness[i]*20)))),end=-1)
            
    except KeyboardInterrupt:
        pass

    finally:
        print("Thanks! :)")
    """

if __name__ == "__main__":
    wire()
