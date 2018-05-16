#!/usr/bin/env python

import fft
from IOManager import IOManager
from leds.LEDManager import LEDManager

from bibliopixel import colors
from bibliopixel.drivers.LPD8806 import *
from bibliopixel import led

def wire():

    io = IOManager()
    #leds = LEDManager()
    ap = fft.AudioProcessor()

    driver = DriverLPD8806(160,c_order=ChannelOrder.RGB,use_py_spi=True,dev="/dev/spidev0.0",SPISpeed=16)
    ledmatrix = led.LEDMatrix(driver,width=20,height=8,threadedUpdate=True,rotation=1,serpentine=False)

    io.start_stream()

    update = 0
    count = 0.0

    while True:
        #This reads the data from the input stream 
        data = io.read()
    
        #This writes the data out to the hardware audio out port
        
        io.write(data)

        
        if len(data):
            brightness = ap.get_visualizer_array(data,io.chunk,io.rate)

            if update == 0:
                update = 10
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
        else:
        	ledmatrix.fillScreen(color=(0,0,0))
            




if __name__ == "__main__":
    wire()
