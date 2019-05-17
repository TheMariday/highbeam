from __future__ import division

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

# from led_harness import LedHarness
# import numpy as np
# import time
#
# h = LedHarness()
#
# h.set_brightness(1)
#
# i = 0
# band = 5
# c = 1
#
# try:
#     while True:
#         pixels = np.zeros((512, 3))
#
#         for led_name in h.leds:
#             led = h.leds[led_name]
#             address = led["hardware_id"]
#
#             x, y, z = led["position"]
#             x_dist = abs(i - x)
#             y_dist = abs(i - y)
#             z_dist = abs(i - z)
#             xb = max(-x_dist / band + 1, 0)
#             yb = max(-y_dist / band + 1, 0)
#             zb = max(-z_dist / band + 1, 0)
#             pixels[address] = [128 * xb, 128 * yb, 128 * zb]
#
#         h.render(pixels)
#
#         time.sleep(1 / 60.0)
#
#         if not (abs(i) <= 27.38 / 2):
#             c = -c
#
#         i += .1 * c
# finally:
#     h.quit()

if __name__ == "__main__":
    import numpy as np

    def buf_display(buf):
        out_str = ""
        for x in range(9):
            for y in range(16):
                out_str += "###" if buf[x, y] else "---"
                out_str += "\t|\t" if y == 7 else ""
            out_str += "\n"
        print(out_str)

    buf = np.zeros((9, 16))

    buf_display(buf)

    circle_center = np.array([4, 0, 0, 0])
    stretch = 3/4
    lec = circle_center[:2] + np.array([9/2, 3.5])
    rec = circle_center[2:] + np.array([9/2, 11.5])

    cs = 2.3

    for x in range(9):
        for y in range(8):
            d2l = np.linalg.norm(lec - np.array([((x - 9/2)*stretch) + 9/2, y]))
            buf[x, y] = int(d2l < cs)

        for y in range(8, 16):
            d2r = np.linalg.norm(rec - np.array([((x - 9/2)*stretch) + 9/2, y]))
            buf[x, y] = int(d2r < cs)

    buf_display(buf)
