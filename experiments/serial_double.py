import argparse
import parsl


def double(x):
    return x * 2


def serial(n):
    print(n)
    k = []
    for i in range(n):
        k.append(double(n))
    return sum(k)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num", default="10", action="store", dest="n", type=int)
    args = parser.parse_args()
    print(serial(args.n))
