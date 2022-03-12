from parsl.providers import LocalProvider
from parsl.channels import LocalChannel
from parsl.config import Config
from parsl.executors import HighThroughputExecutor

local_few_htex = Config(
    executors=[
        HighThroughputExecutor(
            label="local_few_htex",
            worker_debug=True,
            cores_per_worker=1,
            poll_period=10,
            prefetch_capacity=0,
            provider=LocalProvider(
                channel=LocalChannel(),
                init_blocks=1,
                max_blocks=1,
            ),
        )
    ],
    strategy=None,
)

local_high_htex = Config(
    executors=[
        HighThroughputExecutor(
            label="local_high_htex",
            worker_debug=False,
            cores_per_worker=4,
            max_workers=64,
            prefetch_capacity=32,
            provider=LocalProvider(
                channel=LocalChannel(),
                init_blocks=1,
                parallelism=1.0,
                max_blocks=70,
            ),
        )
    ],
    strategy=None,
)
