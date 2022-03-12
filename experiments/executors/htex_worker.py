from parsl.config import Config
from parsl.channels import LocalChannel
from parsl.executors import HighThroughputExecutor
from parsl.providers import LocalProvider

htex_worker = Config(
    executors=[
        HighThroughputExecutor(
            label="htex",
            max_workers=56,
            provider=LocalProvider(),
        )
    ],
)
