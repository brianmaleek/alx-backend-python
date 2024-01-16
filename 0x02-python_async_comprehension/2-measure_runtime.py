#!/usr/bin/env python3

"""
- Description:
    - Import async_comprehension from the previous file.
    - write a measure_runtime coroutine that'll execute async_comprehension
        four times in parallel using asyncio.gather.
    - measure_runtime should measure the total runtime and return it.

- Notice that the total runtime is roughly 10 seconds, explain it to yourself.
"""


import asyncio
from typing import List

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    measure_runtime: coroutine that'll execute async_comprehension
        four times in parallel using asyncio.gather.
    """

    # compute the start time
    start_time = asyncio.get_event_loop().time()

    # create a list of async_comprehension() coroutines
    coroutines = [async_comprehension() for _ in range(4)]

    # execute the coroutines concurrently using asyncio.gather()
    await asyncio.gather(*coroutines)

    # compute the end time
    end_time = asyncio.get_event_loop().time()

    # return the total runtime
    run_time = end_time - start_time
    return run_time

# if __name__ == "__main__":
#     print(asyncio.run(measure_runtime()))
