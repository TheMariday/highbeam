import math
import random

class Alignment:

    def __init__(self):
        self.band = 5

    def update(self, t, h):

        band_pos = t*10-20

        for led_name in h.leds:
            x, y, z = h.leds[led_name]["position"]
            x_dist = abs(band_pos - x)
            y_dist = abs(band_pos - y)
            z_dist = abs(band_pos - z)
            xb = max(-x_dist / self.band + 1, 0)*255
            yb = max(-y_dist / self.band + 1, 0)*255
            zb = max(-z_dist / self.band + 1, 0)*255
            col = [xb, yb, zb]
            if sum(col) > 32*3:
                h.leds[led_name]["colour"] = col

        if t > 4:
            return True


class Swirl:

    def get_swirl_brightness(self, x, y, step):
        y += 2
        dist = math.sqrt(pow(x, 2) + pow(y, 2))

        angle = (step / 10.0) + dist / 1.5

        s = math.sin(angle)
        c = math.cos(angle)

        xs = x * c - y * s
        ys = x * s + y * c

        r = abs(xs + ys)

        return max(0.0, 1 - min(1.0, r / 20.0))

    def update(self, t, h):

        timestep = (t/18)*-200

        for led_id in h.leds:
            x, y, z = h.leds[led_id]["position"]
            v1 = self.get_swirl_brightness(x, z, timestep)
            v2 = self.get_swirl_brightness(x, z, timestep + 10)
            v3 = self.get_swirl_brightness(x, z, timestep + 20)
            h.leds[led_id]["colour"] = [v1*255, v2*255, v3*255]


class BrokenSwirl(Swirl):

    def update(self, t, h):

        timestep = (t/18)*-200

        for led_id in h.leds:
            x, y, z = h.leds[led_id]["position"]
            v1 = self.get_swirl_brightness(x, y, timestep)
            v2 = self.get_swirl_brightness(y, z, timestep + 10)
            v3 = self.get_swirl_brightness(z, x, timestep + 20)
            h.leds[led_id]["colour"] = [v1*255, v2*255, v3*255]


class AllOff:

    def update(self, _, h):

        for led_id in h.leds:
            h.leds[led_id]["colour"] = [0, 0, 0]


class EyesOff:

    def update(self, _, h):
        for led_id in h.leds:
            if h.leds[led_id]["type"] == "mat":
                h.leds[led_id]["colour"] = [0, 0, 0]


class Random:

    def update(self, _, h):

        for led_id in h.leds:
            h.leds[led_id]["colour"] = [random.random()*255, random.random()*255, random.random()*255]


class Sparkle:

    def update(self, _, h):

        for led_id in h.leds:
            if random.random() > .99:
                h.leds[led_id]["colour"] = [255, 255, 255]


class Epilepsy:

    def __init__(self):
        self.cycle_count = 0
        self.tog = True
        self.cycle = [[255, 0, 0],
                      [0, 255, 0],
                      [0, 0, 255],
                      [255, 0, 255],
                      [0, 255, 255],
                      [255, 255, 0],
                      [255, 255, 255],
                      ]

    def update(self, _, h):

        self.cycle_count += 1
        self.tog = not self.tog

        if self.tog:
            for led_id in h.leds:
                h.leds[led_id]["colour"] = self.cycle[self.cycle_count % len(self.cycle)]
