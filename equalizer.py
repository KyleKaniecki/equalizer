from __future__ import print_function
"""
Module to handle the FFT of music files played in the Main_gui
This will make the LED strip seem to go to the music that is currently
being played

Created by: Kyle Kaniecki
Inspired by: lightshowpi

"""



from bibliopixel.drivers.LPD8806 import *
from bibliopixel import led
from bibliopixel import animation
from bibliopixel import colors
from LEDs import LED_anims

import numpy as np
import time
import threading
import alsaaudio as aa
import decoder
import struct
import random
import os
import audioop
import colorsys

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
 
def preshow(leds):
    animation = LED_anims.middle_strobe(leds,start=0,end=-1)
    animation.run(threaded=False,fps=20, max_steps = 63)
    return animation

def audio_in():
    driver = DriverLPD8806(160,c_order=ChannelOrder.RGB,use_py_spi=True,dev="/dev/spidev0.0",SPISpeed=2)
    leds = led.LEDStrip(driver,threadedUpdate=False)
    chunk = 2048
    mean = np.array([12.0 for _ in range(8)], dtype='float32')
    std = np.array([3.2 for _ in range(8)], dtype='float32')
    frequency_limits = calculate_channel_frequency(20,15000)
    rate = 44100
    
    stream = aa.PCM(aa.PCM_CAPTURE,aa.PCM_NORMAL, card="hw:0")
    stream.setchannels(2)
    stream.setformat(aa.PCM_FORMAT_S16_LE)
    stream.setrate(rate)
    stream.setperiodsize(chunk)
    
    output = aa.PCM(aa.PCM_PLAYBACK,aa.PCM_NORMAL,card="hw:0")
    output.setchannels(2)
    output.setformat(aa.PCM_FORMAT_S16_LE)
    output.setperiodsize(chunk)
    output.setrate(rate)
    out = lambda data : output.write(data)

    print("Audio in, press Crtl + C to exit this mode")

    
    try:

        while True:
            length, data = stream.read()

            if out is not None:
                out(data)

            if len(data):
                audio_max = audioop.max(data, 2)
                if audio_max < 250:
                    pass
                else:
                    
                    matrix = calculate_levels(data,chunk,rate,frequency_limits)
                    brightness = matrix - mean + (std * 0.5)
                    brightness = brightness / (std * 1.25)
                    brightness = np.clip(brightness, 0.0, 1.0)
                    brightness = np.round(brightness, decimals=3)


                    for i in range(0,8):
                        leds.fill((0,255,0),i*20, int((i*20+(brightness[i]*20))))
                        leds.fill((0,0,0),int(((i*20+(brightness[i]*20)))),-1)

                    leds.update()
    except KeyboardInterrupt:
        pass

    finally:
        print("Thanks! :)")
        

    
    
def change_color(current):
    if current[0] > 0:
        current = (0,255,0)
        return current
    elif current[1] > 0:
        current = (0,0,255)
        return current
    else:
        current = (255,0,0)
        return current
    
def play_library():
    """
    This is the main function that is run when the 
    """
    driver = DriverLPD8806(160,c_order=ChannelOrder.RGB,use_py_spi=True,dev="/dev/spidev0.0",SPISpeed=2)
    leds = led.LEDStrip(driver,threadedUpdate=False)
    songs = []
    current_song = 0
    current = (0,0,255)
    chunk = 2048
    rate = 44100
    mean = np.array([12.0 for _ in range(8)], dtype='float32')
    std = np.array([3.2 for _ in range(8)], dtype='float32')
    frequency_limits = calculate_channel_frequency(20,15000)
    output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL, card="hw:0")
    output.setchannels(2)
    output.setformat(aa.PCM_FORMAT_S16_LE)
    output.setperiodsize(chunk)
    output.setrate(rate)
    out = lambda data : output.write(data)
    time = 0
    for file in os.listdir("/home/pi/Music"):
            songs.append(file)
    print(songs)
    while current_song < len(songs):
        
        filename = songs[current_song]
        preshow_anim = preshow(leds)
        
        try:
            header = False
            
            if any([ax for ax in [".mp4", ".m4a", ".m4b"] if ax in filename]):
                header = True
                
            musicfile = decoder.open("/home/pi/Music/" + filename, header)
            
            for _ in range(5):
                data = musicfile.readframes(chunk)

                
            
            while data != "":
                out(data)

                matrix = calculate_levels(data,chunk,rate,frequency_limits)
                brightness = matrix - mean + (std * 0.5)
                brightness = brightness / (std * 1.25)
                brightness = np.clip(brightness, 0.0, 1.0)
                brightness = np.round(brightness, decimals=3)


                for i in range(0,8):
                    rgbColor =colorsys.hsv_to_rgb((int(time)%365)*1.01,1,1)
                    leds.fill((20+int(rgbColor[0]*(255-20)),int(rgbColor[1]*255),int(rgbColor[2]*255)),i*20, int((i*20+(brightness[i]*20))))
                    leds.fill((0,0,0),int(((i*20+(brightness[i]*20)))),-1)
                    
                leds.update()
                time = time + 0.25
                
                data = musicfile.readframes(chunk)
        except KeyboardInterrupt:
            pass
            
        current_song += 1
    

if __name__ == "__main__":
    #audio_in()
    play_library()
