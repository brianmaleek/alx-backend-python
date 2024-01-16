#!/usr/bin/env python3

"""
- From the previous file, import wait_n into 2-measure_runtime.py.
- Create a measure_time function with integers n and max_delay as arguments
    that measures the total execution time for wait_n(n, max_delay), and
    returns total_time / n. Your function should return a float.

- Use the time module to measure an approximate elapsed time.
"""


import asyncio
import time

wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """[Measures the total execution time for wait_n(n, max_delay)]

    Args:
        n (int): [Number of times the function will be called]
        max_delay (int): [Max delay of the function]

    Returns:
        float: [Total execution time / n]
    """
    start = time.perf_counter()
    asyncio.run(wait_n(n, max_delay))
    end = time.perf_counter()

    total_time = end - start
    average_time = total_time / n
    return average_time


# if __name__ == "__main__":
#     n = 5
#     max_delay = 9

#     print(measure_time(n, max_delay))
