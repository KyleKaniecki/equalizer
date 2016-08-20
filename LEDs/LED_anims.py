
from bibliopixel.drivers.LPD8806 import *
from bibliopixel import led
from bibliopixel import animation
from bibliopixel import colors
import time
import random
import colorsys

def pre_show():
    for i in range(0,160):
        _leds.set(i,colors.Plaid)

    _leds.update()
        

    
def Color_all(Color):
    for i in range(0,160):
        _leds.set(i,Color)
    _leds.update()
    
def Clear():
    for i in range(0,160):
        _leds.set(i,(0,0,0))

    _leds.update()

#-----------------------------------------------------------------------------

class bouncing_lazer(animation.BaseStripAnim):
    
    def __init__(self, led, start=0, end=-1):
        super(bouncing_lazer,self).__init__(led,start,end)
        self._colors = [colors.Red,colors.Teal, colors.DarkCyan, colors.Violet, colors.Amethyst, colors.GreenYellow]

    def step(self, amt=1):
        Clear()
        for i in range(self._step,self._step+5):
                if i >= 160:
                    self._step = 0
                    self._led.set(i-159,self._colors[random.randint(0,5)])
                else:
                    self._led.set(i,self._colors[random.randint(0,5)])
        self._step += amt

class multiple_lazers(animation.BaseStripAnim):
    
    def __init__(self, led,start=0, end=-1):
        super(multiple_lazers,self).__init__(led,start,end)
        self._colors = []
        self.counter = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160]
        

    def step(self, amt=1):
        Clear()
        for i in range(0, len(self.counter)):
            color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            for j in range(0,5):
                self._led.set(self.counter[i]-j,color)
            if(self.counter[i] >= 160):
                self.counter[i] = 0
            else:
                self.counter[i]+=1
        self._step += amt

class alternation(animation.BaseStripAnim):
    def __init__(self,led,start,end):
        super(alternation,self).__init__(led,start,end)
        self.odds = True
        
    def step(self, amt= 1):
        Clear()
        if(self.odds == True):
            for i in range(0,160,2):
                self._led.set(i,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            self.odds = False
        else:
            for i in range(1,160,2):
                self._led.set(i,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            self.odds = True
        self._step += amt
        
class glimmer(animation.BaseStripAnim):
    def __init__(self,led,start,end):
        super(glimmer,self).__init__(led,start,end)
        
    def step(self, amt=1):
        for i in range(0,160):
            temp = self._led.get(i)
            if(temp[0]-10 < 0):
                self._led.set(i,(0,0,0))
            else:
                self._led.set(i,(temp[0]-10,temp[1]-10,temp[2]-10))
        for i in range(0,5):
            self._led.set(random.randint(0,160),(175,175,175))

        self._step += amt

class stack(animation.BaseStripAnim):
    def __init__(self,led,start,end):
        super(stack,self).__init__(led,start,end)
        self.current = 0
        self.stop = 160
        self.color = (255,0,0)

    def step(self, amt=1):
        if self.current >= self.stop:
            self.current = 0
            self.stop -= 5
            self._step += amt
            self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            
        for i in range(self.current, self.current-5,-1):
            self._led.set(i,self.color)
        for i in range(self.current-5, self.current-10, -1):
            self._led.set(i,(0,0,0))
        self.current += 5

        if(self.stop <= 0):
            self.current = 0
            self.stop = 160
            Clear()


class fade(animation.BaseStripAnim):
    def __init__(self,led,start,end):
        super(fade,self).__init__(led,start,end)
        self._led.fill((125,125,125),start=0,end=-1)
        self.current = 0
        self.add = True
        
    def step(self, amt=1):
        print(self._led.get(0))
        #time.sleep(2)
        self.temp = list(self._led.get(0))

        if self.temp[self.current] == 255 and self.add == True and self.current == 3:
            self.current -= 1
        elif self.temp[self.current] == 0 and self.add == False and self.current == 0:
            self.current += 1
        if self.add == True:
            self.temp[self.current] += 1
        else:
            self.temp[self.current] -= 1
            
            
        self.temp = tuple(self.temp)
            
        self._led.fill(self.temp,start=0,end=-1)
        amt += 1

class middle_strobe(animation.BaseStripAnim):
    def __init__(self,led,start,end):
        super(middle_strobe,self).__init__(led,start,end)
        self._led.set(80,(255,0,0))
        self.position = 5
        self.add = True
        
    def step(self, amt = 1):

        

        if(self.position >= 80):
            self.position = 0
        
            if self.add == True:
                self.add = False
            else:
                self.add = True
            

        if self.add:
            self.position += 5
            self._led.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)),(80 - self.position),(80 + self.position))
        else:
            self.position += 5
            self._led.fill((0,0,0),0,0 + self.position)
            self._led.fill((0,0,0),80-self.position, 80)
            

        self._step += amt
 
class glow(animation.BaseStripAnim):
    def __init__(self,led,start=0,end=-1,red=0,blue=0,green=175):
        super(glow,self).__init__(led,start,end)
        self.time = 0
        self.hue = colorsys.rgb_to_hsv(blue,red,green)[0]
        self.subtract = False
        self.rgbcolor = colorsys.hsv_to_rgb(self.hue,1,(int(self.time)%100)*.01)

    def step(self, amt=1):
        self._led.fill((20+int(self.rgbcolor[0]*(255-20)),int(self.rgbcolor[1]*255),int(self.rgbcolor[2]*255)))
        self.rgbcolor = colorsys.hsv_to_rgb(self.hue,1,(self.time%100)*.01)

        if self.subtract:
            self.time -= 1
            if self.time <= 0:
                self.subtract = False
        else:
            self.time += 1
            if self.time >= 99:
                self.subtract = True
        
        self._step += amt

#private variables
_driver = DriverLPD8806(160,c_order=ChannelOrder.RGB,use_py_spi=True,dev="/dev/spidev0.0",SPISpeed=2)
_leds = led.LEDStrip(_driver,threadedUpdate=True)

#public variables

bouncing_lazer_anim = bouncing_lazer(_leds,start=0,end=-1)
multiple_lazers_anim = multiple_lazers(_leds,start=0,end=-1)

alternation_anim = alternation(_leds,start=0,end=-1)

glimmer_anim = glimmer(_leds,start=0,end=-1)

stack_anim = stack(_leds,start=0,end=-1)

middle_strobe_anim = middle_strobe(_leds,start=0,end=-1)


if __name__ == "__main__":
    Clear()
    time.sleep(2)
    animation = glow(_leds,start=0,end=-1)
    animation.run(fps=60)
    #middle_strobe_anim.run(fps=30)
    
