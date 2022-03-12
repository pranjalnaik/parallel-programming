# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import json

EXEC = ["local_few_htex", "local_high_htex", "local_few_threads", "local_high_threads"]
PROGRAMS = ["double"]
NUM = [10, 100, 1000]
from collections import defaultdict

timings = defaultdict(lambda: defaultdict(dict))

for program in PROGRAMS:
    print(f"Program: {program}")
    for executor in EXEC:
        print(f" \t Executor: {executor}")
        for n in NUM:
            print(f" \t\t n: {n}")
            with open(f"{program}-{n}-{executor}.json", "r") as fp:
                lht = json.load(fp)
                children = lht["root_frame"]["children"][0]["children"][0]["children"][
                    0
                ]["children"][0]["children"]
                for function in children:
                    print(
                        "\t\t\t",
                        function["function"],
                        function["file_path_short"],
                        function["time"],
                    )
                    timings[function["function"] + "|" + function["file_path_short"]][
                        n
                    ][executor] = round(function["time"], 2)
    print("----------")

parallel = dict(timings["parallel_execution|double.py"])

import numpy as np
import matplotlib.pyplot as plt

nf = [10, 100, 1000]
rects = []
for exe in EXEC:
    g = []
    for n in parallel:
        g.append(parallel[n][exe])
    rects.append(g)

x = np.arange(len(nf))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots()

rects0 = ax.bar((x - (width * 1.5)), rects[0], width, label="local_few_htex")
rects1 = ax.bar(x - (width * 0.5), rects[1], width, label="local_high_htex")
rects2 = ax.bar(x + (width * 0.5), rects[2], width, label="local_few_threads")
rects3 = ax.bar(x + width * 1.5, rects[3], width, label="local_high_threads")

ax.set_ylabel("Executiion time in seconds")
ax.set_title("Double in parallel")
ax.set_xticks(x, nf)
ax.legend()

ax.bar_label(rects0, padding=3)
ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)
ax.bar_label(rects3, padding=3)



fig.tight_layout()
plt.show()
0 0.2 0.4 0.6
-0.1 0.1 0.3 0.5
# plt.xticks(X_axis, X)
# plt.xlabel("Groups")
# plt.ylabel("Number of Students")
# plt.title("Number of Students in each group")
# plt.legend()
# plt.show()
