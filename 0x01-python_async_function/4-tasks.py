#!/usr/bin/env python3

"""
- Description: Take the code from wait_n and alter it into a new function
    task_wait_n. The code is nearly identical to wait_n except
    task_wait_random is being called.
"""

import asyncio
from typing import List

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    Spawn task_wait_random n times with the specified max_delay.

    Args:
        n (int): Number of times to spawn task_wait_random.
        max_delay (int): Maximum delay value.

    Returns:
        List[float]: List of delays in ascending order.
    """
    delays = [task_wait_random(max_delay) for _ in range(n)]
    return [await delay for delay in asyncio.as_completed(delays)]
