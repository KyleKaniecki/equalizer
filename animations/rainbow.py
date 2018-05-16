from bibliopixel.animation import BaseStripAnim
from bibliopixel import colors


class rainbow(BaseStripAnim):

	def __init__(self,led,start=0,end=-1):
		super(rainbow,self).__init__(led,start,end)

	def step(self,amt=1):
		self._led.fill(colors.hue2rgb_360(self._step))
		self._led.update()

		self._step += amt

		if self._step > 255:
			self._step = 0