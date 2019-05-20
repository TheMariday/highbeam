#!/usr/bin/env python

import time
import math

#import scrollphathd
from led_harness import LedHarness

h = LedHarness()

print("""
Scroll pHAT HD: Swirl

Displays a basic demo-scene style pattern.

Press Ctrl+C to exit!

""")


def swirl(x, y, step):
    #x -= (scrollphathd.DISPLAY_HEIGHT / 2.0)
    #y -= (scrollphathd.DISPLAY_WIDTH / 2.0)
    y += 2
    dist = math.sqrt(pow(x, 2) + pow(y, 2))

    angle = (step / 10.0) + dist / 1.5

    s = math.sin(angle)
    c = math.cos(angle)

    xs = x * c - y * s
    ys = x * s + y * c

    r = abs(xs + ys)

    return max(0.0, 1 - min(1.0, r / 20.0))


#scrollphathd.set_brightness(0.8)

while True:
    #timestep = math.sin(time.time() / 18) * 1500
    timestep = (time.time()/18)*-200
    #timestep = (time.time()%36)*1500

    for led_id in h.leds:
         x, y, z = h.leds[led_id]["position"]
         v1 = swirl(x, z, timestep)
         v2 = swirl(x,z, timestep+10)
         v3 = swirl(x,y, timestep+20)
         h.leds[led_id]["colour"] = [v1*255, v2*255, v3*255]

    #for x in range(0, scrollphathd.DISPLAY_HEIGHT):
    #    for y in range(0, scrollphathd.DISPLAY_WIDTH):
    #        v = swirl(x, y, timestep)
    #        scrollphathd.pixel(x, y, v)

    time.sleep(0.001)
    h.render()
    #scrollphathd.show()
    #print(scrollphathd.buf.shape)
