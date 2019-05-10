"""
Node list:
    effect_controller.py
        eyes & rgb leds
        controls and stores effects to be launched
        can be controlled directly
        listens to:
            start_effect [effect_name]
            stop_effect [effect_name]
            stop_all
            pupil_location [rx, ry, lx, ly, 0..1]
            overlay_colour [r, g, b]
            set_frame_rate [0..120]
            brightness [value]

    eye_controller.py:
        controls pupil position
        listens to:
            pose [quat]
        broadcasts:
            pupil_location [rx, ry, lx, ly, 0..1]
            look_target [x, y, z]

    localisation.py
        provides IMU readings for moving the 3d points
        also provides temp info
        listens to:
            recenter_pose
        broadcasts:
            pose [quat]
            temp [degrees]
            acceleration [x, y, z in dps]
            gyro [x, y, z in mps]

    button_box.py
        provides button and knob inputs
        broadcasts:
            button [id, action]
            knob [value, direction]
            start_effect [effect_name, args]3

effect ideas:
    flash mask
    wipe mask
    rainbow
    eye flash
    eye spin
    frowny face

effect_struct
    frame_rate = int
    type = full, fadeout
    mask = True / False
"""