import time

class base_effect:
    def __init__(self, harness):
        self.harness = harness
        self.start_time = time.time()
        self.colours = {}
        self.running = True
        self.name = self.__class__.__name__

    def set_colour(self, led_id, colour):
        self.colours[led_id] = colour

    def update(self, time):
        return self.colours

    def finished(self):
        self.running = False
        return self.colours


class Level(base_effect):

    def update(self, time):
        for led_id in self.harness.leds:
            led = self.harness.leds[led_id]
            if -5 < led["position"][0] < 0:
                self.set_colour(led_id, [0, 0, 255])


class Wave(base_effect):

    def update(self, time):
        for led_id in self.harness.leds:
            led = self.harness.leds[led_id]

            band_center = (time*30)/10
            if band_center > 20:
                self.finished()
            if band_center - 2.5 < led["position"][1] < band_center + 2.5:
                self.set_colour(led_id, [0, 0, 255])
