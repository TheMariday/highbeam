import math


class Alignment:

    def __int__(self):
        self.band = 5

    def update(self, t, h):

        for led_name in h.leds:
            x, y, z = h.leds[led_name]["position"]
            x_dist = abs(t*10 - x)
            y_dist = abs(t*10 - y)
            z_dist = abs(t*10 - z)
            xb = max(-x_dist / self.band + 1, 0)*255
            yb = max(-y_dist / self.band + 1, 0)*255
            zb = max(-z_dist / self.band + 1, 0)*255
            if sum([xb, yb, zb]) < 16*3:
                h.leds[led_name]["colour"] = [xb, yb, zb]

        if t > 25:
            return None
        else:
            return h


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
            v3 = self.get_swirl_brightness(x, y, timestep + 20)  # TODO not sure if this should be y or z
            h.leds[led_id]["colour"] = [v1*255, v2*255, v3*255]
