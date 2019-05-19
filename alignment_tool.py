#!/usr/bin/env python

# Light each LED in sequence, and repeat.
import sys

#sys.path.append("D:\\Users\\Sam\\GIT\\HighBeam\\fadecandy\\examples\\python")
import opc, time, json
import numpy as np
from pprint import pprint
#numLEDs = 512
client = opc.Client('localhost:7890')

#led_id_lookup = json.load(open('mapping\\led_hardware_index.json'))
#led_info = json.load(open("mapping\\led_info.json"))

#led_id_lookup = ["LED.%s" % l for l in led_id_lookup]

#for led_name in led_info:
#	led_address = led_id_lookup.index(led_name)
#	led_info[led_name]["address"] = led_address


# pprint(led_info)

# quit()

from led_harness import LedHarness

h = LedHarness()

i = -30
band = 5

try:
	while True:
#			pixels = [ [0,0,0] ] * numLEDs
			
			for led_name in h.leds:
				led = h.leds[led_name]
				#address = led["address"]
				#if "position" not in led:
				#	pprint(led)
				#	led["position"] = led["position_actual"]

				x, y, z = led["position"]
				x_dist = abs(i - x)
				y_dist = abs(i - y)
				z_dist = abs(i - z)
				xb = max(-x_dist/band + 1, 0)
				yb = max(-y_dist/band + 1, 0)
				zb = max(-z_dist/band + 1, 0)
				h.leds[led_name]["colour"] = [128*xb,128*yb,128*zb]
			
#			client.put_pixels(pixels)
			# client.put_pixels(pixels)

			time.sleep(1/60.0)

			if i > 25:
				i = -30

			i += .1
finally:
	#pixels = [ (0,0,0) ] * numLEDs
	#client.put_pixels(pixels)
	#client.put_pixels(pixels)
	h.quit()
