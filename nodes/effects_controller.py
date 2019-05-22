import os
import sys
sys.path.append(os.getcwd())  # Don't ask...

import logging
import CostumePy
import time
from led_harness import LedHarness


class Controller:

    def __init__(self, *effects):
        self.node = CostumePy.new_node("LED_Controller")
        self.effects = {}
        self.effects_stack = []
        self.harness = LedHarness()

        self.node.listen("launch_effect", self.launch_effect)
        self.node.listen("stop_effect", self.stop_effect)
        self.node.listen("stop_all", self.stop_all)
        self.node.listen("brightness_change", self.change_brightness)
        self.node.listen("eye_brightness_change", self.change_eye_brightness)

        self.node.ui.add_button("stop_all", text="Stop All", topic="stop_all", order=0, button_class="btn-danger")
        self.node.ui.add_button("decrease_brightness", text="Suit -", topic="brightness_change", data=False, order=1, button_class="btn-info")
        self.node.ui.add_button("increase_brightness", text="Suit +", topic="brightness_change", data=True, order=2, button_class="btn-warning")

        self.node.ui.add_button("decrease_eye_brightness", text="Eyes -", topic="eye_brightness_change", data=False, order=3, button_class="btn-info")
        self.node.ui.add_button("increase_eye_brightness", text="Eyes +", topic="eye_brightness_change", data=True, order=4, button_class="btn-warning")

        self.node.ui.add_text("brightness", order=5)

        self.node.ui.add_text("effects_running", order=7)

        for i, effect in enumerate(effects):
            name = effect.__name__
            self.node.ui.add_break("%s_break" % name, order=i*4+10)
            self.node.ui.add_text("%s_text" % name, name, order=i*4+11)
            self.node.ui.add_button("%s_launch" % name, "Launch", "launch_effect", data=name, order=i*4+12, button_class="btn-success")
            self.node.ui.add_button("%s_stop" % name, "Stop", "stop_effect", data=name, order=i*4+13, button_class="btn-danger")
            self.node.ui.get("%s_stop" % name)["enabled"] = False
            self.effects[name] = effect

        self.update_ui()

    def stop_all(self, msg):
        self.effects_stack = []
        self.harness.quit()
        self.update_ui()

    def change_eye_brightness(self, msg):
        self.harness.change_eye_brightness(.1 if msg["data"] else -.1)
        self.update_ui()

    def change_brightness(self, msg):
        self.harness.change_brightness(.1 if msg["data"] else -.1)
        self.update_ui()

    def update_ui(self):
        running = [e.__class__.__name__ for e in self.effects_stack]
        for e in self.effects:
            if e in running:
                self.node.ui.get("%s_launch" % e)["button_class"] = "btn-success"
                self.node.ui.get("%s_stop" % e)["enabled"] = True
            else:
                self.node.ui.get("%s_launch" % e)["button_class"] = "btn-default"
                self.node.ui.get("%s_stop" % e)["enabled"] = False
        self.node.ui.get("effects_running")["text"] = "Effects Running: %s" % " -> ".join(running)
        self.node.ui.get("brightness")["text"] = "Suit: %i%% Eyes: %i%%" % (self.harness.get_brightness()*100, self.harness.get_eye_brightness()*100)
        self.node.ui.update()

    def stop_effect(self, msg):
        self.effects_stack = [e for e in self.effects_stack if e.__class__.__name__ != msg["data"]]
        self.update_ui()

    def launch_effect(self, msg):
        effect_name = msg["data"]
        if effect_name in self.effects:
            effect = self.effects[effect_name]
            e = effect()
            e.start_time = time.time()
            self.effects_stack.append(e)
            self.update_ui()
        else:
            logging.error("%s not found" % effect_name)

    def run(self):
        while self.node.running:
            for led_id in self.harness.leds:
                self.harness.leds[led_id]["colour"] = [0, 0, 0]
            for i, effect in enumerate(self.effects_stack):
                stopped = effect.update(time.time()-effect.start_time, self.harness)
                if stopped == True:
                    del self.effects_stack[i]
                    self.update_ui()

            self.harness.render()


if __name__ == "__main__":

    from effects import Swirl, Alignment, Epilepsy, Sparkle, Random, EyesOff, AllOff, BrokenSwirl

    c = Controller(Swirl, Alignment, Epilepsy, Sparkle, Random, EyesOff, AllOff, BrokenSwirl)

    c.run()
