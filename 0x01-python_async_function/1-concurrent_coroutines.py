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
from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Spawn wait_random n times with the specified max_delay.

    Args:
        n (int): Number of times to spawn wait_random.
        max_delay (int): Maximum delay value.

    Returns:
        List[float]: List of delays in ascending order.
    """
    tasks = [wait_random(max_delay) for _ in range(n)]

    # Use asyncio.gather for simplicity and conciseness
    completed_tasks = [await task for task in asyncio.as_completed(tasks)]

    return completed_tasks


# if __name__ == "__main__":
#     print(asyncio.run(wait_n(5, 5)))
#     print(asyncio.run(wait_n(10, 7)))
#     print(asyncio.run(wait_n(10, 0)))
