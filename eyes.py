import numpy as np
from mathutils import Vector, Quaternion


class Eyes:

    def __init__(self, cross_eye=0.0, default_look_distance=200, eye_fov=40):
        self.default_look_target = Vector((0, default_look_distance, 0))
        self.look_target = self.default_look_target
        self.rotation = Quaternion((1, 0, 0, 0))
        self.position = Vector((0, 0, 0))
        self.leye_pos = Vector((-5.96898, 6.09201, 3.69949))
        self.reye_pos = Vector((5.96898, 6.09201, 3.69949))
        self.leye_norm = Vector((cross_eye, 1, 0))
        self.reye_norm = Vector((-cross_eye, 1, 0))
        self.pupil_pos = np.zeros(4)  # lx ly rx ry
        self.eye_fov = eye_fov

    def set_rotation(self, rotation):
        self.rotation = rotation

    def update(self):
        self.update_pupil_pos()
        new_look_target = self.update_look_target()

        if new_look_target:
            print("blonk")
            self.look_target = new_look_target
            self.update()
        else:
            print(self.pupil_pos)

    def update_pupil_pos(self):

        leye_pos = self.leye_pos.copy()
        leye_pos.rotate(self.rotation)
        leye_pos += self.position

        reye_pos = self.reye_pos.copy()
        reye_pos.rotate(self.rotation)
        reye_pos += self.position

        leye_beam = self.look_target.copy() - leye_pos
        reye_beam = self.look_target.copy() - reye_pos

        leye_beam.rotate(self.rotation.inverted())
        leye_beam_angle = self.leye_norm.rotation_difference(leye_beam)

        reye_beam.rotate(self.rotation.inverted())
        reye_beam_angle = self.reye_norm.rotation_difference(reye_beam)

        self.pupil_pos = -1*np.degrees([leye_beam_angle.z, leye_beam_angle.x, reye_beam_angle.z, reye_beam_angle.x])

    def update_look_target(self, forced=False):
        fov = np.full(4, self.eye_fov) / np.array([2, 4, 2, 4])

        if forced or np.any(self.pupil_pos < -1*fov) or np.any(self.pupil_pos > fov):
            new_look_target = self.default_look_target.copy()
            new_look_target.rotate(self.rotation)
            new_look_target += self.position
            return new_look_target
        else:
            return False


if __name__ == "__main__":

    e = Eyes(cross_eye=-.1)

    import bpy
    for i in range(300):

        bpy.context.scene.frame_set(i)

        e.set_rotation(bpy.data.objects['imu'].rotation_quaternion)

        e.update()

        lx, ly, rx, ry = e.pupil_pos

        bpy.data.objects['l_pupil'].location = [lx / 10 - 4, ly / 10 + 40, 0]
        bpy.data.objects['l_pupil'].keyframe_insert(data_path="location")

        bpy.data.objects['r_pupil'].location = [rx / 10 + 4, ry / 10 + 40, 0]
        bpy.data.objects['r_pupil'].keyframe_insert(data_path="location")

        bpy.data.objects['look_target'].location = e.look_target
        bpy.data.objects['look_target'].keyframe_insert(data_path="location")
