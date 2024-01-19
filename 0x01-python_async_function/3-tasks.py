#!/usr/bin/env python3

"""
- Description: Import wait_random from 0-basic_async_syntax.
- Write a function task_wait_random that takes an integer max_delay
        (do not create an async function, use the regular
        function syntax to do this)
- Return: a asyncio.Task.
"""


import asyncio

wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """
    Create an asyncio.Task for wait_random with the specified max_delay.

    Args:
        max_delay (int): Max delay of the function

    Returns:
        asyncio.Task: Task for wait_random
    """
    return asyncio.create_task(wait_random(max_delay))
