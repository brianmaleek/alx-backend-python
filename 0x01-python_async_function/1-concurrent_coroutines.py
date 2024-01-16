#!/usr/bin/env python3

"""
- Import wait_random from the previous python file.
- write an async routine called wait_n that takes in 2 int arguments
    (in this order): n and max_delay.
- spawn wait_random n times with the specified max_delay.
- wait_n should return the list of all the delays (float values).
- List of delays should be in ascending order without using sort()
    because of concurrency.
"""


import asyncio
import random
from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> list[float]:
    """[summary]

    Args:
        n (int): [description]
        max_delay (int): [description]

    Returns:
        list[float]: [description]
    """
    list_delays: List[float] = []
    tasks_delay: List[asyncio.Task] = []

    for _ in range(n):
        task = wait_random(max_delay)
        tasks_delay.append(task)

    for task in asyncio.as_completed(tasks_delay):
        delay = await task
        list_delays.append(delay)

    return list_delays

# if __name__ == "__main__":
#     print(asyncio.run(wait_n(5, 5)))
#     print(asyncio.run(wait_n(10, 7)))
#     print(asyncio.run(wait_n(10, 0)))
