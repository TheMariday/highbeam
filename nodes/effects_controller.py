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

        self.node.ui.add_text("effects_running", order=99)

        for i, e in enumerate(effects):
            self.node.ui.add_button("%s_launch" % e.name, e.name, "launch_effect", data=e.name, order=i*2)
            self.node.ui.add_button("%s_stop" % e.name, e.name, "stop_effect", data=e.name, order=i*2+1)
            self.effects[e.name] = e

        self.update_ui()

    def update_ui(self):
        running = [e.name for e in self.effects_stack]
        self.node.ui.get("effects_running")["text"] = "Effects Running:\n%s" + "\n".join(running)
        self.node.ui.update()

    def stop_effect(self, msg):
        self.effects_stack = [e for e in self.effects_stack if e.name != msg["data"]]
        self.update_ui()

    def launch_effect(self, msg):
        effect_name = msg["data"]
        if effect_name in self.effects:
            effect = self.effects[effect_name](self.harness)
            self.effects_stack.append(effect)
            self.update_ui()
        else:
            logging.error("%s not found" % effect_name)

    def run(self):
        while self.node.running:
            colours = {}
            for effect in self.effects_stack:
                if effect.running:
                    effect.colours = {}
                    effect.update()
                    colours.update(effect.colours)
                else:
                    self.effects_stack.remove(effect)
                    self.update_ui()

            self.harness.set_colours(colours)
            time.sleep(1/60)


if __name__ == "__main__":

    from effects import Level, Wave

    c = Controller(Level, Wave)

    c.run()