import numpy as np

def computeC(time, pos, _Color1, _Color2, _Color3):



    # float p = .5*time + 0.2*pos.x + 0.1*pos.y + 0.05*pos.z;
    p = .5*time + 0.2*pos[0] + 0.1*pos[1] + 0.05*pos[2]

    # float c = sin(p)*0.7 + sin(p*3)*0.16 + sin(p*7)*0.14;
    c = np.sin(p)*0.7 + np.sin(p*3)*0.16 + np.sin(p*7)*0.14

    # p = c + pos.x * 0.1 + time * 0.25 + 0.1;
    p = c + pos[0] * 0.1 + time * 0.25 + 0.1

    # c2+= ((sin(p)*0.7 + sin(p*4)*0.16 + sin(p*16)*0.14)*0.3333+0.3333) * _Color1;
    c2 = np.array((np.sin(p) * 0.7 + np.sin(p * 4) * 0.16 + np.sin(p * 16) * 0.14) * 0.3333 + 0.3333) * _Color1

    # p = .3*time + 0.1*pos.x - 0.1*pos.y + 0.15*pos.z;
    p = .3*time + 0.1*pos[0] - 0.1*pos[1] + 0.15*pos[2]

    # c = sin(p)*0.7 + sin(p*7)*0.15 + sin(p*9)*0.10;
    c = np.sin(p)*0.7 + np.sin(p*7)*0.15 + np.sin(p*9)*0.10

    # p = c + pos.x * 0.02 - pos.y * 0.08 + time * 0.25 + 0.5;
    p = c + pos[0] * 0.02 - pos[1] * 0.08 + time * 0.25 + 0.5

    # c2+= ((sin(p)*0.7 + sin(p*6)*0.16 + sin(p*25)*0.14)*0.3333+0.3333) * _Color2;
    c2 += ((np.sin(p)*0.7 + np.sin(p*6)*0.16 + np.sin(p*25)*0.14)*0.3333+0.3333) * _Color2

    # p = .2*time - 0.05*pos.x + 0.1*pos.y - 0.33*pos.z;
    p = .2 * time - 0.05 * pos[0] + 0.1 * pos[1] - 0.33 * pos[2]

    # c = sin(p)*0.7 + sin(p*10)*0.15 + sin(p*23)*0.10;
    c = np.sin(p)*0.7 + np.sin(p*10)*0.15 + np.sin(p*23)*0.10

    # p = c + pos.x * 0.1 - pos.y * 0.02 + pos.z * 0.3 + time * 0.25 + 0.25;
    p = c + pos[0] * 0.1 - pos[1] * 0.02 + pos[2] * 0.3 + time * 0.25 + 0.25

    # c2+= ((sin(p)*0.7 + sin(p*10)*0.16 + sin(p*19)*0.14)*0.3333+0.3333) * _Color3;
    c2 += ((np.sin(p)*0.7 + np.sin(p*10)*0.16 + np.sin(p*19)*0.14)*0.3333+0.3333) * _Color3

    return c2


class Reyna:

    def __init__(self):
        self.col_a = np.array([0, 255, 255])
        self.col_b = np.array([255, 0, 255])
        self.col_c = np.array([255, 255, 0])

    def update(self, t, harness):

        for led_id in harness.leds:
            pos = harness.leds[led_id]["position"]

            col = computeC(t, pos, self.col_a, self.col_b, self.col_c)

            harness.leds[led_id]["colour"] = np.clip(col, 0, 255)