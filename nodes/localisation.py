import CostumePy
import time


def calibrate_rotation(_):
    global calibration, orientation
    calibration = orientation


calibration = [1, 0, 0, 0]
orientation = [1, 0, 0, 0]
temperature = 0

node = CostumePy.new_node("localiser")

node.ui.add_button("calibrate_rotation", "Calibrate", "calibrate_rotation")
node.ui.add_text("orientation")
node.ui.add_text("temperature")
node.ui.update()

node.listen("calibrate_rotation", calibration)

if __name__ == "__main__":

    while node.running:

        for _ in range(30):
            orientation = NotImplemented
            temperature = NotImplemented

            if calibration:
                node.broadcast("orientation", orientation * calibration)
            else:
                node.broadcast("orientation", orientation)

            time.sleep(1/30.0)

        node.broadcast("head_internal_temperature", temperature)

        node.ui.get("orientation")["text"] = "Orientation: %r" % orientation
        node.ui.get("temperature")["text"] = "Temperature: %f" % temperature
        node.ui.update()

