#!/usr/bin/env python3

"""
- Description: type-annotated function `sum_list` takes a list `input_list`
                of floats as argument
- Parameters: returns their sum as a float.
"""

from typing import List


def sum_list(input_list: List[float]) -> float:
    """ Returns the sum of a list of floats """
    return sum(input_list)
