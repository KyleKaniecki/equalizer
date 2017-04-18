#!/usr/bin/env python

from bibliopixel.drivers.LPD8806 import *
from bibliopixel import led
from bibliopixel import animation
from bibliopixel import colors
import time
from BiblioPixelAnimations.strip import Searchlights

driver = DriverLPD8806(160,c_order=ChannelOrder.RGB,use_py_spi=True,dev="/dev/spidev0.0",SPISpeed=16)
leds = led.LEDStrip(driver,threadedUpdate=True)
matrix = led.LEDMatrix(driver,width=20,height=8,threadedUpdate=True,rotation=1,serpentine=False)
update = 0

class test_anim(animation.BaseStripAnim):

	def __init__(self, led,start=0, end=-1):
		super(test_anim,self).__init__(led,start,end)
		self.subtract = False

	def step(self, amt=1):

		if self._step == 100:
			self.subtract = True
		elif self._step == 0:
			self.subtract = False

		self.clear()
		for i in range(5):
			if self._step -i < 0:
				continue
			self._led.set(self._step - i,(255,0,0))

		if self.subtract:
			self._step -= amt
		else:
			self._step += amt


	def clear(self):
		self._led.fill((0,0,0))
		self._led.update()

class rainbow(animation.BaseStripAnim):

	def __init__(self,led,start=0,end=-1):
		super(rainbow,self).__init__(led,start,end)

	def step(self,amt=1):
		self._led.fill(colors.hue2rgb_spectrum(self._step))
		self._led.update()

		self._step += amt

		if self._step > 255:
			self._step = 0 

class police(animation.BaseStripAnim):

	def __init__(self, led, start=0, end=-1):
		super(police,self).__init__(led,start,end)
		self.red = 1

	def step(self,amt=1):
		self._led.fill((0,0,0))
		self._led.update()
		if self.red:
			color = (0,255,0)
			self.red = 0
		else:
			color = (255,0,0)
			self.red = 1

		for x in range(0,100,10):
				self._led.fill(color,x,x+5)


		self._led.update()
		self._step += amt


#test = rainbow(leds) #Searchlights.Searchlights(leds)
#test.run(fps=20)

column = 0

if column >= 20:
	column = 0
else:
	column += 1

matrix.drawLine(x0=0,y0=19,x1=7,y1=19,color=(0,0,255))
matrix.update()

"""
^ y axis 
|
|
|
|
|
|
-----------------> x axis



"""


"""
while True:

	leds.fill((255,0,0),start=0,end=-1)

	leds.update()

	time.sleep(1)

	leds.fill((0,255,0),start=0,end=-1)

	leds.update()
	time.sleep(1)

	leds.fill((0,0,255))
	leds.update()

	time.sleep(1)

	#time.sleep(.5)
"""
