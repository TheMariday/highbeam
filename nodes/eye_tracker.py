"""        controls pupil position
        listens to:
            pose [quat]
        broadcasts:
            pupil_location [rx, ry, lx, ly, 0..1]
            look_target [x, y, z]"""