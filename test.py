
#
# led_hardware_index.json
# [..., "323", ...]

#
#led_info.json
#
# "LED.323": {
#     "spread": 1.1231472492218018,
#     "maps": {
#         "front": [
#             0.4487215280532837,
#             0.07945242524147034
#         ],
#         "UVMap": [
#             0.0718763992190361,
#             0.33715736865997314
#         ],
#         "side": [
#             0.3793008327484131,
#             0.5983515381813049
#         ]
#     },
#     "position": [
#         -4.174649238586426,
#         -14.621893882751465,
#         -9.542781829833984
#     ],
#     "position_actual": [
#         -3.6334304809570312,
#         -14.371440887451172,
#         -8.591038703918457
#     ]

# import numpy as np
# import opc
import json
import os


def get_led_info():
    local_path = os.path.dirname(os.path.abspath(__file__))
    led_placement = json.load(open(local_path + "/mapping/led_info.json"))
    led_hw_id = ["LED." + i for i in json.load(open(local_path + "/mapping/led_hardware_index.json"))]
    for led_id in led_placement:
        led_placement[led_id]["hardware_id"] = led_hw_id.index(led_id)
        led_placement[led_id]["colour"] = [0, 0, 0]

    return led_placement


class ledHarness:

    def __init__(self):
        self.leds = get_led_info()
        # self.client = opc.Client('localhost:7890')
        self.brightness = 255

    def get_colour_array(self):
        # led_colours = np.zeros((512, 3))

        for led_id in self.leds:
            led = self.leds[led_id]
            led_colours[led["hardware_id"]] = led["colour"]

        return led_colours

    def render(self, led_array, instant=False):

        self.client.put_pixels(led_array)
        if instant:
            self.client.put_pixels(led_array)



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



if __name__ == "__main__":
    import numpy as np
    import math
    leds = get_led_info()

    r2s = (4/3)*math.pi

    led_intersectionality = {}

    for a in leds:
        intersections = []
        for b in leds:
            if ("position" in leds[a]) and ("position" in leds[b]) and (a != b):
                intersect = sphere_overlap(leds[a]["position"], leds[b]["position"], leds[a]["spread"], leds[b]["spread"])
                if intersect > 0:
                    effect = intersect**2 / (r2s*(leds[a]["spread"]**3) * r2s * (leds[a]["spread"]**3))
                    intersections.append(effect)

        led_intersectionality[a] = sum(intersections)

    # import matplotlib.pyplot as plt

    # n, bins, patches = plt.hist(x=led_intersectionality.values(), bins=100)
    #
    # plt.show()
    #

    from PIL import Image, ImageDraw

    img = Image.new("RGB", (500, 500), color="black")
    pixels = img.load()
    for led_id in led_intersectionality:

        if "front" in leds[led_id]["maps"]:
            u, v = leds[led_id]["maps"]["front"]
            b = 255-int(min(255*(led_intersectionality[led_id]/1.5), 255))
            pixels[int(u*500), int(500-v*500)] = (b, b, b)
    img.save('pil_red.png')