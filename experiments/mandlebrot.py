import numpy as np
import os
import parsl

from parsl.app.app import bash_app
from parsl.app.app import python_app
import argparse
from executors.all import execs
import colorsys
import time
from logs.logger import rootLogger
from PIL import Image
from numpy import array


@python_app
def mandelbrot(x, y):
    from numpy import array
    import colorsys

    """
    Internal function for converstion to the RGB type
    tuple that can be added to the image.
    """

    def rgb_conversion(i):
        color = 255 * array(colorsys.hsv_to_rgb(i / 255.0, 1.0, 0.5))
        return tuple(color.astype(int))

    c0 = complex(x, y)
    c = 0
    for i in range(1, 1000):
        if abs(c) > 2:
            return rgb_conversion(i)
        c = c * c + c0
    return (0, 0, 0)


def mandelbrot_non_parallel(x, y):

    """
    Internal function for converstion to the RGB type
    tuple that can be added to the image
    """

    def rgb_conversion(i):
        color = 255 * array(colorsys.hsv_to_rgb(i / 255.0, 1.0, 0.5))
        return tuple(color.astype(int))

    c0 = complex(x, y)
    c = 0
    for i in range(1, 1000):
        if abs(c) > 2:
            return rgb_conversion(i)
        c = c * c + c0
    return (0, 0, 0)


def parallel(width):
    start = time.time()
    # Setting up the image
    WIDTH = width
    img = Image.new("RGB", (WIDTH, int(WIDTH / 2)))
    pixels_raw = [[0 for _ in range(img.size[1])] for _ in range(img.size[0])]

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            """
            Looping through the image width and height to update the
            raw pixels list with the output of the function
            """
            a = (x - (0.75 * WIDTH)) / (WIDTH / 4)
            b = (y - (WIDTH / 4)) / (WIDTH / 4)
            pixels_raw[x][y] = mandelbrot(a, b)

    pixels_raw = [[i.result() for i in x] for x in pixels_raw]

    # Projecting the raw pixels onto the image
    pixels = img.load()

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pixels[x, y] = pixels_raw[x][y]

    end = time.time()
    print(end - start)


def serial(width):
    start2 = time.time()
    # Setting up the image
    WIDTH = width
    img = Image.new("RGB", (WIDTH, int(WIDTH / 2)))
    pixels_raw = [[0 for _ in range(img.size[1])] for _ in range(img.size[0])]

    for x in range(img.size[0]):
        for y in range(img.size[1]):

            # Looping through the image width and height to update the
            # raw pixels list with the output of the function

            a = (x - (0.75 * WIDTH)) / (WIDTH / 4)
            b = (y - (WIDTH / 4)) / (WIDTH / 4)
            pixels_raw[x][y] = mandelbrot_non_parallel(a, b)

    # Projecting the raw pixels onto the image
    pixels = img.load()

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pixels[x, y] = pixels_raw[x][y]

    end2 = time.time()
    print(end2 - start2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w", "--width", default="10", action="store", dest="w", type=int
    )
    parser.add_argument(
        "-e",
        "--exec",
        action="store",
        dest="exec",
        type=str,
    )
    args = parser.parse_args()
    parsl.clear()
    executor = execs.get(args.exec)
    print("Loading executor with config:", executor)
    parsl.load(executor)
    parallel(args.w)
    # serial(args.w)
