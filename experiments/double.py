import time
import argparse
import parsl
from parsl.app.app import python_app

from executors.all import execs
from logs.logger import rootLogger


@python_app
def double(x):
    return x * 2


def parallel_execution(n):
    res = []
    for i in range(n):
        res.append(double(i))
    x = sum([fut.result() for fut in res if not isinstance(fut, int)])
    return x


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num", default="10", action="store", dest="n", type=int)
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
    print(parallel_execution(args.n))
    end = time.time()
    print(end - start)
