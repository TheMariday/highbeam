import CostumePy
import time
from Adafruit_BNO055 import BNO055
from mathutils import Quaternion
bno = BNO055.BNO055()

if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')


def calibrate_rotation(_):
    global calibration, raw
    calibration = Quaternion([raw.w, raw.x, raw.y, raw.z])


calibration = Quaternion([1, 0, 0, 0])
raw = Quaternion([1, 0, 0, 0])
corrected = Quaternion([1, 0, 0, 0])
node = CostumePy.new_node("localiser")

node.ui.add_button("calibrate_rotation", "Calibrate", "calibrate_rotation")
node.ui.add_text("orientation")
node.ui.add_text("temperature")
node.ui.update()

node.listen("calibrate_rotation", calibrate_rotation)

if __name__ == "__main__":

    while node.running:

        for _ in range(30):
            x, y, z, w = bno.read_quaternion()
            raw = Quaternion([w, x, y, z])
            corrected = raw.rotation_difference(calibration)

            node.broadcast("orientation", [corrected.w, corrected.x, corrected.y, corrected.z])

            time.sleep(1/30.0)

        e = corrected.to_euler()
        node.ui.get("orientation")["text"] = "Orientation: %f %f %f" % (e.x, e.y, e.z)
        temperature = bno.read_temp()
        node.ui.get("temperature")["text"] = "Temperature: %f" % temperature
        node.broadcast("head_internal_temperature", temperature)
        node.ui.update()

