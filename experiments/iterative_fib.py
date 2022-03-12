import argparse

import parsl
from parsl.app.app import python_app
from executors.all import execs
import time


@python_app
def get_num(first, second):
    return first + second


def test_fibonacci(num=3):
    x1 = 0
    x2 = 1
    counter = 0
    results = []
    results.append(0)
    results.append(1)
    while counter < num - 2:
        counter += 1
        results.append(get_num(x1, x2))
        temp = x2
        x2 = get_num(x1, x2)
        x1 = temp
    for i in range(len(results)):
        if isinstance(results[i], int):
            print(results[i])
        else:
            print(results[i].result())


def serial_fibonacci(num=3):
    x1 = 0
    x2 = 1
    counter = 0
    results = []
    results.append(0)
    results.append(1)
    while counter < num - 2:
        counter += 1
        results.append(get_num(x1, x2))
        temp = x2
        x2 = x1 + x2
        x1 = temp
    for i in range(len(results)):
        if isinstance(results[i], int):
            print(results[i])
        else:
            print(results[i].result())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    from parsl.app.app import join_app, python_app
    from executors.all import execs

    parser.add_argument("-d", "--num", default="5", action="store", dest="d", type=int)
    parser.add_argument(
        "-e",
        "--exec",
        action="store",
        dest="exec",
        type=str,
    )
    args = parser.parse_args()
    executor = execs.get(args.exec)
    print("Loading executor with config:", executor)
    parsl.clear()
    parsl.load(executor)
    start2 = time.time()
    test_fibonacci(args.d)
    end2 = time.time()
    print(end2 - start2)
