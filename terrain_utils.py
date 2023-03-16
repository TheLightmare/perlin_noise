import noise
import settings
import numpy as np
import math

def water_color(noise, thr):
    noise += thr
    (r, g, b) = settings.SHORE
    noise = 1 - abs(noise)
    r *= noise
    g *= noise
    b *= noise
    return (int(r), int(g), int(b))

def terrain_color(noise, thr):
    noise += thr
    #noise = 1 - noise
    if noise <= 0.05 :
        return settings.TERRAIN
    elif noise <= 0.4 :
        return (0, 100, 0)
    else :
        return (255, 255, 255)




def circle_gradient(w, h):
    center_x = w // 2
    center_y  = h // 2
    circle_grad = np.zeros((h, w))

    offset = 100

    for y in range(h):
        for x in range(w):
            distx = abs(x - center_x) - offset
            disty = abs(y - center_y) - offset
            dist = math.sqrt(distx * distx + disty * disty)
            circle_grad[y][x] = dist * 0.5

    # get it between -1 and 1
    max_grad = np.max(circle_grad)
    circle_grad = circle_grad / max_grad
    circle_grad -= 0.5
    circle_grad *= 2.0
    circle_grad = -circle_grad

    # shrink gradient
    for y in range(h):
        for x in range(w):
            if circle_grad[y][x] > 0:
                circle_grad[y][x] *= 20

    # get it between 0 and 1
    max_grad = np.max(circle_grad)
    circle_grad = circle_grad / max_grad
    circle_grad = abs(circle_grad)
    return circle_grad