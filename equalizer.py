#!/usr/bin/env python

import numpy as np

from bibliopixel.drivers.SPI import SPI
from bibliopixel.drivers.channel_order import ChannelOrder
from bibliopixel.layout.matrix import Matrix
from bibliopixel import colors

from playback.iomanager import IOManager
from audio.processor import AudioProcessor
import utils

class Equalizer(object):

    def __init__(self):
        self.io_manager = IOManager()
        self.audio_processor = AudioProcessor()
        self.driver = SPI(ledtype='LPD8806', num=160, dev='/dev/spidev0.0', c_order=ChannelOrder.RGB, spi_speed=16)
        self.matrix = Matrix(self.driver, width=20, height=8, threadedUpdate=True, rotation=1, serpentine=False)

    def use_shairport(self):
        self.io_manager.start_shairport_sync()

    def run(self):
        try:
            color_position = 0
            while True:
                # Read and write the data
                data = self.io_manager.read()
                self.io_manager.write(data)

                if len(data):
                    brightness = self.audio_processor.get_visualizer_array(data, self.io_manager.chunk, self.io_manager.rate)
                    color_arr = colors.hue_helper(color_position, 20, 2)

                    for i in np.arange(0, 20):
                        self.matrix.drawLine(x0=0, y0=i, x1=brightness[i] ** 7, y1=i, color=color_arr[i])
                        self.matrix.drawLine(x0=brightness[i] ** 7, y0=i, x1=7, y1=i, color=(0, 0, 0))
                    self.matrix.update()

                    if color_position >= 255:
                        color_position = 0
                    else:
                        color_position += 1
                else:
                    # If we didn't get any data, blank out the screen so residual data is not left there.
                    self.matrix.fill((0,0,0), 0, -1)

                    if not self.io_manager.is_input_alive():
                        self.io_manager.start_shairport_sync()

        except KeyboardInterrupt:
            print("Goodbye :)")
    
    
if __name__ == '__main__':
    args = utils.get_commandline_args()
    equalizer = Equalizer()

    if args.use_shairport:
        equalizer.use_shairport()

    equalizer.run()
