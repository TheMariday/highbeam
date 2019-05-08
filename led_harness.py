import os
import json
import sys
import numpy as np
from PIL import Image

local_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(local_path + "/fadecandy/examples/python/")

import opc


def get_led_info():

    led_placement = json.load(open(local_path + "/mapping/led_info.json"))
    led_hw_id = ["LED." + i for i in json.load(open(local_path + "/mapping/led_hardware_index.json"))]
    density = json.load(open(local_path + "/mapping/led_density.json"))
    for led_id in led_placement:
        led_placement[led_id]["hardware_id"] = led_hw_id.index(led_id)
        led_placement[led_id]["density"] = density
        # led_placement[led_id]["colour"] = [0, 0, 0]

    return led_placement


class LedHarness:

    def __init__(self):
        self.leds = get_led_info()
        self.client = opc.Client('localhost:7890')
        self.uv_maps = ["side", "front"]  # order = bottom to top of layers
        self.max_amp = 5
        self.max_rgb = ((self.max_amp*1000)/60.0)*255*3  # max amp 10 amps = 60ma each

    def image_2_colour_array(self, image_filepath):
        led_colours = np.zeros((512, 3))

        img = Image.open(image_filepath)
        pixels = img.load()

        for map_name in self.uv_maps:
            for led_id in self.leds:
                led = self.leds[led_id]
                if map_name in led["maps"]:
                    u, v = led["maps"][map_name]
                    x, y = int(u*img.width), int((1-v)*img.height)
                    rgba = pixels[x, y]
                    r = rgba[3]/255.0
                    led_colours[led["hardware_id"]] = [led_colours[led["hardware_id"]][i]*(1-r) + rgba[i]*r for i in range(3)]
                else:
                    print("can't find mapping for %s" % led_id)

        return led_colours

    def colour_array_info(self, colour_array):
        c = np.array(colour_array)
        print("sum:", np.sum(c))
        print("percentage sum:", np.sum(c)/self.max_rgb)
        print("max:", np.max(c))
        print("full brightness equiv:", np.sum(c)/(3*255))

    def render(self, led_array, instant=False):

        led_array = np.array(led_array)

        if np.sum(led_array) > self.max_rgb:
            ratio = float(self.max_rgb) / np.sum(led_array)
            print("overloaded, capping to %f" % ratio)
            led_array *= ratio

        self.client.put_pixels(led_array)
        if instant:
            self.client.put_pixels(led_array)

    def quit(self):
        self.render(np.zeros((512, 3)), instant=True)
