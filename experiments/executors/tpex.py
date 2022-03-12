from parsl.config import Config
from parsl.executors.threads import ThreadPoolExecutor

local_few_threads = Config(
    executors=[ThreadPoolExecutor(max_threads=4, label="local_few_threads")]
)

local_high_threads = Config(
    executors=[ThreadPoolExecutor(max_threads=64, label="local_high_threads")]
)
