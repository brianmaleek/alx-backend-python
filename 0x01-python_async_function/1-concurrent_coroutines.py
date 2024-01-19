#!/usr/bin/env python3

""" module documentation """
import asyncio
import random
from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> list[float]:
    """ doc function """
    list_delays = []
    tasks_delay = []

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
