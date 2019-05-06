#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc, time, json
import numpy as np
numLEDs = 512
client = opc.Client('localhost:7890')

current_id = 0

store = json.load(open('id_store.json'))

# store = [""]*512
print(store)

try:
	while True:
			pixels = [ (0,0,0) ] * numLEDs
			pixels[current_id] = (128, 128, 128)
			
			client.put_pixels(pixels)
			client.put_pixels(pixels)

			msg = "%i: " % current_id

			if store[current_id] != "":
				msg = "%i (%s): " % (current_id, store[current_id])

			a = input(msg)


			if a == "":
				current_id += 1
			elif a == "-":
				current_id -= 1
			elif a.startswith("+"):
				current_id += int(a[1:])
			elif a.startswith("-"):
				current_id -= int(a[1:])
			elif a.startswith("="):
				current_id = int(a[1:])
			elif a.startswith("f"):
				current_id = store.index(a[1:])
			elif a == "quit":
				break
			else:
				store[current_id] = a
				current_id += 1
finally:
	with open('id_store.json', 'w') as outfile:
		json.dump(list(store), outfile)

	pixels = [ (0,0,0) ] * numLEDs
	client.put_pixels(pixels)
	client.put_pixels(pixels)