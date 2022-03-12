from executors.htex import local_few_htex, local_high_htex
from executors.tpex import local_few_threads, local_high_threads

execs = [local_few_htex, local_high_htex, local_few_threads, local_high_threads]
execs = {_exec.executors[0].label: _exec for _exec in execs}
