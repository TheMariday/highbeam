"""        eyes & rgb leds
        controls and stores effects to be launched
        can be controlled directly
        listens to:
            start_effect [effect_name]
            stop_effect [effect_name]
            stop_all
            pupil_location [rx, ry, lx, ly, 0..1]
            overlay_colour [r, g, b]
            set_frame_rate [0..120]
            brightness [value]"""

import CostumePy


class Controller:

    def __init__(self):
        self.node = CostumePy.new_node("LED_Controller")


if __name__ == "__main__":

    controller = Controller()