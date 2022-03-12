import parsl
import time

from PIL import Image
from parsl import python_app
from tools.n_cores import core_count

import argparse
from executors.all import execs

# from executors.llex import llex_config

core_count()


from logs.logger import rootLogger


def task_p(p):
    for i in range(3000):
        j = i ** 5
        j = i ** i
    return (p[0], 50, p[2])


@python_app
def parallel(p):
    for i in range(3000):
        j = i ** 5
        j = i ** i
    return (p[0], 50, p[2])


def serial(p):
    task_p(p)


class PixelManipulator(object):
    """
    Manipulates the pixel RGB values
    Args:
        length (int): number of pixels in the lenght of the image
        width (int): number of pixels in the width of the image
    """

    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.img = Image.new("RGB", (length, width), "black")
        self.list_of_pixels = list(self.img.getdata())

    def execute_parallel(self):
        rootLogger.info("Executing in Parallel")
        start = time.time()
        pixels = []
        rootLogger.info("Creating tasks")
        for i in self.list_of_pixels:
            pixels.append(parallel(i))
        rootLogger.info("tasks created, tasks - {}".format(len(pixels)))
        new_list_of_pixels = [i.result() for i in pixels]
        rootLogger.info("executed")
        end = time.time()
        elapsed_time = end - start
        rootLogger.info("In Parallel in {} seconds".format(elapsed_time))

    def execute_serial(self):
        rootLogger.info("Executing in Serial")
        start = time.time()
        pixels = []
        rootLogger.info("Creating tasks")
        for i in self.list_of_pixels:
            pixels.append(serial(i))
        rootLogger.info("tasks created, tasks - {}".format(len(pixels)))
        new_list_of_pixels = [i for i in pixels]
        rootLogger.info("executed")
        end = time.time()
        elapsed_time = end - start
        rootLogger.info("In Serial in {} seconds".format(elapsed_time))


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
    pm = PixelManipulator(args.w, args.w)
    pm.execute_parallel()
    pm.execute_serial()
