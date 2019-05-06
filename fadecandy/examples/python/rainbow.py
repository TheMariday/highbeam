#!/usr/bin/env python

# Burn-in test: Keep LEDs at full brightness most of the time, but dim periodically
# so it's clear when there's a problem.

import opc, time, math, random
import numpy as np


numLEDs = 512
client = opc.Client('localhost:7890')

brightness = .2

pink = (255, 134, 247)
green = (17, 255, 141)

allGreen = np.full((512,3), green)*brightness
allPink = np.full((512,3), pink)*brightness


i = 0
try:
	while True:
		frame = np.random.random((512,3))
		# frame = np.full((512, 3), np.random.random((3)))
		for i in range(512):
			frame[i] = (frame[i]*3)/sum(frame[i])

		frame *= 255*brightness
		frame = frame.astype(int)
		client.put_pixels(frame)
		# client.put_pixels(frame)

		time.sleep(1)
except:
	killframe = np.zeros((512,3))
	print(killframe)
	client.put_pixels(killframe)
	client.put_pixels(killframe)