import time
from typing import Callable, Dict, Any

from utils.logger import logger


def logger_hook(
        function_name: str, function_call: Callable, arguments: Dict[str, Any]
):
    """Log the duration of the function call"""
    start_time = time.time()

    # Call the function
    result = function_call(**arguments)

    end_time = time.time()
    duration = end_time - start_time

    logger.info(f"Function {function_name} took {duration:.2f} seconds to execute")

    # Return the result
    return result
