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

    def __init__(self, *effects):
        self.node = CostumePy.new_node("LED_Controller")
        self.effects = {}
        self.effects_stack = []
        self.harness = NotImplemented

        self.node.listen("launch_effect")

        self.node.ui.add_text("effects_running")

        for effect in effects:
            name = effects.__class__.__name__
            self.node.ui.add_button("%s_button" % name, name, "launch_effect", data=name)
            self.effects[name] = effect

        self.update_ui()

    def update_ui(self):
        running = [e.__class__.__name__ for e in self.effects_stack]
        self.node.ui.get("effects_running")["text"] = "Effects Running:\n%s" + "\n".join(running)
        self.node.ui.update()

    def launch_effect(self, msg):
        effect_name = msg["data"]
        effect = self.effects[effect_name](self.harness)
        self.effects_stack.append(effect)
        self.update_ui()

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
            return colours


if __name__ == "__main__":

    from effects import Level, Wave

    c = Controller(Level, Wave)

    c.run()