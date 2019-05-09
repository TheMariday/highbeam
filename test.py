
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


if __name__ == "__main__":

    from led_harness import LedHarness
    import numpy as np
    import time

    h = LedHarness()

    i = -30
    band = 15

    try:
        while True:
            pixels = np.zeros((512, 3))

            for led_name in h.leds:
                led = h.leds[led_name]
                address = led["hardware_id"]

                x, y, z = led["position"]
                x_dist = abs(i - x)
                y_dist = abs(i - y)
                z_dist = abs(i - z)
                xb = max(-x_dist / band + 1, 0)
                yb = max(-y_dist / band + 1, 0)
                zb = max(-z_dist / band + 1, 0)
                pixels[address] = [128 * xb, 128 * yb, 128 * zb]

            h.render(pixels)

            time.sleep(1 / 60.0)

            if i > 25:
                i = -30

            i += 2
    finally:
        h.quit()
