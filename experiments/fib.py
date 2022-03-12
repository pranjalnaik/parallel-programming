import argparse
from parsl.app.app import join_app, python_app
from executors.all import execs
from logs.logger import rootLogger

import parsl


@python_app
def add(*args):
    """Add all of the arguments together. If no arguments, then
    zero is returned (the neutral element of +)
    """
    accumulator = 0
    for v in args:
        accumulator += v
    return accumulator


@join_app
def fibonacci(n):
    if n == 0:
        return add()
    elif n == 1:
        return add(1)
    else:
        return add(fibonacci(n - 1), fibonacci(n - 2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--num", default="5", action="store", dest="d", type=int)
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
    print(fibonacci(args.d).result())
