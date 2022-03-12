import psutil
import sys

sys.path.append("..")

from logs.logger import rootLogger


def core_count():
    N_physical_cores = psutil.cpu_count(logical=False)
    N_logical_cores = psutil.cpu_count(logical=True)
    rootLogger.info(
        f"The number f physical/logical cores is {N_physical_cores}/{N_logical_cores}"
    )
