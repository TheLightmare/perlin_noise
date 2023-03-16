import pygame as pg
from pygame import gfxdraw
import noise
import math

import settings
import numpy as np
import terrain_utils
from PIL import Image, ImageDraw

WIDTH = 1000
HEIGHT = 1000
ZOOM = 10
DETAIL_LEVEL = 10

pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
image = Image.new(mode = "RGB", size = (WIDTH, HEIGHT), color = (0, 0, 0))
draw = ImageDraw.Draw(image)


def get_events():
    event = pg.event.get()
    if event == pg.QUIT:
        pg.quit()

def put_pixel(x, y, color):
    gfxdraw.pixel(screen, x, y, color)


def get_color_abs(noise): # get noise grayscale in absolute value
    r = abs(noise)
    return (r, r, r)

def get_color_trunc(noise): # get truncated noise grayscale
    noise += 0
    if noise < 0:
        return (0, 0, 0, 0)
    else :
        alpha = noise * 255 * 2
        if alpha > 255 :
            alpha = 255
        return (255, 255, 255, alpha)

def get_color_terrain(landmass_noise, moisture_noise, lookup_img: Image): # get color according to depth/altitude calculations
    thr = 0.1
    (w, h) = lookup_img.size
    pixel = (0, 0, 0)
    try :
        pixel = lookup_img.getpixel((moisture_noise * w, h - (landmass_noise**4) * h - 1))
    except :
        print(moisture_noise, landmass_noise, int(moisture_noise * w), int(h - landmass_noise * h - 1))

    '''
    if landmass_noise > thr :
        #pixel = (int(landmass_noise * 255), int(landmass_noise * 255), int(landmass_noise * 255))
        pixel = lookup_img.getpixel((moisture_noise * w, h - (landmass_noise + 1)/2 * h - 1))
    else :
        pixel = (13, 13, 150)
    '''
    return pixel


def render(offset):
    (offsx, offsy) = offset
    z = ZOOM/2000  # proper zoom value
    center = (WIDTH/2, HEIGHT/2)
    landmass_noise_array = np.zeros((WIDTH, HEIGHT))
    moisture_noise_array = np.zeros((WIDTH, HEIGHT))

    circle_grad = terrain_utils.circle_gradient(WIDTH, HEIGHT)

    print("Generating landmass noise array...")
    for j in range(0, HEIGHT):
        for i in range(0, WIDTH):
            landmass_noise_array[i, j] = (noise.pnoise2((i + offsx) * z, (j + offsy) * z, DETAIL_LEVEL, 0.5, 2.0, WIDTH, HEIGHT) + 1)/2 * circle_grad[i, j]
            moisture_noise_array[i, j] = (noise.pnoise2((i + 2 * offsx) * z, (j + 2 * offsy) * z, DETAIL_LEVEL, 0.5, 2.0, WIDTH,HEIGHT) + 1)/2
    print("Landmass noise array generated !")

    print("Normalizing landmass noise array...")
    max_grad = np.max(landmass_noise_array)
    landmass_noise_array = landmass_noise_array / max_grad

    print("Saving map...")
    lookup_img = Image.open(settings.LOOKUP_IMAGE)
    lookup_img = lookup_img.convert("RGB")
    progress = 0
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            prev_progress = progress
            progress = int((x + y * WIDTH) / (WIDTH * HEIGHT) * 100)
            if progress != prev_progress:
                print("Saving map... " + str(int((x + y * WIDTH) / (WIDTH * HEIGHT) * 100)) + "%")

            draw.point((x, y), get_color_terrain(landmass_noise_array[x, y], moisture_noise_array[x, y], lookup_img))

    image.save("map.png")


def render_clouds(offset, size = 4):
    (offsx, offsy) = offset
    z = size / 2000
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            n = noise.pnoise2((x + offsx) * z, (y + offsy) * z, DETAIL_LEVEL, 0.5, 2.0, WIDTH, HEIGHT)
            put_pixel(x, y, get_color_trunc(n))





