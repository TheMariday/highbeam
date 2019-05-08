
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

    h = LedHarness()

    evil_face_colour_array = h.image_2_colour_array("faces/evil_2.png")

    h.colour_array_info(evil_face_colour_array)
    # max_array = np.ones((512, 3))*255/3
    h.render(evil_face_colour_array, instant=True)

    # time.sleep(2)

    # h.quit()
