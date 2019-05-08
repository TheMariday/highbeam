from led_harness import LedHarness
import numpy as np


def sphere_overlap(pos1, pos2, r1, r2):
    """
    double_overlap(pos1, pos2, r1, r2)
    Calculate the overlap volume of two spheres of radius r1, r2, at positions
        pos1, pos2
    """
    d = sum((np.array(pos1) - np.array(pos2)) ** 2) ** 0.5
    # check they overlap
    if d >= (r1 + r2):
        return 0
    # check if one entirely holds the other
    if r1 > (d + r2):  # 2 is entirely contained in one
        return 4. / 3. * np.pi * r2 ** 3
    if r2 > (d + r1):  # 1 is entirely contained in one
        return 4. / 3. * np.pi * r1 ** 3

    vol = (np.pi * (r1 + r2 - d) ** 2 * (d ** 2 + (2 * d * r1 - 3 * r1 ** 2 +
                                                   2 * d * r2 - 3 * r2 ** 2)
                                         + 6 * r1 * r2)) / (12 * d)
    return vol


h = LedHarness()

led_intersectionality = {}

for a in h.leds:
    intersections = []
    for b in h.leds:
        if ("position" in h.leds[a]) and ("position" in h.leds[b]) and (a != b):
            intersect = sphere_overlap(h.leds[a]["position"], h.leds[b]["position"], h.leds[a]["spread"], h.leds[b]["spread"])
            if intersect > 0:
                effect = intersect**2 / ((h.leds[a]["spread"]**3) * ((4*np.pi)/3.0)**2 * (h.leds[a]["spread"]**3))
                intersections.append(effect)

    led_intersectionality[a] = sum(intersections)

# import matplotlib.pyplot as plt

# n, bins, patches = plt.hist(x=led_intersectionality.values(), bins=100)
#
# plt.show()
#
#
# from PIL import Image, ImageDraw
#
# img = Image.new("RGB", (500, 500), color="black")
# pixels = img.load()
# for led_id in led_intersectionality:
#
#     if "front" in leds[led_id]["maps"]:
#         u, v = leds[led_id]["maps"]["front"]
#         b = 255-int(min(255*(led_intersectionality[led_id]/1.5), 255))
#         pixels[int(u*500), int(500-v*500)] = (b, b, b)
# img.save('pil_red.png')