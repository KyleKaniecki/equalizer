#!/usr/bin/env python
from IOManager import IOManager
from LEDs.LEDManager import LEDManager

from bibliopixel import colors
from bibliopixel.drivers.LPD8806 import *
from bibliopixel import led

import numpy as np
import struct
import sys
import select
import errno
import time
import math
from Queue import Empty


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

    matrix = np.empty(20, dtype = "float32")

    for pin in range(20):
        matrix[pin] = sum(power[piff[pin][0]:piff[pin][1]])
    
    power = np.log10(matrix)
    
    return power

def calculate_channel_frequency(min_freq, max_freq):
    channel_length = 20
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
    #leds = LEDManager()
    driver = DriverLPD8806(160,c_order=ChannelOrder.RGB,use_py_spi=True,dev="/dev/spidev0.0",SPISpeed=16)
    ledmatrix = led.LEDMatrix(driver,width=20,height=8,threadedUpdate=True,rotation=1,serpentine=False)

    
    mean = np.array([11.0 for _ in range(20)], dtype='float32')
    #std = np.array([3.2 for _ in range(20)], dtype='float32')
    

    #mean = np.array([11,11,11,11,11,11,11,11,6,6,6,6,6,3,3,3,3,3,3,3],dtype='float32')
    std = np.array([1.2,1.2,1.2,1.2,1.2,1.2,1.2,2.4,2.4,2.4,2.4,2.4,2.4,2.4,2.4,2.4,2.4,2.4,2.4,2.4],dtype='float32')

    frequency_limits = calculate_channel_frequency(20,15000)

    io.start_stream()

    update = 0
    count = 0.0

    while True:
        """
        try:
            streamout = io.output_queue.get_nowait().strip('\n\r')
        except Empty:
            pass
        else:
            print streamout
        """
        #This reads the data from the input stream 
        try:
            data = io.read()
        #if we happen to get a OSError
        except OSError as err:
            if err.errno == errno.EAGAIN or err.errno == errno.EWOULDBLOCK:
                print err
                print err.errno
                exit(0)
                continue
        #This writes the data out to the hardware audio out port
        try:
            io.write(data)
        #Catch any exception that Python might throw
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

            if update < 10:
                update += 1
            else:
                update = 0

            if int(count) >= int(255.0):
                count = 0.0
            else:
                count += .25
            
            """
            HORIZONTAL
            leds.fill(color=colors.hue2rgb_rainbow(int(count)),start=update*20,end=int((update*20+(brightness[update]*20))))
            leds.fill(color=(0,0,0),start=int(((update*20+(brightness[update]*20)))),end=(update* 20)+20)
            """

            ledmatrix.drawLine(x0=0,y0=int(update),x1=int(brightness[update]*7),y1=update,color=colors.hue2rgb_rainbow(int(count)))
            ledmatrix.drawLine(x0=int(brightness[update]*7),y0=update,x1=7,y1=update,color=(0,0,0))

            ledmatrix.drawLine(x0=0,y0=update+1,x1=int(brightness[update+1]*8),y1=update+1,color=colors.hue2rgb_rainbow(int(count)))
            ledmatrix.drawLine(x0=int(brightness[update+1]*8),y0=update+1,x1=8,y1=update+1,color=(0,0,0))

            ledmatrix.drawLine(x0=0,y0=update+2,x1=int(brightness[update+2]*8),y1=update+2,color=colors.hue2rgb_rainbow(int(count)))
            ledmatrix.drawLine(x0=int(brightness[update+2]*8),y0=update+2,x1=8,y1=update+2,color=(0,0,0))

            ledmatrix.drawLine(x0=0,y0=update+3,x1=int(brightness[update+3]*7),y1=update+3,color=colors.hue2rgb_rainbow(int(count)))
            ledmatrix.drawLine(x0=int(brightness[update+3]*8),y0=update+3,x1=8,y1=update+3,color=(0,0,0))

            ledmatrix.drawLine(x0=0,y0=update+4,x1=int(brightness[update+4]*8),y1=update+4,color=colors.hue2rgb_rainbow(int(count)))
            ledmatrix.drawLine(x0=int(brightness[update+4]*8),y0=update+4,x1=8,y1=update+4,color=(0,0,0))

            ledmatrix.drawLine(x0=0,y0=update+5,x1=int(brightness[update+5]*8),y1=update+5,color=colors.hue2rgb_rainbow(int(count)))
            ledmatrix.drawLine(x0=int(brightness[update+5]*8),y0=update+5,x1=8,y1=update+5,color=(0,0,0))

            ledmatrix.drawLine(x0=0,y0=update+6,x1=int(brightness[update+6]*8),y1=update+6,color=colors.hue2rgb_rainbow(int(count)))
            ledmatrix.drawLine(x0=int(brightness[update+6]*8),y0=update+6,x1=8,y1=update+6,color=(0,0,0))

            ledmatrix.drawLine(x0=0,y0=update+7,x1=int(brightness[update+7]*8),y1=update+7,color=colors.hue2rgb_rainbow(int(count)))
            ledmatrix.drawLine(x0=int(brightness[update+7]*8),y0=update+7,x1=8,y1=update+7,color=(0,0,0))

            ledmatrix.drawLine(x0=0,y0=update+8,x1=int(brightness[update+8]*8),y1=update+8,color=colors.hue2rgb_rainbow(int(count)))
            ledmatrix.drawLine(x0=int(brightness[update+8]*8),y0=update+8,x1=8,y1=update+8,color=(0,0,0))

            ledmatrix.drawLine(x0=0,y0=update+9,x1=int(brightness[update+9]*8),y1=update+9,color=colors.hue2rgb_rainbow(int(count)))
            ledmatrix.drawLine(x0=int(brightness[update+9]*8),y0=update+9,x1=8,y1=update+9,color=(0,0,0))

            ledmatrix.update()
            




if __name__ == "__main__":
    wire()
