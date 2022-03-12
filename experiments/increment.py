import time
import argparse
import parsl
from parsl.app.app import python_app

from executors.all import execs


@python_app
def increment(x):
    return x + 1


@python_app
def slow_increment(x, dur):
    import time

    time.sleep(dur)
    return x + 1


def perform_increment(depth=5):
    futs = {0: 0}
    for i in range(1, depth):
        futs[i] = increment(futs[i - 1])

    x = sum([futs[i].result() for i in futs if not isinstance(futs[i], int)])
    return x


def perform_slow_increment(depth=5):
    futs = {0: 0}
    for i in range(1, depth):
        futs[i] = slow_increment(futs[i - 1], 0.1)

    x = sum([futs[i].result() for i in futs if not isinstance(futs[i], int)])

    return x


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
    start = time.time()
    print(perform_increment(args.d))
    end = time.time()
    print(end - start)
    start = time.time()
    print(perform_slow_increment(args.d))
    end = time.time()
    print(end - start)
