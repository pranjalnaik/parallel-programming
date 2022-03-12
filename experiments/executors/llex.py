from parsl.config import Config
from parsl.executors import LowLatencyExecutor
from parsl.launchers import SingleNodeLauncher

# does not work raises the following error
"""
    LowLatencyExecutor(
TypeError: Can't instantiate abstract class LowLatencyExecutor with abstract method _get_block_and_job_ids
"""
llex_config = Config(
    executors=[
        LowLatencyExecutor(
            launcher=SingleNodeLauncher(debug=True, fail_on_any=False), max_blocks=20
        )
    ]
)
