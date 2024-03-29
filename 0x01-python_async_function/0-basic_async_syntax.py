#!/usr/bin/env python3

"""
- asynchronous coroutine that takes in an integer argument
    (max_delay, with a default value of 10) named wait_random
    that waits for a random delay between 0 and max_delay
    (included and float value) seconds and eventually returns it.

- Use the random module.
"""


import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """[summary]

    Args:
        max_delay (int, optional): [description]. Defaults to 10.

    Returns:
        float: [description]
    """
    random_delay = random.uniform(0, max_delay)
    await asyncio.sleep(random_delay)
    return random_delay

# if __name__ == "__main__":
#     print(asyncio.run(wait_random()))
#     print(asyncio.run(wait_random(5)))
#     print(asyncio.run(wait_random(15)))
