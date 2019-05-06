#!/usr/bin/env python

# Burn-in test: Keep LEDs at full brightness most of the time, but dim periodically
# so it's clear when there's a problem.

import opc, time, math, random
import numpy as np



numLEDs = 512
client = opc.Client('localhost:7890')

brightness = .3

bpm = 124
killframe = np.zeros((512,3))

i = 0
try:
	while True:
		frame = np.random.random((512,3))
		frame *= 255*brightness
		frame = frame.astype(int)
		client.put_pixels(frame)
		client.put_pixels(frame)
		time.sleep((30.0)/(bpm))
		client.put_pixels(killframe)
		client.put_pixels(killframe)
		time.sleep((30.0)/(bpm))
except:
	print(killframe)
	client.put_pixels(killframe)
	client.put_pixels(killframe)