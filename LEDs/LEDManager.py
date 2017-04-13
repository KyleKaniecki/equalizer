
# ---------------Bibliopixel Imports-----------------------
from bibliopixel.drivers.LPD8806 import *
from bibliopixel import led
from bibliopixel import animation
from bibliopixel import colors

import numpy as np
import time

class LEDManager():

    def __init__(self):

        # LED Variables
        self.color = (0,0,0)
        self.driver = DriverLPD8806(160,c_order=ChannelOrder.RGB,use_py_spi=True,dev="/dev/spidev0.0",SPISpeed=8)
        self.leds = led.LEDStrip(self.driver,threadedUpdate=True)

    def setColor(self,color):
    	self.leds.fill(color)
    	self.leds.update()

    def fill(self,color=None,start=0,end=-1):

        if color is None:
            color = self.color

        self.leds.fill(color,start,end)
        self.leds.update()
        