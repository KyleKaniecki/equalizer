from bibliopixel.animation import BaseStripAnim


class Police(BaseStripAnim):

    def __init__(self, led, start=0, end=-1):
        super(Police, self).__init__(led, start, end)
        self.red = 1

    def step(self, amt=1):
        self._led.fill((0, 0, 0))
        self._led.update()

        if self.red:
            color = (0, 255, 0)
            self.red = 0
        else:
            color = (255, 0, 0)
            self.red = 1

        for x in range(0, 100, 10):
            self._led.fill(color, x, x + 5)

        self._led.update()
        self._step += amt
